from typing import Optional, Iterable, List, Sequence, Union

from pydantic import BaseModel, ConfigDict

from xddtools import AutoName
from xddtools.base import HeroEntry, get_entry_id, LootMonsterEntry
from xddtools.entries import Effect, Buff, Animation
from xddtools.entries.colour import debuff, heal_hp, skill_unselectable
from xddtools.enum import EffectTarget, BuffType, STDisableCombatSkillAttribute, CurioResultType, BuffSource, \
    BuffDurationType, STCombatStatAdd, HealSource
from xddtools.utils import float_to_percent_int


def get_str_tooltip_effect(text: str) -> Effect:
    """
    为 skill 添加文本提示
    :param text:
    :return:
    """
    return Effect(
        target=EffectTarget.PERFORMER,
        buff_ids=[Buff(
            stat_type=BuffType.UPGRADE_DISCOUNT,
            stat_sub_type=AutoName().new_sub_type(),
            buff_stat_tooltip=text
        )],
        on_miss=True,
        skill_instant=True,
        apply_once=True
    )


def get_str_tooltip_buff(text: str) -> Buff:
    """
    为 trinket 添加文本提示
    :param text:
    :return:
    """
    return Buff(
        stat_type=BuffType.UPGRADE_DISCOUNT,
        stat_sub_type=AutoName().new_sub_type(),
        buff_stat_tooltip=text
    )


def get_number_tooltip_buff(
        text: Optional[str] = None,
        amount: int = 1,
        keep_last_sub_type: bool = False
) -> Buff:
    """
    生成可以累计计数的 buff 提示
    :param text:
    :param amount:
    :param keep_last_sub_type:
    :return:
    """
    if not keep_last_sub_type and text is not None and "%d" not in text:
        raise ValueError("text must contain %d")
    if keep_last_sub_type and text is not None:
        raise ValueError("text must be None when keep_last_sub_type is True")
    if keep_last_sub_type:
        sub_type = AutoName().last_sub_type()
        text = None
    else:
        sub_type = AutoName().new_sub_type()
    return Buff(
        stat_type=BuffType.QUIRK_TAG_EVOLUTION_DURATION,
        stat_sub_type=sub_type,
        buff_stat_tooltip=text,
        amount=amount,
        remove_if_not_active=True,
        is_clear_debuff_valid=False,
    )


def get_cd_tag_effect(cd_type: STDisableCombatSkillAttribute = STDisableCombatSkillAttribute.DAZE) -> Effect:
    """
    生成的 effect 可以给 skill 添加对应类型的技能禁用标签
    :param cd_type:
    :return:
    """
    effect = Effect(
        target=EffectTarget.PERFORMER,
        curio_result_type=CurioResultType.NEGATIVE,
        chance=0,
        duration=1,
        on_hit=False,
        has_description=False,
        apply_once=True
    )
    if cd_type == STDisableCombatSkillAttribute.DAZE:
        effect.daze = True
    elif cd_type == STDisableCombatSkillAttribute.TAG:
        effect.tag = True
    elif cd_type == STDisableCombatSkillAttribute.GUARD:
        effect.guard = True
    elif cd_type == STDisableCombatSkillAttribute.STUN:
        effect.stun = 1
    elif cd_type == STDisableCombatSkillAttribute.BLEED:
        effect.dot_bleed = 1
    elif cd_type == STDisableCombatSkillAttribute.POISON:
        effect.dot_poison = 1
    elif cd_type == STDisableCombatSkillAttribute.HEAL:
        effect.heal = 1
    elif cd_type == STDisableCombatSkillAttribute.STRESS:
        effect.stress = 1
    elif cd_type == STDisableCombatSkillAttribute.DEBUFF:
        effect.combat_stat_buff = True
        effect.speed_rating_add = -1
    elif cd_type == STDisableCombatSkillAttribute.BUFF:
        effect.combat_stat_buff = True
        effect.speed_rating_add = 1
    else:
        raise ValueError("cd_type is not supported")
    return effect


def get_clear_self_buff_source_effect(buff_source: BuffSource = BuffSource.NEVER_AGAIN) -> Effect:
    """
    完全驱散自身所有属于 buff_source 来源的 buff
    :param buff_source:
    :return:
    """
    return Effect(
        target=EffectTarget.PERFORMER,
        on_miss=True,
        steal_buff_source_type=buff_source,
        has_description=False,
        apply_once=True
    )


class CDCharge(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    disable: STDisableCombatSkillAttribute
    amount: int


def get_cd_charge_effect(
        cd_charges: Iterable[CDCharge],
        tooltip_buff: Optional[Buff] = None,
        chance: float = 100,
        buff_source: BuffSource = BuffSource.NEVER_AGAIN,
        buff_duration_type: BuffDurationType = BuffDurationType.QUEST_END,
        duration: int = 1
) -> Effect:
    """
    给技能 CD 充能，需要搭配禁用技能的 quirk 和 get_clear_self_buff_source_effect 函数一起使用
    :param cd_charges:
    :param tooltip_buff:
    :param chance:
    :param buff_source:
    :param buff_duration_type:
    :param duration:
    :return:
    """
    positive = 0
    negative = 0

    effect = Effect(
        target=EffectTarget.PERFORMER,
        chance=chance,
        duration=duration,
        buff_duration_type=buff_duration_type,
        buff_source_type=buff_source,
        on_miss=True,
        has_description=False,
        apply_once=True
    )

    buffs = []
    if tooltip_buff is not None:
        buffs.append(tooltip_buff)

    for cd_charge in cd_charges:
        if cd_charge.amount <= 0:
            positive += 1
        else:
            negative += 1
        buffs.append(Buff(
            stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
            stat_sub_type=cd_charge.disable,
            amount=cd_charge.amount,
            has_description=False,
            is_clear_debuff_valid=False,
        ))
    if positive >= negative:
        effect.curio_result_type = CurioResultType.POSITIVE
    else:
        effect.curio_result_type = CurioResultType.NEGATIVE
    effect.buff_ids = buffs

    return effect


def get_duration_localization(
    duration_type: Optional[BuffDurationType] = None,
    duration: Optional[int] = None
) -> str:
    """
    获取持续时间的翻译文本，仅用于技能描述
    :param duration_type:
    :param duration:
    :return:
    """
    if duration_type is None:
        duration_type = BuffDurationType.ROUND
    if duration is None:
        duration = 1
    if duration_type in [
        BuffDurationType.ROUND,
        BuffDurationType.BEFORE_TURN,
        BuffDurationType.AFTER_TURN
    ]:
        return f"（持续{duration}个回合）"
    elif duration_type == BuffDurationType.COMBAT_END:
        return f"（持续{duration}场战斗）"
    elif duration_type in [
        BuffDurationType.QUEST_COMPLETE,
        BuffDurationType.QUEST_END,
        BuffDurationType.QUEST_NOT_COMPLETE,
    ]:
        return f"（持续{duration}个任务）"
    elif duration_type == BuffDurationType.ACTIVITY_END:
        return f"（持续{duration}个活动）"
    elif duration_type == BuffDurationType.IDLE_START_TOWN_VISIT:
        return f"（持续{duration}周）"
    elif duration_type == BuffDurationType.TILL_REMOVE:
        return f"（直到移除）"
    elif duration_type == BuffDurationType.AFTER_ROUND:
        return f"（持续{duration}整轮）"
    else:
        return " "


def get_steal_target_max_life_effects(
        amount: int,
        buff_duration_type=BuffDurationType.COMBAT_END,
        duration=3
) -> List[Effect]:
    return [
        Effect(
            target=EffectTarget.PERFORMER,
            buff_duration_type=buff_duration_type,
            duration=duration,
            apply_once=True,
            has_description=False,
            buff_ids=[
                Buff(
                    stat_type=BuffType.COMBAT_STAT_ADD,
                    stat_sub_type=STCombatStatAdd.MAX_HP,
                    amount=amount,
                    duration_type=buff_duration_type,
                    duration=duration
                ),
            ]
        ),
        Effect(
            target=EffectTarget.TARGET,
            chance=100,
            buff_duration_type=buff_duration_type,
            duration=duration,
            apply_once=True,
            has_description=False,
            buff_ids=[
                Buff(
                    stat_type=BuffType.COMBAT_STAT_ADD,
                    stat_sub_type=STCombatStatAdd.MAX_HP,
                    amount=amount * -1,
                    duration_type=buff_duration_type,
                    duration=duration
                ),
            ]
        ),
        get_str_tooltip_effect(f"{debuff('偷取')}目标{amount}点{heal_hp('最大生命')}"
                               f"{skill_unselectable(get_duration_localization(buff_duration_type, duration))}")
    ]


def get_suck_blood_effects(
        heal_percent: float
):
    """
    需要搭配 skill 中的 damage_heal_base_class_ids 属性使用
    :param heal_percent: 生命偷取比例
    :return:
    """
    if heal_percent < 0 or heal_percent > 1:
        raise ValueError("heal_percent must be in range [0, 1]")

    return [
        Effect(
            target=EffectTarget.PERFORMER,
            skill_instant=True,
            has_description=False,
            buff_ids=[
                Buff(
                    stat_type=BuffType.HP_HEAL_RECEIVED_PERCENT,
                    stat_sub_type=HealSource.DAMAGE_HEAL,
                    amount=round(heal_percent - 1, 2),
                )
            ]
        ),
        get_str_tooltip_effect(f"{float_to_percent_int}%% {heal_hp('生命偷取')}")
    ]


def get_trinket_fx_buffs(fx_dir: str, heroes: Sequence[Union[HeroEntry, str]]) -> List[Buff]:
    res = []
    sub_type = AutoName().new_sub_type()
    for hero in heroes:
        res.append(Buff(
            stat_type=BuffType.UPGRADE_DISCOUNT,
            stat_sub_type=sub_type,
            has_description=False,
            duration=-1,
            fx=Animation(
                anim_name=sub_type + "_fx",
                anim_dir=fx_dir,
                is_fx=True,
                need_rename=False,
                hero_name=get_entry_id(hero)
            )
        ))
    return res


def get_summon_loot_monster_effect(
        loot_monster: Union[LootMonsterEntry, str]
) -> Effect:
    return Effect(
        target=EffectTarget.PERFORMER,
        summon_count=1,
        summon_can_spawn_loot=True,
        summon_monsters=[f"{get_entry_id(loot_monster)}_A"],
        summon_chances=[1],
        summon_ranks=["01234"],
        summon_does_roll_initiatives=False,
        on_miss=True,
        apply_once=True,
        has_description=False
    )


if __name__ == '__main__':
    # AutoName.set_default_prefix("xue")
    # t1 = get_number_tooltip_buff("魔力值：%d", amount=1)
    # t2 = get_number_tooltip_buff(amount=2, keep_last_sub_type=True)
    # print(t1)
    # print(t2)
    #
    # c1 = get_cd_charge_effect([CDCharge(disable=STDisableCombatSkillAttribute.DAZE, amount=1)], tooltip_buff=t1)
    # print(c1)
    # print(c1.buff_ids[0])
    e = get_summon_loot_monster_effect("loot_monster_test")
    print(e)

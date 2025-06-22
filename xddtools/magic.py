import glob
import hashlib
import os
import re
import shutil
from typing import Optional, Iterable, List, Union, Tuple, Sequence, Dict

from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel, ConfigDict

from xddtools import AutoName
from xddtools.base import HeroEntry, get_entry_id, LootMonsterEntry, BankEntry, ModeEntry
from xddtools.entries import Effect, Buff, Animation, TrinketEffect
from xddtools.entries.colour import debuff, heal_hp, skill_unselectable
from xddtools.enum import EffectTarget, BuffType, STDisableCombatSkillAttribute, CurioResultType, BuffSource, \
    BuffDurationType, STCombatStatAdd, HealSource, TrinketTriggerType
from xddtools.path import DATA_PATH
from xddtools.utils import float_to_percent_int

# 原版18个职业
ALL_HEROES = ("bounty_hunter", "crusader", "vestal", "occultist",
              "hellion", "grave_robber", "highwayman", "plague_doctor",
              "jester", "leper", "arbalest", "man_at_arms",
              "houndmaster", "abomination", "antiquarian", "musketeer",
              "shieldbreaker", "flagellant")


def get_effect_order_dict(order: int = 3) -> Dict[str, Optional[bool]]:
    """
    获得指定优先级的 Effect 参数字典
    :param order: 0最高优先级，第一批执行
    :return:
    """
    res = {
        "skill_instant": False,
        "queue": True,
        "push": None
    }
    if order == 0:
        res["skill_instant"] = True
    elif order == 1:
        res["queue"] = False
    elif order == 2:
        res["queue"] = False
        res["push"] = 0
    elif order == 3:
        pass
    elif order == 4:
        res["push"] = 0
    else:
        raise ValueError("order is not supported,only 0-4")
    return res


def get_str_tooltip_effect(
        text: str,
        target: EffectTarget = EffectTarget.PERFORMER
) -> Effect:
    """
    为 skill 添加文本提示
    :param text:
    :param target:
    :return:
    """
    return Effect(
        target=target,
        buff_ids=[Buff(
            stat_type=BuffType.UPGRADE_DISCOUNT,
            stat_sub_type=AutoName().new_sub_type(),
            buff_stat_tooltip=text
        )],
        on_hit=True,
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
        # remove_if_not_active=True,
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


def get_clear_self_buff_source_effect(
        buff_source: BuffSource = BuffSource.NEVER_AGAIN,
        chance: float = 1.0,
        order: int = 3
) -> Effect:
    """
    完全驱散自身所有属于 buff_source 来源的 buff
    :param buff_source:
    :param chance:
    :param order:
    :return:
    """
    return Effect(
        target=EffectTarget.PERFORMER,
        chance=chance,
        on_miss=True,
        steal_buff_source_type=buff_source,
        has_description=False,
        apply_once=True,
        **get_effect_order_dict(order)
    )


class CDCharge(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)

    disable: STDisableCombatSkillAttribute
    amount: int


def get_cd_charge_effect(
        cd_charges: Iterable[CDCharge],
        other_buffs: Optional[Sequence[Buff]] = None,
        chance: float = 100,
        buff_source: BuffSource = BuffSource.NEVER_AGAIN,
        buff_duration_type: BuffDurationType = BuffDurationType.QUEST_END,
        duration: int = 1,
        on_hit: bool = True,
        on_miss: bool = True,
        order: int = 3
) -> Effect:
    """
    给技能 CD 充能，需要搭配禁用技能的 quirk 和 get_clear_self_buff_source_effect 函数一起使用
    :param cd_charges:
    :param other_buffs:
    :param chance:
    :param buff_source:
    :param buff_duration_type:
    :param duration:
    :param on_miss:
    :param on_hit:
    :param order:
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
        on_hit=on_hit,
        on_miss=on_miss,
        has_description=False,
        apply_once=True,
        **get_effect_order_dict(order)
    )

    buffs = []
    if other_buffs is not None:
        buffs.extend(other_buffs)

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
        return f"(持续{duration}回合)"
    elif duration_type == BuffDurationType.COMBAT_END:
        return f"(持续{duration}战斗)"
    elif duration_type in [
        BuffDurationType.QUEST_COMPLETE,
        BuffDurationType.QUEST_END,
        BuffDurationType.QUEST_NOT_COMPLETE,
    ]:
        return f"(持续{duration}任务)"
    elif duration_type == BuffDurationType.ACTIVITY_END:
        return f"(持续{duration}活动)"
    elif duration_type == BuffDurationType.IDLE_START_TOWN_VISIT:
        return f"(持续{duration}周)"
    elif duration_type == BuffDurationType.TILL_REMOVE:
        return f"(直到移除)"
    elif duration_type == BuffDurationType.AFTER_ROUND:
        return f"(持续{duration}整轮)"
    else:
        return " "


def get_steal_target_max_life_effects(
        amount: int,
        buff_duration_type=BuffDurationType.COMBAT_END,
        duration: int = 3,
        order: int = 3
) -> List[Effect]:
    """
    生命偷取所需的所有 Effect
    :param amount:
    :param buff_duration_type:
    :param duration:
    :param order:
    :return:
    """
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
            ],
            **get_effect_order_dict(order)
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
            ],
            **get_effect_order_dict(order)
        ),
        get_str_tooltip_effect(f"{debuff('偷取')}目标{amount}点{heal_hp('最大生命')}"
                               f"{skill_unselectable(get_duration_localization(buff_duration_type, duration))}")
    ]


def get_suck_blood_effects(
        heal_percent: float,
        has_description: bool = True
) -> List[Effect]:
    """
    需要搭配 skill 中的 damage_heal_base_class_ids 属性使用
    :param heal_percent: 生命偷取比例
    :param has_description:
    :return:
    """
    if heal_percent < 0:
        raise ValueError("heal_percent cannot be negative")

    res = [
        Effect(
            target=EffectTarget.PERFORMER,
            skill_instant=True,
            apply_once=True,
            has_description=False,
            buff_ids=[
                Buff(
                    stat_type=BuffType.HP_HEAL_RECEIVED_PERCENT,
                    stat_sub_type=HealSource.DAMAGE_HEAL,
                    amount=round(heal_percent - 1, 2),
                )
            ]
        )
    ]
    if has_description:
        res.append(get_str_tooltip_effect(f"{float_to_percent_int(heal_percent)}%% {heal_hp('生命偷取')}"))

    return res


def get_hero_fx_sfx_buff(
        hero: Union[HeroEntry, str],
        fx_dir: Optional[str] = None,
        sfx: Optional[BankEntry] = None,
        # duration: int = -1
) -> Buff:
    """
    用于指定英雄的特效Buff
    :param hero:
    :param fx_dir:
    :param sfx:
    :return:
    """
    if fx_dir is None and sfx is None:
        raise ValueError("fx_dir and sfx cannot be both None")

    if fx_dir is None:
        fx_dir = os.path.join(DATA_PATH, "template/fx/sfx")

    return Buff(
        stat_type=BuffType.UPGRADE_DISCOUNT,
        stat_sub_type=AutoName().new_sub_type(),
        has_description=False,
        # duration=duration,
        fx=Animation(
            anim_dir=fx_dir,
            is_fx=True,
            need_rename=False,
            hero_name=hero
        ),
        fx_onset_sfx=sfx
    )


def get_summon_loot_monster_effect(
        loot_monster: Union[LootMonsterEntry, str],
        target: EffectTarget = EffectTarget.PERFORMER,
        chance: float = 1,
        queue: bool = True,
        on_hit: bool = True,
        on_miss: bool = True
) -> Effect:
    return Effect(
        target=target,
        chance=chance,
        summon_count=1,
        summon_can_spawn_loot=True,
        summon_monsters=[loot_monster],
        summon_chances=[1],
        summon_ranks=["01234"],
        summon_does_roll_initiatives=False,
        on_hit=on_hit,
        on_miss=on_miss,
        apply_once=True,
        has_description=False,
        queue=queue
    )


def get_title_fx(
        hero: Union[HeroEntry, str],
        text: str,
        font_path: Optional[str] = None,
        font_size: int = 60,
        text_color: Optional[Tuple[int, int, int]] = None,
        y_offset: int = -5,
) -> Animation:
    if text_color is None:
        text_color = (255, 255, 255)
    if font_path is None:
        font_path = os.path.join(DATA_PATH, "template/font/TianZhenWuXieShouJinTi-2.ttf")
    fx_dir = os.path.join(DATA_PATH, "template/fx/skill_bark")
    fx_name = hashlib.md5((text + str(text_color)).encode()).hexdigest()
    anim = Animation(anim_dir=fx_dir, anim_name=fx_name, is_fx=True, need_rename=False)
    root_dir = os.path.join(DATA_PATH, "temp")
    anim.copy_and_rename_animation(root_dir)
    anim_dir = os.path.join(root_dir, "fx", fx_name)
    res = Animation(
        anim_dir=anim_dir,
        is_fx=True,
        hero_name=hero,
        need_rename=False
    )

    image = Image.open(res.png_path)
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - 30 - text_width) / 2
    y = (height - text_height) / 2 + y_offset

    draw.text((x, y), text, fill=text_color, font=font)
    image.save(res.png_path)

    return res


def get_title_effect(
        hero: Union[HeroEntry, str],
        text: str,
        font_path: Optional[str] = None,
        font_size: int = 60,
        text_color: Optional[Tuple[int, int, int]] = None,
        y_offset: int = -5,
        target: EffectTarget = EffectTarget.PERFORMER,
        sfx: Optional[BankEntry] = None,
) -> Effect:
    return Effect(
        target=target,
        chance=1.01,
        skill_instant=True,
        buff_source_type=BuffSource.NOTSPECIFIED,
        buff_duration_type=BuffDurationType.BEFORE_TURN,
        duration=1,
        on_miss=True,
        queue=False,
        has_description=False,
        apply_once=True,
        buff_ids=[
            Buff(
                stat_type=BuffType.UPGRADE_DISCOUNT,
                stat_sub_type=AutoName().new_sub_type(),
                remove_on_battle_complete=True,
                has_description=False,
                fx=get_title_fx(hero, text, font_path, font_size, text_color, y_offset),
                fx_onset_sfx=sfx
            )
        ]
    )


def get_trinket_effect_sfx(
        hero: Union[HeroEntry, str],
        trigger: TrinketTriggerType,
        sfx: Optional[BankEntry] = None,
) -> TrinketEffect:
    target = EffectTarget.PERFORMER
    if trigger == TrinketTriggerType.KILL_PERFORMER:
        target = EffectTarget.TARGET

    res = TrinketEffect(
        trigger=trigger,
        effects=[
            Effect(
                target=target,
                has_description=False,
                apply_once=True,
                on_miss=True,
                duration=1,
                buff_ids=[
                    get_hero_fx_sfx_buff(hero, sfx=sfx)
                ]
            )
        ]
    )
    return res


def copy_and_rename_hero_fx(hero_dir: str, heroes: Optional[Sequence[Union[HeroEntry, str]]] = None) -> List[str]:
    if heroes is None:
        heroes = ALL_HEROES
    exist_hero = os.path.split(hero_dir)[-1]
    heroes = [get_entry_id(hero) for hero in heroes if hero != exist_hero]

    res = []

    for hero in heroes:
        dst_dir = os.path.join(os.path.dirname(hero_dir), hero)
        shutil.copytree(hero_dir, dst_dir, dirs_exist_ok=True)
        for file in glob.glob(os.path.join(dst_dir, "fx", "*.*")):
            file_name = os.path.basename(file)
            tem = file_name.split(".")
            tem[0] = hero
            new_file_name = ".".join(tem)
            new_path = os.path.join(os.path.dirname(file), new_file_name)

            if file.endswith(".atlas"):
                with open(file, 'r', encoding='utf-8') as f:
                    data = f.read()
                pattern = r'^(.*?)\.png$'
                tem = new_file_name.split(".")
                tem[-1] = "png"
                new_png_name = ".".join(tem)
                result = re.sub(pattern, new_png_name, data, count=1, flags=re.MULTILINE)
                with open(new_path, 'w', encoding='utf-8') as f:
                    f.write(result)
                os.remove(file)
            else:
                os.rename(file, new_path)

            res.append(new_path)

    return res


def get_set_mode_effect(
        mode: Union[ModeEntry, str],
        has_description: bool = True,
        on_hit: bool = True,
        on_miss: bool = True,
        order: int = 1
):
    return Effect(
        target=EffectTarget.PERFORMER,
        chance=100,
        set_mode=mode,
        on_hit=on_hit,
        on_miss=on_miss,
        apply_once=True,
        has_description=has_description,
        **get_effect_order_dict(order)
    )


if __name__ == '__main__':
    print(get_effect_order_dict(5))
    # res = copy_and_rename_hero_fx(r"D:\Users\Desktop\x_dd_tools\examples\xhos\xhos\heroes\xjiangshi")
    # print(res)

    # AutoName.set_default_prefix("xue")
    # t1 = get_number_tooltip_buff("魔力值：%d", amount=1)
    # t2 = get_number_tooltip_buff(amount=2, keep_last_sub_type=True)
    # print(t1)
    # print(t2)
    #
    # c1 = get_cd_charge_effect([CDCharge(disable=STDisableCombatSkillAttribute.DAZE, amount=1)], tooltip_buff=t1)
    # print(c1)
    # print(c1.buff_ids[0])
    # e = get_summon_loot_monster_effect("loot_monster_test")
    # print(e)
    # a = get_title_fx("hero_test", "测试标题")

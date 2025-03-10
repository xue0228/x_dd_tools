from public import auto_name

from xddtools.buffs import Buff
from xddtools.colour import buff
from xddtools.effects import Effect, TooltipEffect
from xddtools.enums import BuffType, STDisableCombatSkillAttribute, EffectTarget, CurioResultType, BuffDurationType, \
    BuffSource, MonsterType

crit_effect = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    buff_source_type=BuffSource.CRIT,
    apply_once=True,
    duration=3,
    buff_ids=(
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.STRESS_HEAL_PERCENT,
            amount=0.25,
        ),
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
            amount=-0.25,
        )
    )
)

# 魔力值提示buff
magic_tooltip_h1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.QUIRK_TAG_EVOLUTION_DURATION,
    stat_sub_type=auto_name.new_sub_type(),
    amount=1,
    remove_if_not_active=True,
    is_clear_debuff_valid=False,
    localization=f'魔力值：%d'
)

poison_l1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
    stat_sub_type=STDisableCombatSkillAttribute.POISON,
    amount=-1,
    has_description=False,
    is_clear_debuff_valid=False,
)
tag_l1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
    stat_sub_type=STDisableCombatSkillAttribute.TAG,
    amount=-1,
    has_description=False,
    is_clear_debuff_valid=False,
)
stun_l1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
    stat_sub_type=STDisableCombatSkillAttribute.STUN,
    amount=-1,
    has_description=False,
    is_clear_debuff_valid=False,
)

poison_h1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
    stat_sub_type=STDisableCombatSkillAttribute.POISON,
    amount=1,
    has_description=False,
    is_clear_debuff_valid=False,
)
tag_h2 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
    stat_sub_type=STDisableCombatSkillAttribute.TAG,
    amount=2,
    has_description=False,
    is_clear_debuff_valid=False,
)
stun_h4 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
    stat_sub_type=STDisableCombatSkillAttribute.STUN,
    amount=4,
    has_description=False,
    is_clear_debuff_valid=False,
)

# 为技能增加cd的effect
daze_cd = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.NEGATIVE,
    chance=0,
    daze=True,
    duration=1,
    on_hit=False,
    has_description=False,
    apply_once=True,
)

clear_charge = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    on_miss=True,
    steal_buff_source_type=BuffSource.NEVER_AGAIN,
    has_description=False,
    apply_once=True,
)

charges = [Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    chance=chance,
    duration=1,
    buff_duration_type=BuffDurationType.QUEST_END,
    buff_source_type=BuffSource.NEVER_AGAIN,
    on_miss=True,
    has_description=False,
    apply_once=True,
    buff_ids=(
        magic_tooltip_h1,
        # poison_l1,
        # tag_l1,
        # stun_l1,
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
            stat_sub_type=STDisableCombatSkillAttribute.POISON,
            amount=-1,
            has_description=False,
            is_clear_debuff_valid=False,
        ),
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
            stat_sub_type=STDisableCombatSkillAttribute.TAG,
            amount=-1,
            has_description=False,
            is_clear_debuff_valid=False,
        ),
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
            stat_sub_type=STDisableCombatSkillAttribute.STUN,
            amount=-1,
            has_description=False,
            is_clear_debuff_valid=False,
        )
    )
) for chance in [100, 0.25, 0.16, 0.08, 100]]

meditations = [Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    duration=3,
    apply_once=True,
    combat_stat_buff=True,
    attack_rating_add=atk,
    crit_chance_add=crit,
) for atk, crit in [(0.05, 0.02), (0.06, 0.03), (0.07, 0.04), (0.08, 0.05), (0.10, 0.06)]]

poisons = [Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.NEGATIVE,
    chance=chance,
    dot_poison=dot,
    duration=3
) for chance, dot in [(1.0, 3), (1.1, 3), (1.2, 4), (1.3, 4), (1.4, 5)]]

tags = [Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.NEGATIVE,
    tag=True,
    chance=chance
) for chance in [0.6, 0.7, 0.8, 0.9, 1.0]]

stuns = [Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.NEGATIVE,
    chance=chance,
    stun=1,
) for chance in [0.9, 1.0, 1.1, 1.2, 1.3]]

disable_daze = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.NEGATIVE,
    duration=2,
    apply_once=True,
    has_description=False,
    buff_ids=(
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
            stat_sub_type=STDisableCombatSkillAttribute.DAZE,
            has_description=False,
        ),
    )
)

unstealth = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    unstealth=True,
    kill_enemy_types=MonsterType.CORPSE
)

heal_stresses = [Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    heal_stress=i,
    apply_once=True
) for i in [10, 20, 40]]

skill_1_tooltip = TooltipEffect(
    effect_name=auto_name.new_effect(),
    buff_name=auto_name.new_buff(),
    sub_name=auto_name.new_sub_type(),
    tooltip_text=f"使用下限：1点{buff('魔力值')}\n"
                 f"使用后清空{buff('魔力值')}且下回合无法移动"
)
skill_2_tooltip = TooltipEffect(
    effect_name=auto_name.new_effect(),
    buff_name=auto_name.new_buff(),
    sub_name=auto_name.new_sub_type(),
    tooltip_text=f"使用下限：2点{buff('魔力值')}\n"
                 f"使用后清空{buff('魔力值')}且下回合无法移动"
)
skill_3_tooltip = TooltipEffect(
    effect_name=auto_name.new_effect(),
    buff_name=auto_name.new_buff(),
    sub_name=auto_name.new_sub_type(),
    tooltip_text=f"使用下限：4点{buff('魔力值')}\n"
                 f"使用后清空{buff('魔力值')}且下回合无法移动"
)

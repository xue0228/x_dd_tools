from buffs import *
from xddtools.effects import Effect
from xddtools.enums import EffectTarget, CurioResultType, QuirkType, BuffSource

effect_x_1 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    damage_low_multiply=0.25,
    damage_high_multiply=0.25,
    crit_chance_add=0.05,
    speed_rating_add=2,
    duration=3
)

effect_x_2 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    damage_low_multiply=0.25,
    damage_high_multiply=0.25,
    duration=1
)

effect_x_3 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    damage_low_multiply=0.5,
    damage_high_multiply=0.5,
    duration=1
)

effect_x_4 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    damage_low_multiply=1,
    damage_high_multiply=1,
    duration=1
)

effect_x_5 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.NEGATIVE,
    duration=3,
    buff_ids=(dmg_ln25, dmg_hn25)
)

effect_x_6 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    crit_chance_add=0.05,
    duration=1
)

effect_x_7 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    attack_rating_add=0.05,
    duration=2
)

effect_x_8 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    crit_chance_add=1.0,
    duration=1
)

effect_y_1 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.NEGATIVE,
    duration=3,
    buff_ids=(dmgrp_25,)
)

effect_y_2 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER_GROUP,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    protection_rating_add=0.1,
    duration=1
)

effect_y_3 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    dot_hp_heal=1,
    duration=3,
    apply_once=True
)

effect_y_4 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    health_damage_blocks=1,
    apply_once=True
)

effect_y_5 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    health_damage_blocks=1,
    apply_once=True
)

effect_z_1 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    duration=1,
    buff_ids=(stun_10_zhang,)
)

effect_z_2 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    duration=1,
    buff_ids=(bleed_20_zhang,)
)

effect_z_3 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    duration=1,
    buff_ids=(poison_20_zhang,)
)

effect_z_4 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    unstun=True,
    cure=True,
    apply_once=True
)

effect_m_1 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER_GROUP,
    curio_result_type=CurioResultType.POSITIVE,
    heal_stress=3,
    apply_once=True
)

effect_m_2 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER_GROUP,
    curio_result_type=CurioResultType.POSITIVE,
    heal=2,
    apply_once=True
)

effect_m_3 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET_ENEMY_GROUP,
    curio_result_type=CurioResultType.NEGATIVE,
    duration=1,
    apply_once=True,
    buff_ids=(dis_stress,)
)

effect_m_4 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    defense_rating_add=0.05,
    duration=1
)

effect_m_5 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    heal=1,
    apply_once=True
)

effect_m_6 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    heal=1,
    apply_once=True
)

effect_o_1 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    damage_low_multiply=0.05,
    damage_high_multiply=0.05,
    duration=3,
    apply_once=True
)

effect_o_2 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    attack_rating_add=0.05,
    duration=3,
    apply_once=True
)

effect_o_3 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    crit_chance_add=0.02,
    duration=3,
    apply_once=True
)

effect_o_4 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    speed_rating_add=2,
    duration=3,
    apply_once=True
)

effect_o_5 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    protection_rating_add=0.05,
    duration=3,
    apply_once=True
)

effect_o_6 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    clear_debuff=True,
    untag=True,
    apply_once=True
)

effect_o_7 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    disease=QuirkType.POSITIVE_LUMINOUS
)

effect_o_8 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    disease=QuirkType.POSITIVE_CORVIDS_GRACE
)

effect_o_9 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET,
    curio_result_type=CurioResultType.POSITIVE,
    disease=QuirkType.POSITIVE_CORVIDS_EYE
)

effect_n_1 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    buff_source_type=BuffSource.ITEM,
    buff_ids=(
        dmg_l2_gu, dmg_h2_gu, crit_1_gu, stress_2_gu
    )
)

effect_n_2 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    heal_stress=1,
    heal=1,
    apply_once=True
)

effect_n_3 = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.TARGET_ENEMY_GROUP,
    curio_result_type=CurioResultType.NEGATIVE,
    buff_ids=(dmgrp_50_gu,),
    duration=1,
    apply_once=True
)
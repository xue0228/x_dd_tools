from buffs import *
from xddtools.entries import Effect
from xddtools.enum import EffectTarget, QuirkType

effect_x_1 = Effect(
    target=EffectTarget.TARGET,
    combat_stat_buff=True,
    damage_low_multiply=0.25,
    damage_high_multiply=0.25,
    crit_chance_add=0.05,
    speed_rating_add=2,
    duration=3
)

effect_x_2 = Effect(
    target=EffectTarget.TARGET,
    combat_stat_buff=True,
    damage_low_multiply=0.25,
    damage_high_multiply=0.25,
    duration=1
)

effect_x_3 = Effect(
    target=EffectTarget.TARGET,
    combat_stat_buff=True,
    damage_low_multiply=0.5,
    damage_high_multiply=0.5,
    duration=1
)

effect_x_4 = Effect(
    target=EffectTarget.TARGET,
    combat_stat_buff=True,
    damage_low_multiply=1,
    damage_high_multiply=1,
    duration=1
)

effect_x_5 = Effect(
    target=EffectTarget.PERFORMER,
    duration=3,
    buff_ids=[dmg_ln25, dmg_hn25],
    apply_once=True
)

effect_x_6 = Effect(
    target=EffectTarget.PERFORMER,
    combat_stat_buff=True,
    crit_chance_add=0.05,
    duration=1,
    apply_once=True
)

effect_x_7 = Effect(
    target=EffectTarget.TARGET,
    combat_stat_buff=True,
    attack_rating_add=0.15,
    duration=2
)

effect_x_8 = Effect(
    target=EffectTarget.PERFORMER,
    combat_stat_buff=True,
    crit_chance_add=1,
    duration=1,
    apply_once=True
)

effect_y_1 = Effect(
    target=EffectTarget.TARGET,
    duration=3,
    buff_ids=[dmgrp_25]
)

effect_y_2 = Effect(
    target=EffectTarget.PERFORMER_GROUP,
    combat_stat_buff=True,
    protection_rating_add=0.1,
    duration=3,
    apply_once=True
)

effect_y_3 = Effect(
    target=EffectTarget.PERFORMER,
    dot_hp_heal=1,
    duration=3,
    apply_once=True
)

effect_y_4 = Effect(
    target=EffectTarget.TARGET,
    health_damage_blocks=1
)

effect_y_5 = Effect(
    target=EffectTarget.PERFORMER,
    health_damage_blocks=1,
    apply_once=True
)

effect_z_1 = Effect(
    target=EffectTarget.TARGET,
    duration=1,
    buff_ids=[stun_10_zhang]
)

effect_z_2 = Effect(
    target=EffectTarget.TARGET,
    duration=1,
    buff_ids=[bleed_20_zhang]
)

effect_z_3 = Effect(
    target=EffectTarget.TARGET,
    duration=1,
    buff_ids=[poison_20_zhang]
)

effect_z_4 = Effect(
    target=EffectTarget.TARGET,
    unstun=True,
    cure=True
)

effect_z_5 = Effect(
    target=EffectTarget.PERFORMER,
    apply_once=True,
    duration=1,
    buff_ids=[stun_100]
)

effect_m_1 = Effect(
    target=EffectTarget.PERFORMER_GROUP,
    heal_stress=3,
    apply_once=True
)

effect_m_2 = Effect(
    target=EffectTarget.PERFORMER_GROUP,
    heal=2,
    apply_once=True
)

effect_m_3 = Effect(
    target=EffectTarget.TARGET_ENEMY_GROUP,
    duration=1,
    apply_once=True,
    buff_ids=[dis_stress]
)

effect_m_4 = Effect(
    target=EffectTarget.PERFORMER,
    combat_stat_buff=True,
    defense_rating_add=0.05,
    duration=1,
    apply_once=True
)

effect_m_5 = Effect(
    target=EffectTarget.PERFORMER,
    heal=1,
    apply_once=True
)

effect_m_6 = Effect(
    target=EffectTarget.TARGET,
    heal=3
)

effect_o_1 = Effect(
    target=EffectTarget.TARGET,
    combat_stat_buff=True,
    damage_low_multiply=0.05,
    damage_high_multiply=0.05,
    duration=3
)

effect_o_2 = Effect(
    target=EffectTarget.TARGET,
    combat_stat_buff=True,
    attack_rating_add=0.05,
    duration=3
)

effect_o_3 = Effect(
    target=EffectTarget.TARGET,
    combat_stat_buff=True,
    crit_chance_add=0.02,
    duration=3
)

effect_o_4 = Effect(
    target=EffectTarget.TARGET,
    combat_stat_buff=True,
    speed_rating_add=2,
    duration=3
)

effect_o_5 = Effect(
    target=EffectTarget.TARGET,
    combat_stat_buff=True,
    protection_rating_add=0.05,
    duration=3
)

effect_o_6 = Effect(
    target=EffectTarget.TARGET,
    clear_debuff=True,
    untag=True
)

effect_o_7 = Effect(
    target=EffectTarget.TARGET,
    disease=QuirkType.POSITIVE_LUMINOUS
)

effect_o_8 = Effect(
    target=EffectTarget.TARGET,
    disease=QuirkType.POSITIVE_CORVIDS_GRACE
)

effect_o_9 = Effect(
    target=EffectTarget.TARGET,
    disease=QuirkType.POSITIVE_CORVIDS_EYE
)

effect_n_1 = Effect(
    target=EffectTarget.PERFORMER,
    buff_duration_type=BuffDurationType.COMBAT_END,
    duration=1,
    buff_ids=[
        dmg_h_gui, dmg_l_gui, crit_gui, dmg_rec_gui, crit_rec_gui
    ]
)

effect_n_2 = Effect(
    target=EffectTarget.PERFORMER,
    heal_stress=1,
    heal=1,
    apply_once=True
)

effect_n_3 = Effect(
    target=EffectTarget.TARGET_ENEMY_GROUP,
    duration=1,
    apply_once=True,
    buff_ids=[dmg_rec_33]
)

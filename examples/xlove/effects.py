from xddtools.entries import Effect
from xddtools.enum import EffectTarget
from buffs import *

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
    crit_chance_add=0.15,
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

from xddtools.entries import Buff, BuffRule
from xddtools.enum import BuffType, STCombatStatMultiply, STCombatStatAdd, BuffRuleType, BuffDurationType

dmg_l3 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=0.03
)

dmg_h3 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=0.03
)

dmg_l4 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=0.04
)

dmg_h4 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=0.04
)

dmg_l5 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=0.05
)

dmg_h5 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=0.05
)

dmg_l8 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=0.08
)

dmg_h8 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=0.08
)

dmg_ln25 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=-0.25,
    is_clear_debuff_valid=False
)

dmg_hn25 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=-0.25,
    is_clear_debuff_valid=False
)

acc_1 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.ATTACK_RATING,
    amount=0.01
)

acc_2 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.ATTACK_RATING,
    amount=0.02
)

acc_3 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.ATTACK_RATING,
    amount=0.03
)

acc_5 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.ATTACK_RATING,
    amount=0.05
)

crit_1 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
    amount=0.01
)

crit_2 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
    amount=0.02
)

crit_3 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
    amount=0.03
)

crit_5 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
    amount=0.05
)

def_1 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
    amount=0.01
)

def_2 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
    amount=0.02
)

def_3 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
    amount=0.03
)

def_5 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
    amount=0.05
)

spd_1 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.SPEED_RATING,
    amount=1
)

spd_2 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.SPEED_RATING,
    amount=2
)

spd_3 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.SPEED_RATING,
    amount=3
)

prot_10 = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.PROTECTION_RATING,
    amount=0.1
)

buff_x_1 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=9.99,
    buff_rule=BuffRule(
        rule_type=BuffRuleType.TARGET_HP_BELOW,
        rule_data_float=0.08
    )
)

buff_x_2 = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=9.99,
    buff_rule=BuffRule(
        rule_type=BuffRuleType.TARGET_HP_BELOW,
        rule_data_float=0.08
    )
)

buff_x_3 = Buff(
    stat_type=BuffType.IGNORE_PROTECTION,
    amount=0.2
)

buff_y_1 = Buff(
    stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
    amount=-0.1
)

buff_y_2 = Buff(
    stat_type=BuffType.HP_DOT_HEAL,
    amount=1
)

dmgrp_25 = Buff(
    stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
    amount=0.25,
    is_clear_debuff_valid=False
)

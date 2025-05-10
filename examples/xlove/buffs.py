from xddtools.entries import Buff, BuffRule
from xddtools.enum import BuffType, STCombatStatMultiply, STCombatStatAdd, BuffRuleType, BuffDurationType, \
    STDisableCombatSkillAttribute

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
    amount=1,
    duration_type=BuffDurationType.QUEST_END,
    duration=1,
    remove_if_not_active=True
)

dmgrp_25 = Buff(
    stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
    amount=0.25,
    is_clear_debuff_valid=False
)

stun_10_zhang = Buff(
    stat_type=BuffType.STUN_CHANCE,
    amount=0.1
)

bleed_20_zhang = Buff(
    stat_type=BuffType.HP_DOT_BLEED_AMOUNT_PERCENT,
    amount=0.2
)

poison_20_zhang = Buff(
    stat_type=BuffType.HP_DOT_POISON_AMOUNT_PERCENT,
    amount=0.2
)

bleed_10 = Buff(
    stat_type=BuffType.BLEED_CHANCE,
    amount=0.1
)

poison_10 = Buff(
    stat_type=BuffType.POISON_CHANCE,
    amount=0.1
)

stun_10_first = Buff(
    stat_type=BuffType.STUN_CHANCE,
    amount=0.1,
    buff_rule=BuffRule(
        rule_type=BuffRuleType.ACTIVATED_FIRST
    )
)

bleed_10_first = Buff(
    stat_type=BuffType.BLEED_CHANCE,
    amount=0.1,
    buff_rule=BuffRule(
        rule_type=BuffRuleType.ACTIVATED_FIRST
    )
)

poison_10_first = Buff(
    stat_type=BuffType.POISON_CHANCE,
    amount=0.1,
    buff_rule=BuffRule(
        rule_type=BuffRuleType.ACTIVATED_FIRST
    )
)

speed_2_first = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.SPEED_RATING,
    amount=2,
    buff_rule=BuffRule(
        rule_type=BuffRuleType.FIRST_ROUND_ONLY
    )
)

stun_100 = Buff(
    stat_type=BuffType.STUN_CHANCE,
    amount=1
)

dis_stress = Buff(
    stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
    stat_sub_type=STDisableCombatSkillAttribute.STRESS
)

buff_m_1 = Buff(
    stat_type=BuffType.HP_HEAL_PERCENT,
    amount=0.1
)

buff_m_2 = Buff(
    stat_type=BuffType.STRESS_HEAL_PERCENT,
    amount=0.1
)

buff_m_3 = Buff(
    stat_type=BuffType.HP_HEAL_DOT_AMOUNT_PERCENT,
    amount=0.2
)

buff_m_4 = Buff(
    stat_type=BuffType.HP_HEAL_PERCENT,
    amount=0.33,
    buff_rule=BuffRule(
        rule_type=BuffRuleType.TARGET_HP_BELOW,
        rule_data_float=0.05
    )
)

buff_m_5 = Buff(
    stat_type=BuffType.STRESS_HEAL_PERCENT,
    amount=0.33,
    buff_rule=BuffRule(
        rule_type=BuffRuleType.TARGET_HP_BELOW,
        rule_data_float=0.05
    )
)

buff_m_6 = Buff(
    stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
    amount=-0.2
)

buff_o_1 = Buff(
    stat_type=BuffType.DEBUFF_CHANCE,
    amount=0.1
)

buff_o_2 = Buff(
    stat_type=BuffType.MOVE_CHANCE,
    amount=0.1
)

buff_o_3 = Buff(
    stat_type=BuffType.RESOLVE_CHECK_PERCENT,
    amount=0.1
)

buff_n_1 = Buff(
    stat_type=BuffType.HEARTATTACK_STRESS_HEAL_PERCENT,
    amount=200
)

buff_n_2 = Buff(
    stat_type=BuffType.GUARD_BLOCKED
)

dmg_h_gui = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=0.1,
    duration_type=BuffDurationType.COMBAT_END,
    duration=1
)

dmg_l_gui = Buff(
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=0.1
)

crit_gui = Buff(
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
    amount=0.05
)

dmg_rec_gui = Buff(
    stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
    amount=0.1,
    is_clear_debuff_valid=False
)

crit_rec_gui = Buff(
    stat_type=BuffType.CRIT_RECEIVED_CHANCE,
    amount=0.05,
    is_clear_debuff_valid=False
)

dmg_rec_33 = Buff(
    stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
    amount=0.33
)

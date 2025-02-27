from xddtools.buff_rules import BRActivatedFirst, BRTargetHpBelow
from xddtools.buffs import Buff
from xddtools.enums import BuffType, STCombatStatMultiply, BuffDurationType, STCombatStatAdd, \
    STDisableCombatSkillAttribute
from xddtools.name import AutoName

MOD_NAME = "xlove_token"

auto_name = AutoName(MOD_NAME)

dmg_l3 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=0.03,
    has_description=False,
    remove_if_not_active=False,
)

dmg_h3 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=0.03,
    has_description=False,
    remove_if_not_active=False,
)

dmg_l4 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=0.04,
    has_description=False,
    remove_if_not_active=False,
)

dmg_h4 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=0.04,
    has_description=False,
    remove_if_not_active=False,
)

dmg_l5 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=0.05,
    has_description=False,
    remove_if_not_active=False,
)

dmg_h5 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=0.05,
    has_description=False,
    remove_if_not_active=False,
)

dmg_l8 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=0.08,
    has_description=False,
    remove_if_not_active=False,
)

dmg_h8 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=0.08,
    has_description=False,
    remove_if_not_active=False,
)

dmg_ln25 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=-0.25,
    is_clear_debuff_valid=False,
    remove_if_not_active=False,
)

dmg_hn25 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=-0.25,
    is_clear_debuff_valid=False,
    remove_if_not_active=False,
)

acc_1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.ATTACK_RATING,
    amount=0.01,
    has_description=False,
    remove_if_not_active=False,
)

acc_2 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.ATTACK_RATING,
    amount=0.02,
    has_description=False,
    remove_if_not_active=False,
)

acc_3 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.ATTACK_RATING,
    amount=0.03,
    has_description=False,
    remove_if_not_active=False,
)

acc_5 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.ATTACK_RATING,
    amount=0.05,
    has_description=False,
    remove_if_not_active=False,
)

crit_1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
    amount=0.01,
    has_description=False,
    remove_if_not_active=False,
)

crit_2 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
    amount=0.02,
    has_description=False,
    remove_if_not_active=False,
)

crit_3 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
    amount=0.03,
    has_description=False,
    remove_if_not_active=False,
)

crit_5 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
    amount=0.05,
    has_description=False,
    remove_if_not_active=False,
)

def_1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
    amount=0.01,
    has_description=False,
    remove_if_not_active=False,
)

def_2 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
    amount=0.02,
    has_description=False,
    remove_if_not_active=False,
)

def_3 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
    amount=0.03,
    has_description=False,
    remove_if_not_active=False,
)

def_5 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
    amount=0.05,
    has_description=False,
    remove_if_not_active=False,
)

spd_1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.SPEED_RATING,
    amount=1,
    has_description=False,
    remove_if_not_active=False,
)

spd_2 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.SPEED_RATING,
    amount=2,
    has_description=False,
    remove_if_not_active=False,
)

spd_3 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.SPEED_RATING,
    amount=3,
    has_description=False,
    remove_if_not_active=False,
)

prot_10 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.PROTECTION_RATING,
    amount=0.10,
    has_description=False,
    remove_if_not_active=False,
)

buff_x_1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=9.99,
    has_description=False,
    remove_if_not_active=False,
    buff_rule=BRTargetHpBelow(0.08)
)

buff_x_2 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=9.99,
    has_description=False,
    remove_if_not_active=False,
    buff_rule=BRTargetHpBelow(0.08)
)

buff_x_3 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.IGNORE_PROTECTION,
    amount=0.20,
    has_description=False,
    remove_if_not_active=False,
)

buff_y_1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
    amount=-0.10,
    has_description=False,
    remove_if_not_active=False,
)

buff_y_2 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.HP_DOT_HEAL,
    amount=1,
    has_description=False,
    remove_if_not_active=False,
    duration_type=BuffDurationType.QUEST_END,
    duration=1,
)

stun_10 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.STUN_CHANCE,
    amount=0.1,
    has_description=False,
    remove_if_not_active=False,
)

bleed_10 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.BLEED_CHANCE,
    amount=0.1,
    has_description=False,
    remove_if_not_active=False,
)

poison_10 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.POISON_CHANCE,
    amount=0.1,
    has_description=False,
    remove_if_not_active=False,
)

stun_10_zhang = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.STUN_CHANCE,
    amount=0.1,
    remove_if_not_active=False,
)

stun_10_first = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.STUN_CHANCE,
    amount=0.1,
    has_description=False,
    remove_if_not_active=False,
    buff_rule=BRActivatedFirst(),
)

bleed_10_first = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.BLEED_CHANCE,
    amount=0.1,
    has_description=False,
    remove_if_not_active=False,
    buff_rule=BRActivatedFirst(),
)

poison_10_first = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.POISON_CHANCE,
    amount=0.1,
    has_description=False,
    remove_if_not_active=False,
    buff_rule=BRActivatedFirst(),
)

buff_z = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.SPEED_RATING,
    amount=2,
    has_description=False,
    remove_if_not_active=False,
)

buff_m_1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.HP_HEAL_PERCENT,
    amount=0.10,
    has_description=False,
    remove_if_not_active=False,
)

buff_m_2 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.STRESS_HEAL_PERCENT,
    amount=0.10,
    has_description=False,
    remove_if_not_active=False,
)

buff_m_3 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.HP_HEAL_DOT_AMOUNT_PERCENT,
    amount=0.20,
    has_description=False,
    remove_if_not_active=False,
)

buff_m_4 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.HP_HEAL_PERCENT,
    amount=0.33,
    has_description=False,
    remove_if_not_active=False,
    buff_rule=BRTargetHpBelow(0.05)
)

buff_m_5 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.STRESS_HEAL_PERCENT,
    amount=0.33,
    has_description=False,
    remove_if_not_active=False,
    buff_rule=BRTargetHpBelow(0.05)
)

buff_m_6 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
    amount=-0.20,
    has_description=False,
    remove_if_not_active=False,
)

buff_o_1 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.DEBUFF_CHANCE,
    amount=0.1,
    has_description=False,
    remove_if_not_active=False,
)

buff_o_2 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.MOVE_CHANCE,
    amount=0.1,
    has_description=False,
    remove_if_not_active=False,
)

buff_o_3 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.RESOLVE_CHECK_PERCENT,
    amount=0.1,
    has_description=False,
    remove_if_not_active=False,
)

buff_n = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.HEARTATTACK_STRESS_HEAL_PERCENT,
    amount=9999,
    has_description=False,
    remove_if_not_active=False,
)

dmgrp_25 = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
    amount=0.25,
    is_clear_debuff_valid=False,
    remove_if_not_active=False,
)

dis_stress = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
    stat_sub_type=STDisableCombatSkillAttribute.STRESS,
    remove_if_not_active=False,
)

bleed_20_zhang = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.HP_DOT_BLEED_AMOUNT_PERCENT,
    amount=0.2,
    remove_if_not_active=False,
)

poison_20_zhang = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.HP_DOT_POISON_AMOUNT_PERCENT,
    amount=0.2,
    remove_if_not_active=False,
)

dmg_l2_gu = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
    amount=0.02,
    duration_type=BuffDurationType.QUEST_END,
    duration=1,
    remove_if_not_active=False,
)

dmg_h2_gu = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_MULTIPLY,
    stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
    amount=0.02,
    duration_type=BuffDurationType.QUEST_END,
    duration=1,
    remove_if_not_active=False,
)

crit_1_gu = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.COMBAT_STAT_ADD,
    stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
    amount=0.01,
    duration_type=BuffDurationType.QUEST_END,
    duration=1,
    remove_if_not_active=False,
)

stress_2_gu = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
    amount=0.02,
    duration_type=BuffDurationType.QUEST_END,
    duration=1,
    is_clear_debuff_valid=False,
)

dmgrp_50_gu = Buff(
    buff_name=auto_name.new_buff(),
    stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
    amount=0.5,
    remove_if_not_active=False
)

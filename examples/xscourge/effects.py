from constants import skill_b1, skill_b2, skill_b3, skill_a1, skill_a2, skill_a3
from modes import modes_a, mode_c
from quirks import quirk
from xddtools.entries import Effect, Buff, BuffRule, ActorDot, DurationElement, Animation
from xddtools.entries.colour import bleed, buff, mark, heal_hp, riposte, stress, move, stun, blight
from xddtools.enum import EffectTarget, BuffType, STCombatStatAdd, STCombatStatMultiply, BuffRuleType, \
    STDisableCombatSkillAttribute, BuffDurationType, BuffSource, CurioResultType, KeyStatus, STResistance, \
    ActorDotUpdateDurationType, ActorStatus
from xddtools.magic import get_set_mode_effect, get_str_tooltip_effect, get_cd_tag_effect, get_number_tooltip_buff, \
    get_clear_self_buff_source_effect, get_cd_charge_effect, CDCharge, get_suck_blood_effects
from xddtools.utils import float_to_percent_int

change_modes_a = [get_set_mode_effect(
    mode=mode,
    has_description=False,
    on_hit=True,
    on_miss=False,
    order=4
) for mode in modes_a]
change_mode_c = get_set_mode_effect(mode_c)
change_mode_a0 = get_set_mode_effect(modes_a[0])
change_mode_a0_no_description = get_set_mode_effect(modes_a[0], has_description=False)

effect_crit = Effect(
    target=EffectTarget.PERFORMER,
    skill_instant=True,
    has_description=False,
    buff_ids=[
        Buff(
            stat_type=BuffType.COMBAT_STAT_ADD,
            stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
            amount=2
        )
    ]
)
effect_stun = Effect(
    target=EffectTarget.TARGET,
    chance=1.4,
    has_description=False,
    stun=1
)
effect_kill = Effect(
    target=EffectTarget.PERFORMER,
    skill_instant=True,
    has_description=False,
    apply_once=True,
    buff_ids=[
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
            amount=100,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.TARGET_HP_BELOW,
                rule_data_float=0.25
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
            amount=100,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.TARGET_HP_BELOW,
                rule_data_float=0.25
            )
        )
    ]
)

effect_a = Effect(
    target=EffectTarget.PERFORMER,
    apply_once=True,
    has_description=False,
    buff_ids=[
        Buff(
            stat_type=BuffType.DEBUFF_CHANCE,
            amount=0.2,
            duration=2,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.SKILL,
                rule_data_string=skill_b1,
                rule_data_string_tooltip="月尘"
            )
        ),
        Buff(
            stat_type=BuffType.DEBUFF_CHANCE,
            amount=0.2,
            duration=2,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.SKILL,
                rule_data_string=skill_b2,
                rule_data_string_tooltip="新月"
            )
        ),
        Buff(
            stat_type=BuffType.BLEED_CHANCE,
            amount=0.1,
            duration=1,
            duration_type=BuffDurationType.COMBAT_END,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.SKILL,
                rule_data_string=skill_b3,
                rule_data_string_tooltip="律令：痛苦"
            )
        ),
        Buff(
            stat_type=BuffType.POISON_CHANCE,
            amount=0.1,
            duration=1,
            duration_type=BuffDurationType.COMBAT_END,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.SKILL,
                rule_data_string=skill_b3,
                rule_data_string_tooltip="律令：痛苦"
            )
        )
    ]
)
effect_b = Effect(
    target=EffectTarget.PERFORMER,
    apply_once=True,
    has_description=False,
    buff_ids=[
        Buff(
            stat_type=BuffType.COMBAT_STAT_ADD,
            stat_sub_type=STCombatStatAdd.ATTACK_RATING,
            amount=0.1,
            duration=2,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.SKILL,
                rule_data_string=skill_a1,
                rule_data_string_tooltip="耀斑"
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_ADD,
            stat_sub_type=STCombatStatAdd.ATTACK_RATING,
            amount=0.1,
            duration=2,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.SKILL,
                rule_data_string=skill_a2,
                rule_data_string_tooltip="日蚀"
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_ADD,
            stat_sub_type=STCombatStatAdd.ATTACK_RATING,
            amount=0.05,
            duration=1,
            duration_type=BuffDurationType.COMBAT_END,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.SKILL,
                rule_data_string=skill_a3,
                rule_data_string_tooltip="律令：死亡"
            )
        )
    ]
)
effect_a2 = Effect(
    target=EffectTarget.PERFORMER,
    chance=0.2,
    initiative_change=1,
    apply_once=True,
    has_description=False,
    buff_ids=[
        Buff(
            stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
            stat_sub_type=STDisableCombatSkillAttribute.BLEED,
            has_description=False,
            is_clear_debuff_valid=False,
            duration=2
        )
    ]
)
effect_b2 = Effect(
    target=EffectTarget.PERFORMER,
    chance=0.2,
    initiative_change=1,
    apply_once=True,
    has_description=False,
    buff_ids=[
        Buff(
            stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
            stat_sub_type=STDisableCombatSkillAttribute.POISON,
            has_description=False,
            is_clear_debuff_valid=False,
            duration=2
        )
    ]
)

effects_c1 = [Effect(
    target=EffectTarget.PERFORMER_GROUP_OTHER,
    has_description=False,
    chance=100,
    apply_once=True,
    on_hit=False,
    on_miss=True,
    health_damage=5 + i
) for i in range(5)]
effects_c2 = [Effect(
    target=EffectTarget.TARGET_GROUP,
    has_description=False,
    chance=100,
    apply_once=True,
    on_hit=False,
    on_miss=True,
    health_damage=5 + i
) for i in range(5)]
effects_c_tooltip = [get_str_tooltip_effect(f"未命中：对所有其他角色造成{5 + i}点真实伤害") for i in range(5)]
effect_c3 = Effect(
    target=EffectTarget.PERFORMER,
    duration=1,
    apply_once=True,
    buff_duration_type=BuffDurationType.COMBAT_END,
    buff_source_type=BuffSource.NEVER_AGAIN,
    buff_ids=[
        Buff(
            stat_type=BuffType.COMBAT_STAT_ADD,
            stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
            amount=-0.3
        )
    ]
)

effect_quirk = Effect(
    target=EffectTarget.PERFORMER,
    chance=100,
    disease=quirk,
    apply_once=True,
    has_description=False
)

poison_cd = get_cd_tag_effect(STDisableCombatSkillAttribute.POISON)
bleed_cd = get_cd_tag_effect(STDisableCombatSkillAttribute.BLEED)
daze_cd = get_cd_tag_effect(STDisableCombatSkillAttribute.DAZE)

num_buff_p1 = get_number_tooltip_buff(text="恐惧值：%d", amount=1)
num_buff_p2 = get_number_tooltip_buff(amount=2, keep_last_sub_type=True)
clear_charge = get_clear_self_buff_source_effect()
charge_p1 = get_cd_charge_effect(
    cd_charges=[CDCharge(disable=STDisableCombatSkillAttribute.DAZE, amount=-1)],
    buff_duration_type=BuffDurationType.COMBAT_END,
    other_buffs=[
        num_buff_p1,
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.MAX_HP,
            amount=0.5,
            has_description=False,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.IN_MODE,
                rule_data_string=mode_c,
                rule_data_string_tooltip="极巨化"
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_ADD,
            stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
            amount=0.4,
            has_description=False,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.IN_MODE,
                rule_data_string=mode_c
            )
        )
    ]
)
charge_p2 = get_cd_charge_effect(
    cd_charges=[CDCharge(disable=STDisableCombatSkillAttribute.DAZE, amount=-2)],
    buff_duration_type=BuffDurationType.COMBAT_END,
    other_buffs=[
        num_buff_p2,
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.MAX_HP,
            amount=1,
            has_description=False,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.IN_MODE,
                rule_data_string=mode_c
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_ADD,
            stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
            amount=0.8,
            has_description=False,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.IN_MODE,
                rule_data_string=mode_c
            )
        )
    ]
)

tooltip_effect_1 = get_str_tooltip_effect(f"攻击命中：获得1点{bleed('末日充能')}\n攻击：获得1点{stress('恐惧值')}")
tooltip_effect_2 = get_str_tooltip_effect(f"攻击命中：获得2点{bleed('末日充能')}\n攻击：获得2点{stress('恐惧值')}")
tooltip_effect_3 = get_str_tooltip_effect(f"攻击命中：强化另一武器/小概率触发{buff('连携')}")
tooltip_effect_4 = get_str_tooltip_effect(f"{bleed('末日充能')}：对{mark('标记')}最大攻击力+30%%/60%%/90%%/120%%")
tooltip_effect_5 = get_str_tooltip_effect(f"{bleed('末日充能')}：{heal_hp('生命偷取')}+20%%/30%%/40%%/50%%")
tooltip_effect_6 = get_str_tooltip_effect(f"{bleed('末日充能')}：队伍攻击力+0/1/2/3")
tooltip_effect_7 = get_str_tooltip_effect(f"{bleed('末日充能')}：队伍闪避+0/3/6/9")
tooltip_effect_8 = get_str_tooltip_effect(f"{riposte('反击')}命中额外获得1回合")
tooltip_effect_9 = get_str_tooltip_effect(f"{bleed('恐惧值')}大于等于3时可用")
tooltip_effect_10 = get_str_tooltip_effect(f"每1点{bleed('恐惧值')}提升50%%{heal_hp('最大生命')}/40%%暴击率")
tooltip_effect_11 = get_str_tooltip_effect(f"{move('扰乱')}双方")

# skill_1
effects_tag = [Effect(
    target=EffectTarget.PERFORMER,
    has_description=False,
    apply_once=True,
    curio_result_type=CurioResultType.POSITIVE,
    combat_stat_buff=True,
    key_status=KeyStatus.TAGGED,
    damage_high_multiply=0.3 * (i + 1),
    damage_low_multiply=0.3 * (i + 1)
) for i in range(4)]

# skill_2
effects_suck_blood = [
    get_suck_blood_effects(0.20 + i * 0.10, has_description=False)[0]
    for i in range(4)
]

# skill_3
effects_protection = [Effect(
    target=EffectTarget.TARGET,
    chance=0.9 + i * 0.1,
    combat_stat_buff=True,
    duration=3,
    protection_rating_add=-0.1 - i * 0.02 if i < 4 else -0.2
) for i in range(5)]
effects_damage_add = [Effect(
    target=EffectTarget.PERFORMER_GROUP,
    has_description=False,
    apply_once=True,
    curio_result_type=CurioResultType.POSITIVE,
    # buff_duration_type=BuffDurationType.COMBAT_END,
    duration=3,
    buff_ids=[
        Buff(
            stat_type=BuffType.COMBAT_STAT_ADD,
            stat_sub_type=STCombatStatAdd.DAMAGE_LOW,
            amount=1 + i
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_ADD,
            stat_sub_type=STCombatStatAdd.DAMAGE_HIGH,
            amount=1 + i
        )
    ]
) for i in range(3)]

# skill_4
effects_defence = [Effect(
    target=EffectTarget.TARGET,
    chance=0.9 + i * 0.1,
    combat_stat_buff=True,
    duration=3,
    defense_rating_add=-0.15 + i * 0.01 if i < 4 else -0.2
) for i in range(5)]
effects_drp = [Effect(
    target=EffectTarget.TARGET,
    chance=0.9 + i * 0.1,
    duration=1,
    buff_ids=[
        Buff(
            stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
            amount=0.1 + i * 0.02 if i < 4 else 0.2
        )
    ]
) for i in range(5)]
effects_defence_add = [Effect(
    target=EffectTarget.PERFORMER_GROUP,
    has_description=False,
    apply_once=True,
    curio_result_type=CurioResultType.POSITIVE,
    duration=3,
    buff_ids=[
        Buff(
            stat_type=BuffType.COMBAT_STAT_ADD,
            stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
            amount=0.03 + i * 0.03
        )
    ]
) for i in range(3)]

# skill_5
effects_crc = [Effect(
    target=EffectTarget.TARGET,
    chance=1 + i * 0.1,
    duration=1,
    buff_ids=[
        Buff(
            stat_type=BuffType.CRIT_RECEIVED_CHANCE,
            amount=0.2 + i * 0.02 if i < 4 else 0.3
        )
    ]
) for i in range(5)]
effects_disable_stress = [Effect(
    target=EffectTarget.TARGET,
    chance=0.9 + i * 0.1,
    duration=1,
    buff_ids=[
        Buff(
            stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
            stat_sub_type=STDisableCombatSkillAttribute.STRESS
        )
    ]
) for i in range(5)]
effect_riposte = Effect(
    target=EffectTarget.PERFORMER,
    apply_once=True,
    duration=3,
    riposte=True,
    riposte_on_hit_chance_add=1,
    riposte_on_miss_chance_add=1
)
effect_tag_self = Effect(
    target=EffectTarget.PERFORMER,
    tag=True,
    duration=2,
    apply_once=True
)
effect_no_crit = Effect(
    target=EffectTarget.PERFORMER,
    duration=2,
    buff_ids=[
        Buff(
            stat_type=BuffType.CRIT_RECEIVED_CHANCE,
            amount=-1
        )
    ],
    apply_once=True
)
effects_heal_stress = [Effect(
    target=EffectTarget.PERFORMER_GROUP,
    chance=0.5 + i * 0.02 if i < 4 else 0.6,
    heal_stress=2 + i,
    apply_once=True
) for i in range(5)]

# skill_6
effect_huge = Effect(
    target=EffectTarget.PERFORMER,
    buff_source_type=BuffSource.NEVER_AGAIN,
    duration=1,
    buff_duration_type=BuffDurationType.COMBAT_END,
    apply_once=True,
    buff_ids=[
        Buff(
            stat_type=BuffType.COMBAT_STAT_ADD,
            stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
            amount=1
        ),
        Buff(
            stat_type=BuffType.RESISTANCE,
            stat_sub_type=STResistance.STUN,
            amount=1
        ),
        Buff(
            stat_type=BuffType.RESISTANCE,
            stat_sub_type=STResistance.MOVE,
            amount=1
        )
    ]
)
effect_heal_self = Effect(
    target=EffectTarget.PERFORMER,
    heal_percent=0.5,
    apply_once=True
)
effect_shuffle_ally = Effect(
    target=EffectTarget.PERFORMER_GROUP,
    chance=100,
    shuffle_target=True,
    apply_once=True,
    has_description=False
)
effect_shuffle_enemy = Effect(
    target=EffectTarget.TARGET_ENEMY_GROUP,
    chance=100,
    shuffle_target=True,
    apply_once=True,
    has_description=False
)
effect_clear_guard = Effect(
    target=EffectTarget.PERFORMER_GROUP,
    clear_guarded=True,
    clear_guarding=True,
    has_description=False,
    apply_once=True
)
effect_guard_ally = Effect(
    target=EffectTarget.PERFORMER_GROUP_OTHER,
    guard=True,
    duration=1,
    buff_duration_type=BuffDurationType.COMBAT_END,
    apply_once=True
)

# skill_7
effects_push = [Effect(
    target=EffectTarget.TARGET,
    chance=1 + i * 0.1,
    push=3) for i in range(5)]
effects_stun = [Effect(
    target=EffectTarget.TARGET,
    chance=1 + i * 0.1,
    stun=1) for i in range(5)]

# skill_8
effects_stun_damage = [Effect(
    target=EffectTarget.PERFORMER,
    key_status=KeyStatus.STUNNED,
    apply_once=True,
    has_description=False,
    combat_stat_buff=True,
    damage_high_multiply=0.3 + i * 0.1,
    damage_low_multiply=0.3 + i * 0.1
) for i in range(5)]
tooltip_effects_stun_damage = [
    get_str_tooltip_effect(f"对{stun('眩晕')}目标+{float_to_percent_int(0.3 + i * 0.1)}%%伤害")
    for i in range(5)
]
effects_damage = [Effect(
    target=EffectTarget.TARGET,
    chance=1 + i * 0.1,
    duration=2,
    combat_stat_buff=True,
    damage_low_multiply=-0.2 - i * 0.02 if i < 4 else -0.3,
    damage_high_multiply=-0.2 - i * 0.02 if i < 4 else -0.3
) for i in range(5)]

# skill_9
effects_pull = [Effect(
    target=EffectTarget.TARGET,
    chance=1 + i * 0.1,
    pull=3) for i in range(5)]
immobilize_dot = ActorDot(
    update_duration_type=ActorDotUpdateDurationType.AFTER_TURN_ATTACK,
    duration_elements=[
        DurationElement(completion_chance=0),
        DurationElement(completion_chance=0),
        DurationElement(completion_chance=1, completion_effects=[Effect(
            target=EffectTarget.TARGET,
            chance=100,
            unimmobilize=True
        )])
    ],
    fx=Animation(anim_dir="fx/actor_dot", need_rename=False)
)
effect_immobilize = Effect(
    target=EffectTarget.TARGET,
    chance=100,
    actor_dot=immobilize_dot,
    has_description=False,
    immobilize=True,
    duration=1,
    buff_duration_type=BuffDurationType.COMBAT_END
)
tooltip_effect_immobilize = get_str_tooltip_effect(f"{move('禁锢')}目标（3次攻击后解除）")

# skill_10
effect_heal_ally = Effect(
    target=EffectTarget.PERFORMER_GROUP,
    heal_percent=0.25,
    apply_once=True
)
effect_clear_guarding = Effect(
    target=EffectTarget.PERFORMER,
    clear_guarding=True,
    apply_once=True
)

# skill_11
effects_status_damage_add = [Effect(
    target=EffectTarget.PERFORMER,
    has_description=False,
    skill_instant=True,
    apply_once=True,
    buff_ids=[
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
            amount=0.3 + i * 0.02 if i < 4 else 0.4,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.ACTOR_STATUS,
                rule_data_string=ActorStatus.TAGGED
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
            amount=0.3 + i * 0.02 if i < 4 else 0.4,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.ACTOR_STATUS,
                rule_data_string=ActorStatus.TAGGED
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
            amount=0.3 + i * 0.02 if i < 4 else 0.4,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.ACTOR_STATUS,
                rule_data_string=ActorStatus.BLEEDING
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
            amount=0.3 + i * 0.02 if i < 4 else 0.4,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.ACTOR_STATUS,
                rule_data_string=ActorStatus.BLEEDING
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
            amount=0.3 + i * 0.02 if i < 4 else 0.4,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.ACTOR_STATUS,
                rule_data_string=ActorStatus.POISONED
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
            amount=0.3 + i * 0.02 if i < 4 else 0.4,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.ACTOR_STATUS,
                rule_data_string=ActorStatus.POISONED
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
            amount=0.3 + i * 0.02 if i < 4 else 0.4,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.ACTOR_STATUS,
                rule_data_string=ActorStatus.STUNNED
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
            amount=0.3 + i * 0.02 if i < 4 else 0.4,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.ACTOR_STATUS,
                rule_data_string=ActorStatus.STUNNED
            )
        ),
    ]
) for i in range(5)]
tooltip_effects_status_damage_add = [
    get_str_tooltip_effect(f"对{mark('标记')}/{bleed('流血')}/{blight('腐蚀')}/{stun('眩晕')}"
                           f"目标+{float_to_percent_int(0.3 + i * 0.02 if i < 4 else 0.4)}%%伤害")
    for i in range(5)
]

# skill_12
effect_tag_target = Effect(
    target=EffectTarget.TARGET,
    tag=True,
    duration=2
)
effects_bleed_target = [Effect(
    target=EffectTarget.TARGET,
    chance=0.9 + i * 0.1,
    dot_bleed=1 + (i // 2),
    duration=2
) for i in range(5)]
effects_poison_target = [Effect(
    target=EffectTarget.TARGET,
    chance=0.9 + i * 0.1,
    dot_poison=1 + (i // 2),
    duration=2
) for i in range(5)]
effects_stun_target = [Effect(
    target=EffectTarget.TARGET,
    chance=0.9 + i * 0.1,
    stun=1
) for i in range(5)]

# 反击技能
effect_clear_riposte = Effect(
    target=EffectTarget.PERFORMER,
    clear_riposte=True,
    apply_once=True
)
effect_extra_round = Effect(
    target=EffectTarget.PERFORMER,
    initiative_change=1,
    apply_once=True
)

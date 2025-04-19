from xddtools import AutoName
from xddtools.entries.colour import move, bleed, heal_hp, stress, buff, mark, riposte, stun, blight, Colour, notable
from xddtools.magic import get_set_mode_effect, get_suck_blood_effects, get_cd_tag_effect, get_str_tooltip_effect, \
    get_number_tooltip_buff, get_clear_self_buff_source_effect, get_cd_charge_effect, CDCharge, get_str_tooltip_buff
from xddtools.target import LAUNCH_12, Target, ENEMY_GROUP_12, ALL_ENEMY, LAUNCH_ANY, SELF, LAUNCH_34, ENEMY_GROUP_34
from xddtools.utils import float_to_percent_int

MOD_NAME = "xscourge"
AutoName.set_default_prefix(MOD_NAME)

from xddtools.entries import Resistance, Hero, Weapon, Armour, ActivityModify, Mode, Animation, Effect, \
    HeroLocalization, Generation, Project, ActoutDisplay, Skill, SkillInfo, ModeEffects, Buff, BuffRule, ActorDot, \
    DurationElement, Quirk, HealthBar, TrinketRarity, Trinket, TrinketEffect, TrinketSet
from xddtools.enum import TagID, TownActivityType, QuirkType, EffectTarget, CurioResultType, ProjectTag, SkillType, \
    KeyStatus, BuffType, STCombatStatMultiply, BuffRuleType, BuffDurationType, STCombatStatAdd, BuffSource, \
    STDisableCombatSkillAttribute, STResistance, ActorDotUpdateDurationType, SkillHeadType, QuirkTag, \
    TrinketAwardCategory, TrinketRarityType, TrinketTriggerType
from xddtools.writers import get_dd_writer

if __name__ == '__main__':
    project = Project(
        title="灾厄",
        preview_icon_image="hero/preview_icon.png",
        tags=[ProjectTag.NEW_CLASS]
    )

    skill_name_a_to_c = AutoName().new_skill()
    skill_name_c_to_a = AutoName().new_skill()
    skill_a1 = AutoName().new_skill()
    skill_a2 = AutoName().new_skill()
    skill_a3 = AutoName().new_skill()
    skill_b1 = AutoName().new_skill()
    skill_b2 = AutoName().new_skill()
    skill_b3 = AutoName().new_skill()

    modes_a = [Mode(
        is_raid_default=True if i == 0 else False,
        affliction_combat_skill_id=skill_name_a_to_c,
        battle_complete_combat_skill_id="move",
        actor_mode_name=f"普通形态-{i}充能",
        # str_skill_mode_info=f"{i}充能时：",
        str_skill_mode_info="",
        combat=Animation(anim_dir="anim/combat_a"),
        # defend=Animation(anim_dir="anim/defend_a"),
        riposte=Animation(anim_dir="anim/skill_a1"),
        battle_complete_sfx="audio/Scourge_SK7 {fa1467a6-b782-45c9-bf88-92ae1ac64bf6}.wav"
    ) for i in range(4)]

    change_modes_a = [get_set_mode_effect(mode, False, True, False) for mode in modes_a]

    mode_b = Mode(
        affliction_combat_skill_id=skill_name_a_to_c,
        battle_complete_combat_skill_id="move",
        actor_mode_name=f"律令形态",
        str_skill_mode_info=f"律令形态时：",
        combat=Animation(anim_dir="anim/combat_a"),
        # defend=Animation(anim_dir="anim/defend_a"),
        riposte=Animation(anim_dir="anim/skill_a1")
    )

    mode_c = Mode(
        battle_complete_combat_skill_id="move",
        actor_mode_name="极巨化形态",
        str_skill_mode_info="极巨化时：",
        combat=Animation(anim_dir="anim/combat_c"),
        # defend=Animation(anim_dir="anim/defend_c"),
        riposte=Animation(anim_dir="anim/skill_c2")
    )

    stun_effect = Effect(
        target=EffectTarget.TARGET,
        chance=1.4,
        has_description=False,
        stun=1
    )
    kill_effect = Effect(
        target=EffectTarget.PERFORMER,
        skill_instant=True,
        has_description=False,
        apply_once=True,
        buff_ids=[
            Buff(
                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
                amount=100,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.TARGET_HP_BELOW,
                    rule_data_float=0.2
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
                amount=0.2,
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
                amount=0.2,
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
                amount=0.1,
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
                duration=2
            )
        ]
    )
    effects_c1 = [Effect(
        target=EffectTarget.PERFORMER_GROUP_OTHER,
        has_description=False,
        chance=100,
        on_hit=False,
        on_miss=True,
        health_damage=5 + i
    ) for i in range(5)]
    effects_c2 = [Effect(
        target=EffectTarget.TARGET_GROUP,
        has_description=False,
        chance=100,
        on_hit=False,
        on_miss=True,
        health_damage=5 + i
    ) for i in range(5)]
    effects_c_tooltip = [get_str_tooltip_effect(f"未命中：对所有其他角色造成{5 + i}点真实伤害") for i in range(5)]
    effect_c3 = Effect(
        target=EffectTarget.PERFORMER,
        duration=1,
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
    poison_cd = get_cd_tag_effect(STDisableCombatSkillAttribute.POISON)
    bleed_cd = get_cd_tag_effect(STDisableCombatSkillAttribute.BLEED)
    daze_cd = get_cd_tag_effect(STDisableCombatSkillAttribute.DAZE)
    crit_effect = Effect(
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
    tooltip_effect_5 = get_str_tooltip_effect(f"{bleed('末日充能')}：{heal_hp('生命偷取')}+50%%/75%%/100%%/125%%")
    tooltip_effect_6 = get_str_tooltip_effect(f"{bleed('末日充能')}：队伍攻击力+0/1/2/3")
    tooltip_effect_7 = get_str_tooltip_effect(f"{bleed('末日充能')}：队伍闪避+0/3/6/9")
    tooltip_effect_8 = get_str_tooltip_effect(f"{riposte('反击')}命中额外获得1回合")

    skill_1 = Skill(
        entry_id=skill_a1,
        skill_type=SkillType.MELEE,
        launch=LAUNCH_12,
        target=Target("123"),
        skill_name="耀斑",
        upgrade_tree_name="耀斑",
        icon_image="hero/Scourge.ability.1.png",
        anim=Animation(anim_dir="anim/skill_a1"),
        hit_sfx="audio/Scourge_SK1 {6ba3b10d-e055-4d05-91cc-52d17bdd6704}.wav",
        miss_sfx="audio/Scourge_SK1 {6ba3b10d-e055-4d05-91cc-52d17bdd6704}.wav",
        skill_info=[
            SkillInfo(
                atk=0.85 + i * 0.05,
                dmg=0,
                per_battle_limit=2,
                effect_ids=[
                    tooltip_effect_1,
                    tooltip_effect_3,
                    tooltip_effect_4,
                    charge_p1,
                    effect_a,
                    effect_a2,
                    bleed_cd
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=modes_a[0],
                        effects=[
                            Effect(
                                target=EffectTarget.PERFORMER,
                                has_description=False,
                                curio_result_type=CurioResultType.POSITIVE,
                                combat_stat_buff=True,
                                key_status=KeyStatus.TAGGED,
                                damage_high_multiply=0.3
                            ),
                            change_modes_a[1]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[1],
                        effects=[
                            Effect(
                                target=EffectTarget.PERFORMER,
                                has_description=False,
                                curio_result_type=CurioResultType.POSITIVE,
                                combat_stat_buff=True,
                                key_status=KeyStatus.TAGGED,
                                damage_high_multiply=0.6
                            ),
                            change_modes_a[2]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[2],
                        effects=[
                            Effect(
                                target=EffectTarget.PERFORMER,
                                has_description=False,
                                curio_result_type=CurioResultType.POSITIVE,
                                combat_stat_buff=True,
                                key_status=KeyStatus.TAGGED,
                                damage_high_multiply=0.9
                            ),
                            change_modes_a[3]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[3],
                        effects=[
                            Effect(
                                target=EffectTarget.PERFORMER,
                                has_description=False,
                                curio_result_type=CurioResultType.POSITIVE,
                                combat_stat_buff=True,
                                key_status=KeyStatus.TAGGED,
                                damage_high_multiply=1.2
                            ),
                            crit_effect,
                            stun_effect,
                            change_modes_a[0]
                        ]
                    )
                ]
            )
            for i in range(5)
        ]
    )

    skill_2 = Skill(
        entry_id=skill_a2,
        skill_type=SkillType.MELEE,
        launch=LAUNCH_12,
        target=ENEMY_GROUP_12,
        skill_name="日蚀",
        upgrade_tree_name="日蚀",
        icon_image="hero/Scourge.ability.2.png",
        anim=Animation(anim_dir="anim/skill_a2"),
        targchestfx=Animation(anim_dir="fx/skill_a2_targchestfx"),
        hit_sfx="audio/Scourge_SK2 {b5831aa6-8776-46ac-9376-994ec2b3c64c}.wav",
        miss_sfx="audio/Scourge_SK2 {b5831aa6-8776-46ac-9376-994ec2b3c64c}.wav",
        skill_info=[
            SkillInfo(
                atk=0.9 + i * 0.05,
                dmg=-0.5,
                per_battle_limit=1,
                damage_heal_base_class_ids=[MOD_NAME],
                effect_ids=[
                    tooltip_effect_2,
                    tooltip_effect_3,
                    tooltip_effect_5,
                    charge_p2,
                    effect_a,
                    effect_a2,
                    bleed_cd
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=modes_a[0],
                        effects=[
                            *get_suck_blood_effects(0.50, has_description=False),
                            change_modes_a[2]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[1],
                        effects=[
                            *get_suck_blood_effects(0.75, has_description=False),
                            change_modes_a[3]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[2],
                        effects=[
                            *get_suck_blood_effects(1.0, has_description=False),
                            change_modes_a[3]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[3],
                        effects=[
                            *get_suck_blood_effects(1.25, has_description=False),
                            crit_effect,
                            stun_effect,
                            change_modes_a[0]
                        ]
                    )
                ]
            )
            for i in range(5)
        ]
    )

    damage_buff_effects = [Effect(
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

    skill_3 = Skill(
        entry_id=skill_b1,
        skill_type=SkillType.MELEE,
        launch=LAUNCH_12,
        target=Target("1234"),
        skill_name="月尘",
        upgrade_tree_name="月尘",
        icon_image="hero/Scourge.ability.4.png",
        anim=Animation(anim_dir="anim/skill_b1"),
        hit_sfx="audio/Scourge_SK4 {07773d12-7e45-4a06-bc63-0a6d00c65f01}.wav",
        miss_sfx="audio/Scourge_SK4 {07773d12-7e45-4a06-bc63-0a6d00c65f01}.wav",
        skill_info=[
            SkillInfo(
                atk=0.9 + i * 0.05,
                dmg=-0.65,
                per_battle_limit=2,
                effect_ids=[
                    tooltip_effect_1,
                    tooltip_effect_3,
                    tooltip_effect_6,
                    charge_p1,
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=0.9 + i * 0.1,
                        combat_stat_buff=True,
                        duration=3,
                        protection_rating_add=-0.1 - i * 0.02 if i < 4 else -0.2
                    ),
                    poison_cd,
                    effect_b,
                    effect_b2
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=modes_a[0],
                        effects=[
                            change_modes_a[1]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[1],
                        effects=[
                            damage_buff_effects[0],
                            change_modes_a[2]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[2],
                        effects=[
                            damage_buff_effects[1],
                            change_modes_a[3]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[3],
                        effects=[
                            damage_buff_effects[2],
                            crit_effect,
                            kill_effect,
                            change_modes_a[0]
                        ]
                    )
                ]
            )
            for i in range(5)
        ]
    )

    def_effects = [Effect(
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

    skill_4 = Skill(
        entry_id=skill_b2,
        skill_type=SkillType.MELEE,
        launch=LAUNCH_12,
        target=ENEMY_GROUP_34,
        skill_name="新月",
        upgrade_tree_name="新月",
        icon_image="hero/Scourge.ability.5.png",
        anim=Animation(anim_dir="anim/skill_b2"),
        hit_sfx="audio/Scourge_SK5 {171c99c1-d09e-4ae8-8ed6-0522759f6e24}.wav",
        miss_sfx="audio/Scourge_SK5 {171c99c1-d09e-4ae8-8ed6-0522759f6e24}.wav",
        skill_info=[
            SkillInfo(
                atk=0.95 + i * 0.05,
                dmg=-0.95,
                per_battle_limit=1,
                effect_ids=[
                    tooltip_effect_2,
                    tooltip_effect_3,
                    tooltip_effect_7,
                    charge_p2,
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=0.9 + i * 0.1,
                        combat_stat_buff=True,
                        duration=3,
                        defense_rating_add=-0.15 + i * 0.01 if i < 4 else -0.2
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=0.9 + i * 0.1,
                        duration=1,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
                                amount=0.1 + i * 0.02 if i < 4 else 0.2
                            )
                        ]
                    ),
                    poison_cd,
                    effect_b,
                    effect_b2
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=modes_a[0],
                        effects=[
                            change_modes_a[1]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[1],
                        effects=[
                            def_effects[0],
                            change_modes_a[2]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[2],
                        effects=[
                            def_effects[1],
                            change_modes_a[3]
                        ]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[3],
                        effects=[
                            def_effects[2],
                            crit_effect,
                            kill_effect,
                            change_modes_a[0]
                        ]
                    )
                ]
            )
            for i in range(5)
        ]
    )

    riposte_effect = Effect(
        target=EffectTarget.PERFORMER,
        duration=3,
        riposte=True,
        riposte_on_hit_chance_add=1,
        riposte_on_miss_chance_add=1
    )

    tag_self_2_round = Effect(
        target=EffectTarget.PERFORMER,
        tag=True,
        duration=2
    )

    no_crit_effect = Effect(
        target=EffectTarget.PERFORMER,
        duration=2,
        buff_ids=[
            Buff(
                stat_type=BuffType.CRIT_RECEIVED_CHANCE,
                amount=-1
            )
        ]
    )

    skill_5 = Skill(
        skill_type=SkillType.RANGED,
        launch=LAUNCH_ANY,
        target=ALL_ENEMY,
        skill_name="友善的交流",
        upgrade_tree_name="友善的交流",
        icon_image="hero/Scourge.ability.7.png",
        anim=Animation(anim_dir="anim/skill_ab"),
        hit_sfx="audio/Scourge_SK7 {fa1467a6-b782-45c9-bf88-92ae1ac64bf6}.wav",
        miss_sfx="audio/Scourge_SK7 {fa1467a6-b782-45c9-bf88-92ae1ac64bf6}.wav",
        skill_info=[
            SkillInfo(
                atk=0.95 + i * 0.05,
                dmg=-1,
                per_battle_limit=1,
                effect_ids=[
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1 + i * 0.1,
                        duration=1,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.CRIT_RECEIVED_CHANCE,
                                amount=0.3 + i * 0.02 if i < 4 else 0.4
                            )
                        ]
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=0.9 + i * 0.1,
                        duration=1,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
                                stat_sub_type=STDisableCombatSkillAttribute.STRESS
                            )
                        ]
                    ),
                    riposte_effect,
                    tooltip_effect_8,
                    tag_self_2_round,
                    Effect(
                        target=EffectTarget.PERFORMER_GROUP,
                        chance=0.5 + i * 0.02 if i < 4 else 0.6,
                        heal_stress=2 + i,
                        apply_once=True
                    ),
                    no_crit_effect,
                    bleed_cd,
                    poison_cd
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=modes_a[0]
                    )
                ]
            )
            for i in range(5)
        ]
    )

    clear_guard_effect = Effect(
        target=EffectTarget.PERFORMER_GROUP,
        queue=False,
        clear_guarded=True,
        clear_guarding=True,
        has_description=False
    )

    skill_6 = Skill(
        entry_id=skill_name_a_to_c,
        skill_type=SkillType.RANGED,
        launch=LAUNCH_ANY,
        target=SELF,
        skill_name="坠入星界",
        icon_image="hero/Scourge.ability.9.png",
        anim=Animation(anim_dir="anim/transform_a_c"),
        hit_sfx="audio/Scourge_SK9 {9017c964-2424-4fca-8c8f-299eae40d251}.wav",
        miss_sfx="audio/Scourge_SK9 {9017c964-2424-4fca-8c8f-299eae40d251}.wav",
        skill_info=[
            SkillInfo(
                per_battle_limit=1,
                is_continue_turn=True,
                effect_ids=[
                    get_str_tooltip_effect(f"{bleed('恐惧值')}大于等于3时可用"),
                    get_str_tooltip_effect(f"每1点{bleed('恐惧值')}提升50%%{heal_hp('最大生命')}/40%%暴击率"),
                    get_str_tooltip_effect(f"{move('扰乱')}双方"),
                    get_set_mode_effect(mode_c, ensure_last=False),
                    bleed_cd,
                    poison_cd,
                    daze_cd,
                    Effect(
                        target=EffectTarget.PERFORMER,
                        buff_source_type=BuffSource.NEVER_AGAIN,
                        duration=1,
                        buff_duration_type=BuffDurationType.COMBAT_END,
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
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        heal_percent=0.5,
                        apply_once=True
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER_GROUP,
                        chance=100,
                        shuffle_target=True,
                        apply_once=True,
                        has_description=False
                    ),
                    clear_guard_effect,
                    Effect(
                        target=EffectTarget.PERFORMER_GROUP_OTHER,
                        guard=True,
                        duration=1,
                        buff_duration_type=BuffDurationType.COMBAT_END
                    ),
                    Effect(
                        target=EffectTarget.TARGET_ENEMY_GROUP,
                        chance=100,
                        shuffle_target=True,
                        apply_once=True,
                        has_description=False
                    )
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=modes_a[0]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[1]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[2]
                    ),
                    ModeEffects(
                        valid_mode=modes_a[3]
                    ),
                ]
            )
        ]
    )

    skill_7 = Skill(
        skill_type=SkillType.MELEE,
        launch=LAUNCH_12,
        target=Target("234"),
        skill_name="飞踢",
        upgrade_tree_name="飞踢",
        icon_image="hero/Scourge.ability.10.png",
        anim=Animation(anim_dir="anim/skill_c1"),
        hit_sfx="audio/Scourge_SK10 {7aee8460-c254-4feb-9d39-7f886230269a}.wav",
        miss_sfx="audio/Scourge_SK10 {7aee8460-c254-4feb-9d39-7f886230269a}.wav",
        skill_info=[
            SkillInfo(
                atk=0.8 + i * 0.05,
                dmg=-0.5,
                per_battle_limit=1,
                move_back=1,
                effect_ids=[
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1 + i * 0.1,
                        push=3
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1 + i * 0.1,
                        stun=1
                    ),
                    effects_c1[i],
                    effects_c2[i],
                    effect_c3,
                    effects_c_tooltip[i]
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=mode_c
                    )
                ]
            )
            for i in range(5)
        ]
    )

    skill_8 = Skill(
        skill_type=SkillType.MELEE,
        launch=LAUNCH_ANY,
        target=Target("123"),
        skill_name="尾击",
        upgrade_tree_name="尾击",
        icon_image="hero/Scourge.ability.11.png",
        anim=Animation(anim_dir="anim/skill_c2"),
        hit_sfx="audio/Scourge_SK11 {5a10dd7d-bd8c-4380-b8d0-f936626d8ef8}.wav",
        miss_sfx="audio/Scourge_SK11 {5a10dd7d-bd8c-4380-b8d0-f936626d8ef8}.wav",
        skill_info=[
            SkillInfo(
                atk=0.85 + i * 0.05,
                dmg=-0.3,
                move_forward=1,
                per_battle_limit=1,
                effect_ids=[
                    Effect(
                        target=EffectTarget.PERFORMER,
                        key_status=KeyStatus.STUNNED,
                        combat_stat_buff=True,
                        damage_high_multiply=0.3 + i * 0.1
                    ),
                    get_str_tooltip_effect(f"对{stun('眩晕')}目标+{float_to_percent_int(0.3 + i * 0.1)}%%最大攻击力"),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1 + i * 0.1,
                        duration=2,
                        combat_stat_buff=True,
                        damage_low_multiply=-0.2 - i * 0.02 if i < 4 else -0.3,
                        damage_high_multiply=-0.2 - i * 0.02 if i < 4 else -0.3
                    ),
                    effects_c1[i],
                    effects_c2[i],
                    effect_c3,
                    effects_c_tooltip[i]
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=mode_c
                    )
                ]
            )
            for i in range(5)
        ]
    )

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
        fx=Animation(anim_dir="fx/actor_dot", hero_name=MOD_NAME, need_rename=False)
    )

    immobilize_effect = Effect(
        target=EffectTarget.TARGET,
        chance=100,
        actor_dot=immobilize_dot,
        immobilize=True,
        duration=1,
        buff_duration_type=BuffDurationType.COMBAT_END
    )
    immobilize_effect_tooltip = get_str_tooltip_effect(f"{move('禁锢')}目标（3次攻击后解除）")

    skill_9 = Skill(
        skill_type=SkillType.RANGED,
        launch=LAUNCH_34,
        target=Target("1234"),
        skill_name="来吧",
        upgrade_tree_name="来吧",
        icon_image="hero/Scourge.ability.12.png",
        anim=Animation(anim_dir="anim/skill_c3"),
        hit_sfx="audio/Scourge_SK12 {f839b631-319f-4cf2-a326-f7e4ba5abbf3}.wav",
        miss_sfx="audio/Scourge_SK12 {f839b631-319f-4cf2-a326-f7e4ba5abbf3}.wav",
        skill_info=[
            SkillInfo(
                atk=0.8 + i * 0.05,
                dmg=-0.1,
                move_forward=3,
                per_battle_limit=1,
                effect_ids=[
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=1 + i * 0.1,
                        pull=3
                    ),
                    immobilize_effect,
                    immobilize_effect_tooltip,
                    effects_c1[i],
                    effects_c2[i],
                    effect_c3,
                    effects_c_tooltip[i]
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=mode_c
                    )
                ]
            )
            for i in range(5)
        ]
    )

    quirk = Quirk(
        str_quirk_name="魔王",
        str_quirk_description="我即是灾厄！",
        random_chance=0.0,
        can_modify_in_activity=False,
        can_remove_with_camping_skill=False,
        can_be_replaced_by_new_quirk=False,
        tags=[QuirkTag.CANT_LOCK],
        buffs=[
            Buff(
                stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
                stat_sub_type=STDisableCombatSkillAttribute.DAZE,
                amount=3,
                has_description=False
            ),
            Buff(
                stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
                amount=0.5,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_MODE,
                    rule_data_string=mode_c
                )
            ),
            Buff(
                stat_type=BuffType.MONSTERS_SURPRISE_CHANCE,
                amount=0.25
            )
        ]
    )
    quirk_effect = Effect(
        target=EffectTarget.PERFORMER,
        chance=100,
        disease=quirk,
        has_description=False
    )

    change_back_a0 = get_set_mode_effect(modes_a[0], ensure_last=False)

    skill_10 = Skill(
        entry_id=skill_name_c_to_a,
        skill_type=SkillType.RANGED,
        launch=LAUNCH_ANY,
        target=SELF,
        skill_name="重返现实",
        icon_image="hero/Scourge.ability.13.png",
        anim=Animation(anim_dir="anim/transform_c_a"),
        hit_sfx="audio/Scourge_SK13 {adc70f61-9fd1-4b5d-a698-c757e2637cb4}.wav",
        miss_sfx="audio/Scourge_SK13 {adc70f61-9fd1-4b5d-a698-c757e2637cb4}.wav",
        skill_info=[
            SkillInfo(
                # per_battle_limit=1,
                effect_ids=[
                    change_back_a0,
                    Effect(
                        target=EffectTarget.PERFORMER_GROUP,
                        heal_percent=0.25
                    ),
                    clear_charge,
                    clear_guard_effect
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=mode_c
                    )
                ]
            )
        ]
    )

    skill_11 = Skill(
        entry_id=skill_a3,
        skill_type=SkillType.RANGED,
        launch=LAUNCH_34,
        target=Target("1234"),
        skill_name="律令：死亡",
        upgrade_tree_name="律令：死亡",
        icon_image="hero/Scourge.ability.6.png",
        anim=Animation(anim_dir="anim/skill_a3"),
        targchestfx=Animation(anim_dir="fx/skill_a3_targchestfx"),
        hit_sfx="audio/Scourge_SK6 {45e3c21c-2eab-4587-8fb7-690a903606cd}.wav",
        miss_sfx="audio/Scourge_SK6 {45e3c21c-2eab-4587-8fb7-690a903606cd}.wav",
        skill_info=[
            SkillInfo(
                per_battle_limit=1,
                atk=0.85 + i * 0.05,
                crit=1.075 + i * 0.01,
                dmg=-0.15,
                effect_ids=[
                    change_modes_a[0],
                    effect_a,
                    get_str_tooltip_effect(f"对{mark('标记')}/{bleed('流血')}/{blight('腐蚀')}/{stun('眩晕')}"
                                           f"最大攻击力+{float_to_percent_int(0.3 + i * 0.02 if i < 4 else 0.4)}%%"),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        has_description=False,
                        curio_result_type=CurioResultType.POSITIVE,
                        combat_stat_buff=True,
                        key_status=KeyStatus.TAGGED,
                        damage_high_multiply=0.3 + i * 0.02 if i < 4 else 0.4,
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        has_description=False,
                        curio_result_type=CurioResultType.POSITIVE,
                        combat_stat_buff=True,
                        key_status=KeyStatus.BLEEDING,
                        damage_high_multiply=0.3 + i * 0.02 if i < 4 else 0.4,
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        has_description=False,
                        curio_result_type=CurioResultType.POSITIVE,
                        combat_stat_buff=True,
                        key_status=KeyStatus.POISONED,
                        damage_high_multiply=0.3 + i * 0.02 if i < 4 else 0.4,
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        has_description=False,
                        curio_result_type=CurioResultType.POSITIVE,
                        combat_stat_buff=True,
                        key_status=KeyStatus.STUNNED,
                        damage_high_multiply=0.3 + i * 0.02 if i < 4 else 0.4,
                    )
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=mode_b
                    )
                ]
            )
            for i in range(5)
        ]
    )

    skill_12 = Skill(
        entry_id=skill_b3,
        skill_type=SkillType.RANGED,
        launch=LAUNCH_34,
        target=Target("1234"),
        skill_name="律令：痛苦",
        upgrade_tree_name="律令：痛苦",
        icon_image="hero/Scourge.ability.3.png",
        anim=Animation(anim_dir="anim/skill_b3"),
        targchestfx=Animation(anim_dir="fx/skill_b3_targchestfx"),
        hit_sfx="audio/Scourge_SK3 {c21b3b34-0837-445f-97dc-fc8accff2c5e}.wav",
        miss_sfx="audio/Scourge_SK3 {c21b3b34-0837-445f-97dc-fc8accff2c5e}.wav",
        skill_info=[
            SkillInfo(
                per_battle_limit=1,
                atk=0.95 + i * 0.05,
                dmg=-1,
                effect_ids=[
                    change_modes_a[0],
                    effect_b,
                    Effect(
                        target=EffectTarget.TARGET,
                        tag=True,
                        duration=3
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=0.9+i*0.1,
                        dot_bleed=1+(i//2),
                        buff_duration_type=BuffDurationType.COMBAT_END,
                        duration=1
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=0.9 + i * 0.1,
                        dot_poison=1 + (i // 2),
                        buff_duration_type=BuffDurationType.COMBAT_END,
                        duration=1
                    ),
                    Effect(
                        target=EffectTarget.TARGET,
                        chance=0.9+i*0.1,
                        stun=1
                    )
                ],
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=mode_b
                    )
                ]
            )
            for i in range(5)
        ]
    )

    move_skill = Skill(
        entry_id="move",
        skill_name="移动",
        skill_head_type=SkillHeadType.COMBAT_MOVE_SKILL,
        skill_type=SkillType.MOVE,
        launch=LAUNCH_ANY,
        skill_info=[
            SkillInfo(
                move_back=2,
                move_forward=2,
                effect_ids=[
                    get_set_mode_effect(modes_a[0], ensure_last=False, has_description=False),
                    quirk_effect
                ]
            )
        ]
    )

    riposte_skill = Skill(
        skill_head_type=SkillHeadType.RIPOSTE_SKILL,
        skill_type=SkillType.MELEE,
        launch=LAUNCH_ANY,
        target=Target("1234"),
        skill_info=[
            SkillInfo(
                atk=1,
                dmg=-0.33,
                crit=0,
                effect_ids=[
                    Effect(
                        target=EffectTarget.PERFORMER,
                        clear_riposte=True
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        initiative_change=1,
                    )
                ]
            )
        ],
        hit_sfx="audio/Scourge_SK1 {6ba3b10d-e055-4d05-91cc-52d17bdd6704}.wav",
        miss_sfx="audio/Scourge_SK1 {6ba3b10d-e055-4d05-91cc-52d17bdd6704}.wav"
    )

    hero = Hero(
        entry_id=MOD_NAME,
        id_index=101,
        target_rank=2,
        can_select_combat_skills=False,
        number_of_selected_combat_skills_max=12,
        resistances=Resistance(
            stun=0.6,
            poison=0.0,
            bleed=0.0,
            disease=0.6,
            move=0.4,
            debuff=0.4,
            death_blow=0.67,
            trap=0.1
        ),
        weapons=[
            Weapon(attack=0, damage_low=1, damage_high=11, critical_rate=-1, speed=8),
            Weapon(attack=0, damage_low=1, damage_high=21, critical_rate=-1, speed=10)
        ],
        armours=[
            Armour(defense=0.1, protection=0, hp=26, speed=0),
            Armour(defense=0.3, protection=0, hp=46, speed=0)
        ],
        weapon_images=[f"icons_equip/eqp_weapon_{i}.png" for i in range(5)],
        armour_images=[f"icons_equip/eqp_armour_{i}.png" for i in range(5)],
        guild_header_image_path="hero/Scourge_guild_header.png",
        portrait_roster_image_path="hero/Scourge_portrait_roster.png",
        tags=[TagID.LIGHT, TagID.NON_RELIGIOUS, TagID.OUTSIDERS_BONFIRE],
        can_self_party=False,
        activity_modifier=ActivityModify(
            activity_ids=[
                TownActivityType.BROTHEL,
                TownActivityType.BAR,
                TownActivityType.GAMBLING,
                TownActivityType.TREATMENT,
                TownActivityType.DISEASE_TREATMENT
            ],
            stress_removal_amount_low=50,
            stress_removal_amount_high=100
        ),
        quirk_modifier=[
            QuirkType.NEGATIVE_ENLIGHTENED,
            QuirkType.NEGATIVE_FLAGELLANT,
            QuirkType.NEGATIVE_UNQUIET_MIND,
            QuirkType.NEGATIVE_WITNESS,
            QuirkType.NEGATIVE_FAITHLESS,
            QuirkType.POSITIVE_MEDITATOR,
            QuirkType.NEGATIVE_GOD_FEARING,
            QuirkType.POSITIVE_WARRIOR_OF_LIGHT,
            QuirkType.NEGATIVE_DIURNAL,
            QuirkType.NEGATIVE_FEAR_OF_UNHOLY,
            QuirkType.NEGATIVE_LYGOPHOBIA,
            QuirkType.POSITIVE_PHOTOMANIA,
            QuirkType.POSITIVE_EARLY_RISER,
            QuirkType.NEGATIVE_NIGHT_BLINDNESS,
            QuirkType.NEGATIVE_SATANOPHOBIA,
            QuirkType.POSITIVE_SPIRITUAL,
            QuirkType.DISEASE_VAMPIRE_PASSIVE,
        ],
        base_mode=Mode(
            afflicted=Animation(anim_dir="anim/afflicted"),
            camp=Animation(anim_dir="anim/camp"),
            heroic=Animation(anim_dir="anim/heroic"),
            idle=Animation(anim_dir="anim/idle"),
            investigate=Animation(anim_dir="anim/investigate"),
            defend=Animation(anim_dir="anim/defend"),
            walk=Animation(anim_dir="anim/walk")
        ),
        crit_effects=[
            Effect(
                target=EffectTarget.PERFORMER,
                refreshes_skill_uses=True
            ),
            Effect(
                target=EffectTarget.PERFORMER,
                curio_result_type=CurioResultType.POSITIVE,
                buff_source_type=BuffSource.CRIT,
                duration=3,
                buff_ids=[
                    Buff(
                        stat_type=BuffType.HP_HEAL_RECEIVED_PERCENT,
                        amount=0.2
                    )
                ]
            )
        ],
        skills=[skill_1, skill_2, skill_3, skill_4, skill_5, skill_6, skill_7, skill_8, skill_9, skill_10,
                skill_11, skill_12, move_skill, riposte_skill],
        generation=Generation(card_chance=100, number_of_cards_in_deck=100, number_of_random_combat_skills=12),
        actout_display=ActoutDisplay(
            attack_friendly_anim="riposte"
        ),
        health_bar=HealthBar(current_top="#FFC0CB"),
        hero_localization=HeroLocalization(
            hero_class_name="灾厄",
            blacksmith_verbose="",
            guild_verbose="",
            camping_verbose="",
            weapon_upgrade="镰斧",
            weapon_0="破烂的折叠镰刀",
            weapon_1="银质折叠镰斧",
            weapon_2="灵能镰斧",
            weapon_3="契约镰斧",
            weapon_4="“忠告”",
            armour_upgrade="装束",
            armour_0="赤身裸体",
            armour_1="简单的遮蔽",
            armour_2="合身的着装",
            armour_3="量身定制的装束",
            armour_4="“纵欲”"
        )
    )

    rarity = TrinketRarity(
        award_category=TrinketAwardCategory.TROPHY,
        trinket_rarity_title="世界",
        rarity_image="trinket/rarity_Scourge_World.png"
    )

    world_colour = Colour(rgba=(202, 66, 117, 255), entry_id=rarity.id())
    trinket_0 = Trinket(
        hero_class_requirements=[MOD_NAME],
        rarity=TrinketRarityType.COMMON,
        str_inventory_title_trinket="德罗姆的建言",
        inv_trinket_image="trinket/inv_trinket+Scourge_1.png",
        limit=1,
        buffs=[
            get_str_tooltip_buff(world_colour(text="“别忘了有空时来看看我”\n")),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.DAMAGE_LOW,
                has_description=False,
                amount=5
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.DAMAGE_HIGH,
                has_description=False,
                amount=-5
            ),
            get_str_tooltip_buff("+5最小攻击\n-5最大攻击"),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.ATTACK_RATING,
                amount=0.05
            ),
            Buff(
                stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
                amount=0.1
            )
        ]
    )

    trinket_1 = Trinket(
        hero_class_requirements=[MOD_NAME],
        rarity=TrinketRarityType.UNCOMMON,
        str_inventory_title_trinket="一罐能量饮料",
        inv_trinket_image="trinket/inv_trinket+Scourge_2.png",
        limit=1,
        buffs=[
            get_str_tooltip_buff(world_colour(text="“饮料里的能量也是能量！”\n")),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.SPEED_RATING,
                amount=-6
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
                amount=-0.5
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
                amount=-0.5
            )
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.ATTACK_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.PERFORMER_GROUP,
                        heal=2,
                        apply_once=True
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER_GROUP,
                        chance=0.5,
                        duration=3,
                        apply_once=True,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.HP_HEAL_RECEIVED_PERCENT,
                                amount=0.25
                            )
                        ]
                    ),
                    Effect(
                        target=EffectTarget.PERFORMER,
                        chance=0.5,
                        duration=3,
                        apply_once=True,
                        buff_ids=[
                            Buff(
                                stat_type=BuffType.HP_HEAL_PERCENT,
                                amount=0.25
                            )
                        ]
                    )
                ]
            )
        ]
    )

    trinket_2 = Trinket(
        hero_class_requirements=[MOD_NAME],
        rarity=TrinketRarityType.RARE,
        str_inventory_title_trinket="往日幻影",
        inv_trinket_image="trinket/inv_trinket+Scourge_3.png",
        limit=1,
        buffs=[
            get_str_tooltip_buff(world_colour(text="“时间从未回头，今夜为了往昔回忆”\n")),
            Buff(
                stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
                amount=0.15
            ),
            get_str_tooltip_buff(f"攻击：自身：获得1点{stress('恐惧值')}"),
            get_str_tooltip_buff(f"攻击：自身：受到6点真实伤害"),
            get_str_tooltip_buff(f"暴击：清除所有极巨化加成（20%%概率）"),
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.ATTACK_SKILL,
                effects=[
                    charge_p1,
                    Effect(
                        target=EffectTarget.PERFORMER,
                        health_damage=6,
                        on_miss=True,
                        has_description=False
                    )
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.ATTACK_CRIT,
                effects=[
                    get_clear_self_buff_source_effect(chance=0.2)
                ]
            )
        ]
    )

    trinket_3 = Trinket(
        hero_class_requirements=[MOD_NAME],
        rarity=TrinketRarityType.VERY_RARE,
        str_inventory_title_trinket="地狱之力战旗",
        inv_trinket_image="trinket/inv_trinket+Scourge_4.png",
        limit=1,
        buffs=[
            get_str_tooltip_buff(world_colour(text="“我即是新的领主，低头！”\n")),
            Buff(
                stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
                stat_sub_type=STDisableCombatSkillAttribute.GUARD,
                amount=1,
                has_description=False
            ),
            Buff(
                stat_type=BuffType.STUN_CHANCE,
                amount=-0.2
            ),
            Buff(
                stat_type=BuffType.DEBUFF_CHANCE,
                amount=-0.2
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
                amount=-0.25
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
                amount=-0.25
            ),
            Buff(
                stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
                amount=0.2
            ),
            get_str_tooltip_buff(f"禁用{notable('坠入星界')}"),
            get_str_tooltip_buff(f"近战攻击：获得3点{bleed('末日充能')}"),
            get_str_tooltip_buff(f"暴击：清空所有{bleed('末日充能')}和{stress('恐惧值')}")
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.ATTACK_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.PERFORMER,
                        duration=2,
                        on_miss=True,
                        tag=True
                    )
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.MELEE_ATTACK_SKILL,
                effects=[
                    get_set_mode_effect(modes_a[3], ensure_last=True, has_description=False)
                ]
            ),
            TrinketEffect(
                trigger=TrinketTriggerType.ATTACK_CRIT,
                effects=[
                    get_set_mode_effect(modes_a[0], ensure_last=True, has_description=False),
                    clear_charge
                ]
            )
        ]
    )

    trinket_set = TrinketSet(
        str_inventory_set_title="领域",
        buffs=[
            Buff(
                stat_type=BuffType.DAMAGE_REFLECT_PERCENT,
                amount=0.3
            )
        ]
    )

    change_mode_b = get_set_mode_effect(mode_b, ensure_last=False)

    trinket_4 = Trinket(
        hero_class_requirements=[MOD_NAME],
        rarity=TrinketRarityType.CRIMSON_COURT,
        set_id=trinket_set,
        limit=1,
        str_inventory_title_trinket="一箱灵魂币",
        inv_trinket_image="trinket/inv_trinket+Scourge_5.png",
        buffs=[
            Buff(
                stat_type=BuffType.DAMAGE_RECEIVED_PERCENT,
                amount=0.25
            ),
            Buff(
                stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
                stat_sub_type=STDisableCombatSkillAttribute.GUARD,
                amount=1,
                has_description=False
            ),
            get_str_tooltip_buff(f"禁用{notable('坠入星界')}"),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.ATTACK_RATING,
                amount=0.15,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.RIPOSTE
                )
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.CRIT_CHANCE,
                amount=1.5,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.RIPOSTE
                )
            )
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.RANGED_ATTACK_SKILL,
                effects=[
                    change_mode_b
                ]
            )
        ]
    )

    trinket_5 = Trinket(
        hero_class_requirements=[MOD_NAME],
        rarity=TrinketRarityType.CRIMSON_COURT,
        set_id=trinket_set,
        limit=1,
        str_inventory_title_trinket="千年图书馆密瑟能核",
        inv_trinket_image="trinket/inv_trinket+Scourge_6.png",
        buffs=[
            Buff(
                stat_type=BuffType.DAMAGE_REFLECT_PERCENT,
                amount=0.25
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.DEFENSE_RATING,
                amount=-0.15
            ),
            get_str_tooltip_buff("攻击：自身：刷新技能使用次数")
        ],
        special_effects=[
            TrinketEffect(
                trigger=TrinketTriggerType.ATTACK_SKILL,
                effects=[
                    Effect(
                        target=EffectTarget.PERFORMER,
                        refreshes_skill_uses=True,
                        has_description=False
                    )
                ]
            )
        ]
    )

    trinket_6 = Trinket(
        hero_class_requirements=[MOD_NAME],
        rarity=TrinketRarityType.COMET,
        shard=80,
        limit=1,
        str_inventory_title_trinket="燃烧怒火之护手",
        inv_trinket_image="trinket/inv_trinket+Scourge_7.png",
        buffs=[
            get_str_tooltip_buff(world_colour(text="“这里最不缺的就是火啦~”\n")),
            Buff(
                stat_type=BuffType.RESISTANCE,
                stat_sub_type=STResistance.BLEED,
                amount=0.6
            ),
            Buff(
                stat_type=BuffType.RESISTANCE,
                stat_sub_type=STResistance.POISON,
                amount=0.6
            ),
            Buff(
                stat_type=BuffType.RESISTANCE,
                stat_sub_type=STResistance.DEATH_BLOW,
                amount=-0.1
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
                amount=0.15,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=0
                )
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
                amount=0.15,
                buff_rule=BuffRule(
                    rule_type=BuffRuleType.IN_RANK,
                    rule_data_float=0
                )
            )
        ]
    )

    trinket_7 = Trinket(
        hero_class_requirements=[MOD_NAME],
        rarity=TrinketRarityType.ANCESTRAL,
        limit=1,
        str_inventory_title_trinket="一纸老旧的契约",
        inv_trinket_image="trinket/inv_trinket+Scourge_10.png",
        buffs=[
            get_str_tooltip_buff(world_colour(text="“你叫恩宠？真是个奇怪的名字……\n呵呵，在这里签名吧。”\n")),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.PROTECTION_RATING,
                amount=0.25
            ),
            Buff(
                stat_type=BuffType.STRESS_HEAL_PERCENT,
                amount=0.5
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_MULTIPLY,
                stat_sub_type=STCombatStatMultiply.MAX_HP,
                amount=-0.15
            ),
            Buff(
                stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
                amount=0.2
            )
        ]
    )

    trinket_8 = Trinket(
        hero_class_requirements=[MOD_NAME],
        rarity=rarity,
        limit=1,
        str_inventory_title_trinket="“泰拉蒂斯”",
        inv_trinket_image="trinket/inv_trinket+Scourge_9.png",
        buffs=[
            get_str_tooltip_buff(world_colour(text="“末日降临的样子吗？这就是答案，它就在你眼前”\n")),
            Buff(
                stat_type=BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE,
                stat_sub_type=STDisableCombatSkillAttribute.DAZE,
                amount=-3,
                has_description=False
            ),
            get_str_tooltip_buff(world_colour(text=f"{notable('坠入星界')}没有{stress('恐惧值')}限制")),
            Buff(
                stat_type=BuffType.STUN_CHANCE,
                amount=0.4
            ),
            Buff(
                stat_type=BuffType.HP_HEAL_PERCENT,
                amount=-0.4
            )
        ]
    )

    writer = get_dd_writer(MOD_NAME)
    writer.add_entry(project)
    writer.add_entry(hero)
    writer.add_entry(world_colour)
    writer.add_entries([
        trinket_0, trinket_1, trinket_2, trinket_3, trinket_4, trinket_5, trinket_6, trinket_7, trinket_8
    ])
    writer.export(MOD_NAME)

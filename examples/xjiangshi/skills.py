from xddtools.entries import Skill, SkillInfo, Effect, Buff, Animation, BuffRule
from xddtools.entries.buff_rule import BuffRuleType
from xddtools.entries.colour import heal_hp, debuff, skill_unselectable, riposte, mark
from xddtools.enum import SkillType, EffectTarget, BuffType, STResistance, STCombatStatAdd, KeyStatus, \
    STCombatStatMultiply, BuffDurationType, HealSource, ActorStatus, SkillHeadType
from xddtools.magic import get_str_tooltip_effect
from xddtools.target import LAUNCH_123, LAUNCH_12, LAUNCH_ANY, Target, LAUNCH_34, ENEMY_GROUP_123, SELF

remove_vampire_effect = Effect(
    target=EffectTarget.PERFORMER,
    remove_vampire=True,
    on_miss=True,
    has_description=False,
    apply_once=True
)

skill_0_effects_0 = [
    Effect(
        target=EffectTarget.TARGET,
        chance=chance,
        duration=3,
        queue=False,
        buff_ids=[
            Buff(
                stat_type=BuffType.RESISTANCE,
                stat_sub_type=STResistance.POISON,
                amount=poison,
            ),
            Buff(
                stat_type=BuffType.RESISTANCE,
                stat_sub_type=STResistance.BLEED,
                amount=poison,
            ),
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.PROTECTION_RATING,
                amount=prot,
            )
        ]
    )
    for chance, poison, prot in [
        (1.0, -0.08, -0.12),
        (1.1, -0.11, -0.14),
        (1.2, -0.14, -0.16),
        (1.3, -0.17, -0.18),
        (1.4, -0.20, -0.20),
    ]
]

skill_0 = Skill(
    skill_name="坏死之触",
    upgrade_tree_name="坏死之触",
    skill_type=SkillType.MELEE,
    launch=LAUNCH_123,
    target=Target("12"),
    skill_info=[
        SkillInfo(
            atk=0.85 + i * 0.05,
            dmg=0,
            crit=i * 0.01,
            move_forward=1,
            effect_ids=[
                skill_0_effects_0[i],
                remove_vampire_effect
            ]
        )
        for i in range(5)
    ],
    icon_image="icons_skill/jiangshi.ability.one.png",
    anim=Animation(anim_dir="anim/attack_claw_swipe"),
    fx=Animation(anim_dir="fx/attack_claw_swipe"),
    targchestfx=Animation(anim_dir="fx/attack_claw_swipe_target"),
    hit_sfx="audio/jiangshi_riposte {a519dfa8-6b45-4192-ae95-46dc1b2e4d9c}.wav",
    miss_sfx="audio/jiangshi_riposte_miss {a068ea87-9e6e-45a1-b891-bf6531bfde40}.wav"
)

skill_1_effect = Effect(
    target=EffectTarget.PERFORMER,
    key_status=KeyStatus.TAGGED,
    combat_stat_buff=True,
    attack_rating_add=0.25,
)

skill_1 = Skill(
    skill_name="神出鬼没",
    upgrade_tree_name="神出鬼没",
    skill_type=SkillType.RANGED,
    launch=LAUNCH_12,
    target=Target("12"),
    skill_info=[
        SkillInfo(
            atk=0.50 + i * 0.05,
            dmg=0.6,
            crit=0.03 + i * 0.01,
            effect_ids=[
                skill_1_effect,
                remove_vampire_effect
            ]
        )
        for i in range(5)
    ],
    icon_image="icons_skill/jiangshi.ability.two.png",
    anim=Animation(anim_dir="anim/attack_haunt"),
    fx=Animation(anim_dir="fx/attack_haunt"),
    targchestfx=Animation(anim_dir="fx/attack_haunt_target"),
    hit_sfx="audio/jiangshi_haunt {cb7a2299-7696-435e-82ea-81da999e99a1}.wav",
    miss_sfx="audio/jiangshi_haunt_miss {fa348e46-c71a-45ac-9aba-4bf7e88889d9}.wav"
)

skill_2_effect_0 = Effect(
    target=EffectTarget.TARGET,
    unstealth=True
)
skill_2_effect_1 = Effect(
    target=EffectTarget.TARGET,
    duration=3,
    tag=True
)
skill_2_effects_2 = [
    Effect(
        target=EffectTarget.PERFORMER,
        combat_stat_buff=True,
        attack_rating_add=atk,
        queue=False,
        apply_once=True
    )
    for atk in [0.10, 0.12, 0.15, 0.17, 0.20]
]
skill_2_effects_3 = [
    Effect(
        target=EffectTarget.PERFORMER,
        chance=0.75 + i * 0.10,
        instant_shuffle=True,
        on_hit=False,
        on_miss=True,
        apply_once=True
    )
    for i in range(5)
]

skill_2 = Skill(
    skill_name="检测呼吸",
    upgrade_tree_name="检测呼吸",
    skill_type=SkillType.RANGED,
    launch=LAUNCH_ANY,
    target=Target("1234"),
    skill_info=[
        SkillInfo(
            atk=0.95 + i * 0.05,
            dmg=-1.0,
            crit=0,
            is_crit_valid=False,
            ignore_stealth=True,
            effect_ids=[
                skill_2_effect_0,
                skill_2_effect_1,
                skill_2_effects_2[i],
                skill_2_effects_3[i],
                remove_vampire_effect
            ]
        )
        for i in range(5)
    ],
    icon_image="icons_skill/jiangshi.ability.three.png",
    anim=Animation(anim_dir="anim/attack_detect_breach"),
    fx=Animation(anim_dir="fx/attack_detect_breath"),
    hit_sfx="audio/jiangshi_detect_breath {67152fc5-5c85-417f-b79d-2b010aea5bd2}.wav",
    miss_sfx="audio/jiangshi_detect_breath_miss {cbe61dfb-16d3-4fe4-b633-1f4d8ca2afd0}.wav"
)

skill_3_effect_0 = Effect(
    target=EffectTarget.PERFORMER,
    skill_instant=True,
    buff_ids=[
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_LOW,
            amount=1.2,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.TARGET_HP_ABOVE,
                rule_data_float=0.75
            )
        ),
        Buff(
            stat_type=BuffType.COMBAT_STAT_MULTIPLY,
            stat_sub_type=STCombatStatMultiply.DAMAGE_HIGH,
            amount=1.2,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.TARGET_HP_ABOVE,
                rule_data_float=0.75
            )
        )
    ]
)

skill_3_effects_1 = [
    Effect(
        target=EffectTarget.PERFORMER,
        combat_stat_buff=True,
        protection_rating_add=prot,
        queue=False
    )
    for prot in [0.05, 0.06, 0.07, 0.08, 0.10]
]

skill_3_effects_2 = [
    Effect(
        target=EffectTarget.PERFORMER,
        combat_stat_buff=True,
        attack_rating_add=0.06 + i * 0.02,
        queue=False,
        apply_once=True
    )
    for i in range(5)
]

skill_3_effects_3 = [
    Effect(
        target=EffectTarget.PERFORMER,
        buff_duration_type=BuffDurationType.COMBAT_END,
        duration=3,
        apply_once=True,
        has_description=False,
        buff_ids=[
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.MAX_HP,
                amount=i,
                duration_type=BuffDurationType.COMBAT_END,
                duration=3
            ),
        ]
    )
    for i in [2, 2, 3, 3, 4]
]

skill_3_effects_4 = [
    Effect(
        target=EffectTarget.TARGET,
        chance=100,
        buff_duration_type=BuffDurationType.COMBAT_END,
        duration=3,
        apply_once=True,
        has_description=False,
        buff_ids=[
            Buff(
                stat_type=BuffType.COMBAT_STAT_ADD,
                stat_sub_type=STCombatStatAdd.MAX_HP,
                amount=i,
                duration_type=BuffDurationType.COMBAT_END,
                duration=3
            ),
        ]
    )
    for i in [-2, -2, -3, -3, -4]
]

skill_3_effects_5 = [
    Effect(
        target=EffectTarget.PERFORMER,
        skill_instant=True,
        has_description=False,
        buff_ids=[
            Buff(
                stat_type=BuffType.HP_HEAL_RECEIVED_PERCENT,
                stat_sub_type=HealSource.DAMAGE_HEAL,
                amount=round(-0.6 + i * 0.05, 2),
            )
        ]
    )
    for i in range(5)
]

skill_3_effects_6 = [
    Effect(
        target=EffectTarget.TARGET,
        chance=1.1 + i * 0.1,
        combat_stat_buff=True,
        speed_rating_add=-1 - i,
    )
    for i in range(5)
]

skill_3_effects_7 = [
    Effect(
        target=EffectTarget.TARGET,
        chance=1.1 + i * 0.1,
        combat_stat_buff=True,
        defense_rating_add=-0.10 - i * 0.025,
        queue=False
    )
    for i in range(5)
]

skill_3_tt_0 = [
    get_str_tooltip_effect(f"{40 + i * 5}%% {heal_hp('生命偷取')}")
    for i in range(5)
]

skill_3_tt_1 = [
    get_str_tooltip_effect(f"{debuff('偷取')}目标{i}点{heal_hp('最大生命')}{skill_unselectable('（持续3场战斗）')}")
    for i in [2, 2, 3, 3, 4]
]

skill_3 = Skill(
    skill_name="气泄",
    upgrade_tree_name="气泄",
    skill_type=SkillType.RANGED,
    launch=LAUNCH_12,
    target=Target("123"),
    skill_info=[
        SkillInfo(
            generation_guaranteed=True if i == 0 else False,
            atk=0.85 + i * 0.05,
            dmg=-0.5,
            crit=0,
            is_crit_valid=False,
            damage_heal_base_class_ids=["xjiangshi"],
            effect_ids=[
                skill_3_effect_0,
                skill_3_effects_1[i],
                skill_3_effects_2[i],
                skill_3_effects_3[i],
                skill_3_effects_4[i],
                skill_3_effects_5[i],
                skill_3_effects_6[i],
                skill_3_effects_7[i],
                skill_3_tt_0[i],
                skill_3_tt_1[i],
                remove_vampire_effect
            ]
        )
        for i in range(5)
    ],
    icon_image="icons_skill/jiangshi.ability.four.png",
    anim=Animation(anim_dir="anim/attack_drain_chi"),
    fx=Animation(anim_dir="fx/attack_drain_chi"),
    targchestfx=Animation(anim_dir="fx/attack_drain_chi_target"),
    hit_sfx="audio/jiangshi_chi_drain {ec197270-65cf-4ba6-9433-943ba21802f8}.wav",
    miss_sfx="audio/jiangshi_chi_drain_miss {0eb1b5ad-814a-4ca4-a687-8797c44d117f}.wav"
)

skill_4_effect_0 = Effect(
    target=EffectTarget.PERFORMER,
    skill_instant=True,
    buff_ids=[
        Buff(
            stat_type=BuffType.STUN_CHANCE,
            amount=-0.2,
            buff_rule=BuffRule(
                rule_type=BuffRuleType.IS_ACTOR_STATUS,
                rule_data_string=ActorStatus.TAGGED
            )
        )
    ]
)

skill_4_effect_1 = Effect(
    target=EffectTarget.PERFORMER,
    duration=3,
    tag=True,
    on_miss=True,
    apply_once=True
)

skill_4_effects_2 = [
    Effect(
        target=EffectTarget.TARGET,
        chance=1.0 + i * 0.1,
        stun=1
    )
    for i in range(5)
]

skill_4 = Skill(
    skill_name="恐怖之歌",
    upgrade_tree_name="恐怖之歌",
    skill_type=SkillType.RANGED,
    launch=LAUNCH_12,
    target=Target("123"),
    skill_info=[
        SkillInfo(
            atk=0.90 + i * 0.05,
            dmg=-0.5,
            crit=0.09 + i * 0.01,
            effect_ids=[
                skill_4_effect_0,
                skill_4_effect_1,
                skill_4_effects_2[i],
                remove_vampire_effect
            ]
        )
        for i in range(5)
    ],
    icon_image="icons_skill/jiangshi.ability.five.png",
    anim=Animation(anim_dir="anim/attack_song"),
    fx=Animation(anim_dir="fx/attack_song"),
    hit_sfx="audio/jiangshi_frightening_song {b4cb2a4e-fbea-46dc-9ec3-b7e05e8b96c0}.wav",
    miss_sfx="audio/jiangshi_frightening_song_miss {387a8f54-d3cf-4cc7-abd9-ef9c8ec5cd34}.wav"
)

skill_5_effects_0 = [
    Effect(
        target=EffectTarget.TARGET,
        combat_stat_buff=True,
        attack_rating_add=atk,
        crit_chance_add=crit,
        queue=False
    )
    for atk, crit in [
        (-0.05, -0.02),
        (-0.06, -0.03),
        (-0.07, -0.04),
        (-0.08, -0.05),
        (-0.10, -0.06)
    ]
]

skill_5_effects_1 = [
    Effect(
        target=EffectTarget.TARGET,
        chance=1.0 + i * 0.1,
        dot_shuffle=True,
        duration=1
    )
    for i in range(5)
]

skill_5 = Skill(
    skill_name="恐惧一跃",
    upgrade_tree_name="恐惧一跃",
    skill_type=SkillType.RANGED,
    launch=LAUNCH_34,
    target=ENEMY_GROUP_123,
    skill_info=[
        SkillInfo(
            atk=0.85 + i * 0.05,
            dmg=-0.66,
            crit=-0.04 + i * 0.01,
            move_forward=2,
            is_crit_valid=False,
            effect_ids=[
                skill_5_effects_0[i],
                skill_5_effects_1[i],
                remove_vampire_effect
            ]
        )
        for i in range(5)
    ],
    icon_image="icons_skill/jiangshi.ability.six.png",
    anim=Animation(anim_dir="anim/attack_hop"),
    fx=Animation(anim_dir="fx/attack_hop"),
    hit_sfx="audio/jiangshi_fearfull_leap {b45d0940-85e6-4ae5-9074-7b9f60a45f8f}.wav",
    miss_sfx="audio/jiangshi_leap_miss {5858c8d9-46ff-4af0-8ccd-99ecc907658a}.wav"
)

skill_6_effect_0 = Effect(
    target=EffectTarget.TARGET,
    duration=3,
    tag=True
)

# skill_6_effects_1 = [
#     Effect(
#         target=EffectTarget.TARGET,
#         chance=1.1+i*0.1,
#         combat_stat_buff=True,
#         defense_rating_add=-0.05-i*0.02,
#         queue=False
#     )
#     for i in range(5)
# ]

skill_6_effects_2 = [
    Effect(
        target=EffectTarget.PERFORMER,
        riposte=True,
        riposte_on_hit_chance_add=1,
        riposte_on_miss_chance_add=1,
        on_miss=True,
        duration=3,
        damage_low_multiply=low,
        damage_high_multiply=low,
        attack_rating_add=atk,
        riposte_effect=[
            skill_6_effect_0,
            # skill_6_effects_1[i]  # 反击特效应该只有第一个生效
        ]
    )
    for i, (low, atk) in enumerate([
        (-0.95, 0.10),
        (-0.90, 0.10),
        (-0.85, 0.20),
        (-0.80, 0.20),
        (-0.80, 0.25)
    ])
]

skill_6_tt_0 = get_str_tooltip_effect(f"{riposte('反击')}：{mark('标记')}目标")

skill_6 = Skill(
    skill_name="可怕回忆",
    upgrade_tree_name="可怕回忆",
    skill_type=None,
    launch=LAUNCH_12,
    target=SELF,
    skill_info=[
        SkillInfo(
            is_crit_valid=False,
            effect_ids=[
                skill_6_tt_0,
                skill_6_effects_2[i],
            ]
        )
        for i in range(5)
    ],
    icon_image="icons_skill/jiangshi.ability.seven.png",
    anim=Animation(anim_dir="anim/attack_reminder"),
    fx=Animation(anim_dir="fx/attack_reminder"),
    hit_sfx="audio/jiangshi_horrid {9b57b9ce-a4ac-4170-853c-6682c09c42c9}.wav",
    miss_sfx="audio/jiangshi_horrid {9b57b9ce-a4ac-4170-853c-6682c09c42c9}.wav"
)

move_skill = Skill(
    skill_name="移动",
    skill_head_type=SkillHeadType.COMBAT_MOVE_SKILL,
    skill_type=SkillType.MOVE,
    launch=LAUNCH_ANY,
    skill_info=[
        SkillInfo(
            move_back=1,
            move_forward=1
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
            crit=0
        )
    ],
    fx=Animation(anim_dir="fx/attack_riposte"),
    targchestfx=Animation(anim_dir="fx/attack_riposte_target"),
    hit_sfx="audio/jiangshi_riposte {a519dfa8-6b45-4192-ae95-46dc1b2e4d9c}.wav",
    miss_sfx="audio/jiangshi_riposte_miss {a068ea87-9e6e-45a1-b891-bf6531bfde40}.wav"
)

skills = [
    skill_0, skill_1, skill_2, skill_3, skill_4, skill_5, skill_6,
    move_skill, riposte_skill
]

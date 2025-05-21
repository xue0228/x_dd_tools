from constants import skill_a1, skill_a2, MOD_NAME, skill_b1, skill_b2, skill_a_to_c, skill_c_to_a, skill_a3, skill_b3
from effects import tooltip_effect_1, tooltip_effect_3, tooltip_effect_4, bleed_cd, charge_p1, effect_a, effect_a2, \
    change_modes_a, effects_tag, effect_crit, effect_stun, tooltip_effect_2, tooltip_effect_5, charge_p2, \
    effects_suck_blood, tooltip_effect_6, poison_cd, effects_protection, effect_b, effect_b2, effects_damage_add, \
    effect_kill, tooltip_effect_7, effects_defence, effects_drp, effects_defence_add, tooltip_effect_8, effects_crc, \
    effects_disable_stress, effect_riposte, effect_tag_self, effect_no_crit, effects_heal_stress, tooltip_effect_9, \
    tooltip_effect_11, tooltip_effect_10, daze_cd, change_mode_c, effect_huge, effect_heal_self, effect_clear_guard, \
    effect_guard_ally, effect_shuffle_ally, effect_shuffle_enemy, effects_c1, effects_c2, effect_c3, \
    effects_c_tooltip, effects_push, effects_stun, effects_stun_damage, tooltip_effects_stun_damage, effects_damage, \
    tooltip_effect_immobilize, effects_pull, effect_immobilize, change_mode_a0, effect_heal_ally, clear_charge, \
    effect_clear_guarding, tooltip_effects_status_damage_add, effects_status_damage_add, effect_tag_target, \
    effects_poison_target, effects_stun_target, effects_bleed_target, effect_quirk, change_mode_a0_no_description, \
    effect_clear_riposte, effect_extra_round
from modes import modes_a, mode_c, mode_b
from xddtools.entries import Skill, Animation, SkillInfo, ModeEffects
from xddtools.entries.colour import invisible
from xddtools.enum import SkillType, SkillHeadType
from xddtools.target import LAUNCH_12, Target, ENEMY_GROUP_12, LAUNCH_ANY, ALL_ENEMY, SELF, LAUNCH_34, \
    ENEMY_GROUP_234

skill_1 = Skill(
    entry_id=skill_a1,
    skill_type=SkillType.MELEE,
    launch=LAUNCH_12,
    target=Target("123"),
    skill_name=f"耀斑{invisible('​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​')}",
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
                bleed_cd,
                charge_p1,
                effect_a,
                effect_a2
            ],
            valid_modes_and_effects=[
                ModeEffects(
                    valid_mode=modes_a[0],
                    effects=[
                        effects_tag[0],
                        change_modes_a[1]
                    ]
                ),
                ModeEffects(
                    valid_mode=modes_a[1],
                    effects=[
                        effects_tag[1],
                        change_modes_a[2]
                    ]
                ),
                ModeEffects(
                    valid_mode=modes_a[2],
                    effects=[
                        effects_tag[2],
                        change_modes_a[3]
                    ]
                ),
                ModeEffects(
                    valid_mode=modes_a[3],
                    effects=[
                        effects_tag[3],
                        effect_crit,
                        effect_stun,
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
    condensed_tooltip_effects=True,
    condensed_tooltip_effects_per_line=2,
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
                bleed_cd,
                charge_p2,
                effect_a,
                effect_a2,
            ],
            valid_modes_and_effects=[
                ModeEffects(
                    valid_mode=modes_a[0],
                    effects=[
                        effects_suck_blood[0],
                        change_modes_a[2]
                    ]
                ),
                ModeEffects(
                    valid_mode=modes_a[1],
                    effects=[
                        effects_suck_blood[1],
                        change_modes_a[3]
                    ]
                ),
                ModeEffects(
                    valid_mode=modes_a[2],
                    effects=[
                        effects_suck_blood[2],
                        change_modes_a[3]
                    ]
                ),
                ModeEffects(
                    valid_mode=modes_a[3],
                    effects=[
                        effects_suck_blood[3],
                        effect_crit,
                        effect_stun,
                        change_modes_a[0]
                    ]
                )
            ]
        )
        for i in range(5)
    ]
)

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
                poison_cd,
                effects_protection[i],
                charge_p1,
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
                        effects_damage_add[0],
                        change_modes_a[2]
                    ]
                ),
                ModeEffects(
                    valid_mode=modes_a[2],
                    effects=[
                        effects_damage_add[1],
                        change_modes_a[3]
                    ]
                ),
                ModeEffects(
                    valid_mode=modes_a[3],
                    effects=[
                        effects_damage_add[2],
                        effect_crit,
                        effect_kill,
                        change_modes_a[0]
                    ]
                )
            ]
        )
        for i in range(5)
    ]
)

skill_4 = Skill(
    entry_id=skill_b2,
    skill_type=SkillType.MELEE,
    launch=LAUNCH_12,
    target=ENEMY_GROUP_234,
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
                poison_cd,
                effects_defence[i],
                effects_drp[i],
                charge_p2,
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
                        effects_defence_add[0],
                        change_modes_a[2]
                    ]
                ),
                ModeEffects(
                    valid_mode=modes_a[2],
                    effects=[
                        effects_defence_add[1],
                        change_modes_a[3]
                    ]
                ),
                ModeEffects(
                    valid_mode=modes_a[3],
                    effects=[
                        effects_defence_add[2],
                        effect_crit,
                        effect_kill,
                        change_modes_a[0]
                    ]
                )
            ]
        )
        for i in range(5)
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
            is_stall_invalidating=False,
            effect_ids=[
                tooltip_effect_8,
                bleed_cd,
                poison_cd,
                effects_crc[i],
                effects_disable_stress[i],
                effects_heal_stress[i],
                effect_riposte,
                effect_tag_self,
                effect_no_crit
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

skill_6 = Skill(
    entry_id=skill_a_to_c,
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
                tooltip_effect_9,
                tooltip_effect_10,
                tooltip_effect_11,
                bleed_cd,
                poison_cd,
                daze_cd,
                change_mode_c,
                effect_huge,
                effect_heal_self,
                effect_clear_guard,
                effect_guard_ally,
                effect_shuffle_ally,
                effect_shuffle_enemy
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
                effects_push[i],
                effects_stun[i],
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
                effects_stun_damage[i],
                tooltip_effects_stun_damage[i],
                effects_damage[i],
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
                effects_pull[i],
                effect_immobilize,
                tooltip_effect_immobilize,
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

skill_10 = Skill(
    entry_id=skill_c_to_a,
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
            is_stall_invalidating=False,
            effect_ids=[
                change_mode_a0,
                effect_heal_ally,
                clear_charge,
                effect_clear_guarding
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
                tooltip_effects_status_damage_add[i],
                effects_status_damage_add[i],
                effect_a,
                change_modes_a[0]
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
                effect_tag_target,
                effects_bleed_target[i],
                effects_poison_target[i],
                effects_stun_target[i],
                effect_b,
                change_modes_a[0]
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
                effect_quirk,
                change_mode_a0_no_description
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
                effect_clear_riposte,
                effect_extra_round
            ]
        )
    ],
    hit_sfx="audio/Scourge_SK1 {6ba3b10d-e055-4d05-91cc-52d17bdd6704}.wav",
    miss_sfx="audio/Scourge_SK1 {6ba3b10d-e055-4d05-91cc-52d17bdd6704}.wav"
)

skills = [skill_1, skill_2, skill_3, skill_4, skill_5, skill_6, skill_7, skill_8, skill_9, skill_10, skill_11, skill_12,
          move_skill, riposte_skill]

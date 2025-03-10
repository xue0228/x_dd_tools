from effects import *
from quirk import huihui_quirk
from xddtools.animation import Animation
from xddtools.colour import buff
from xddtools.effects import TooltipEffect
from xddtools.enums import SkillHeadType, SkillType, Level
from xddtools.skills import Skill
from xddtools.target import LAUNCH_ANY, LAUNCH_34, ALL_ENEMY

skill_move = Skill(
    skill_name=auto_name.new_skill(),
    skill_head_type=SkillHeadType.COMBAT_MOVE_SKILL,
    skill_type=SkillType.MOVE,
    launch=LAUNCH_ANY,
    move_back=2,
    move_forward=1,
    effect_ids=(
        TooltipEffect(
            effect_name=auto_name.new_effect(),
            buff_name=auto_name.new_buff(),
            tooltip_text=f"恢复1点{buff('魔力值')}",
            sub_name=auto_name.new_sub_type(),
        ),
        charges[4],
        daze_cd
    ),
    icon="generic_move",
    localization="移动"
)

skill_0s = [
    (TooltipEffect(
        effect_name=auto_name.new_effect(),
        buff_name=auto_name.new_buff(),
        sub_name=auto_name.new_sub_type(),
        tooltip_text=f"恢复1点{buff('魔力值')}"
    ), meditations[0], charges[0]),
    (TooltipEffect(
        effect_name=auto_name.new_effect(),
        buff_name=auto_name.new_buff(),
        sub_name=auto_name.new_sub_type(),
        tooltip_text=f"恢复1点{buff('魔力值')}\n"
                     f"有机率额外恢复1点{buff('魔力值')}"
    ), meditations[1], charges[0], charges[1]),
    (TooltipEffect(
        effect_name=auto_name.new_effect(),
        buff_name=auto_name.new_buff(),
        sub_name=auto_name.new_sub_type(),
        tooltip_text=f"恢复1点{buff('魔力值')}\n"
                     f"有机率额外恢复1-2点{buff('魔力值')}"
    ), meditations[2], charges[0], charges[1], charges[2]),
    (TooltipEffect(
        effect_name=auto_name.new_effect(),
        buff_name=auto_name.new_buff(),
        sub_name=auto_name.new_sub_type(),
        tooltip_text=f"恢复1点{buff('魔力值')}\n"
                     f"有机率额外恢复1-2点{buff('魔力值')}"
    ), meditations[3], charges[0], charges[1], charges[2]),
    (TooltipEffect(
        effect_name=auto_name.new_effect(),
        buff_name=auto_name.new_buff(),
        sub_name=auto_name.new_sub_type(),
        tooltip_text=f"恢复1点{buff('魔力值')}\n"
                     f"有机率额外恢复1-3点{buff('魔力值')}"
    ), meditations[4], charges[0], charges[1], charges[2], charges[3]),
]

skill_0_0 = Skill(
    skill_name=auto_name.new_skill(),
    level=Level.ZERO,
    skill_type=SkillType.RANGED,
    launch=LAUNCH_ANY,
    is_stall_invalidating=False,
    effect_ids=skill_0s[0],
    image_path="combat_skill/arch_wizard.ability.four.png",
    localization="冥想",
    anim=Animation(
        anim_dir="anim/pose",
        anim_name=auto_name.new_anim(),
    ),
    fx=Animation(
        anim_dir="fx/eye",
        anim_name=auto_name.new_anim(),
    )
)
skill_0s = [Skill(
    skill_name=auto_name.last_skill(),
    level=Level(i),
    skill_type=SkillType.RANGED,
    launch=LAUNCH_ANY,
    is_stall_invalidating=False,
    effect_ids=skill_0s[i],
) for i in range(1, 5)]
skill_0s.insert(0, skill_0_0)

disease_quirk = Effect(
    effect_name=auto_name.new_effect(),
    target=EffectTarget.PERFORMER,
    curio_result_type=CurioResultType.POSITIVE,
    chance=100,
    disease=huihui_quirk,
    has_description=False,
    on_miss=True,
    apply_once=True,
)

skill_1s = [
    (skill_1_tooltip, heal_stresses[0], disable_daze, unstealth, poisons[i], clear_charge, disease_quirk)
    for i in range(5)
]
skill_1s_damage = [
    (0.90, 0, 0.05),
    (0.95, 0, 0.06),
    (1.00, 0, 0.07),
    (1.05, 0, 0.08),
    (1.10, 0, 0.09),
]

skill_2s = [
    (skill_2_tooltip, heal_stresses[1], disable_daze, unstealth, tags[i], clear_charge, disease_quirk)
    for i in range(5)
]
skill_2s_damage = [
    (0.90, 1.0, 0.05),
    (0.95, 1.0, 0.06),
    (1.00, 1.0, 0.07),
    (1.05, 1.0, 0.08),
    (1.10, 1.0, 0.09),
]

skill_3s = [
    (skill_3_tooltip, heal_stresses[2], disable_daze, unstealth, stuns[i], clear_charge, disease_quirk)
    for i in range(5)
]
skill_3s_damage = [
    (0.90, 3.0, 0.05),
    (0.95, 3.0, 0.06),
    (1.00, 3.0, 0.07),
    (1.05, 3.0, 0.08),
    (1.10, 3.0, 0.09),
]

explosion_anim = Animation(
    anim_dir="anim/explosion",
    anim_name=auto_name.new_anim(),
)
explosion_fx = Animation(
    anim_dir="fx/explosion",
    anim_name=auto_name.new_anim(),
)


def get_magic_skills(damage, effects, localization):
    skill = Skill(
        skill_name=auto_name.new_skill(),
        level=Level.ZERO,
        skill_type=SkillType.RANGED,
        launch=LAUNCH_34,
        target=ALL_ENEMY,
        atk=damage[0][0],
        dmg=damage[0][1],
        crit=damage[0][2],
        effect_ids=effects[0],
        localization=localization,
        image_path="combat_skill/arch_wizard.ability.five.png",
        anim=explosion_anim,
        fx=explosion_fx,
    )
    skills = [Skill(
        skill_name=auto_name.last_skill(),
        level=Level(i),
        skill_type=SkillType.RANGED,
        launch=LAUNCH_34,
        target=ALL_ENEMY,
        atk=damage[i][0],
        dmg=damage[i][1],
        crit=damage[i][2],
        effect_ids=effects[i],
    ) for i in range(1, 5)]
    skills.insert(0, skill)
    return skills


skill_1s = get_magic_skills(skill_1s_damage, skill_1s, "爆裂魔法·普通")
skill_2s = get_magic_skills(skill_2s_damage, skill_2s, "爆裂魔法·超级")
skill_3s = get_magic_skills(skill_3s_damage, skill_3s, "爆裂魔法·究极")

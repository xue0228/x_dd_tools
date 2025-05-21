from constants import skill_a_to_c
from xddtools.entries import Mode, Animation
from xddtools.entries.colour import invisible

modes_a = [Mode(
    is_raid_default=True if i == 0 else False,
    affliction_combat_skill_id=skill_a_to_c,
    battle_complete_combat_skill_id="move",
    actor_mode_name=f"普通形态-{i}充能",
    # str_skill_mode_info=f"{i}充能时：",
    str_skill_mode_info=f"",
    # str_skill_mode_info=f"{invisible('​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​​​​​​​​​​​﻿​​​​​')}",
    combat=Animation(anim_dir="anim/combat_a"),
    # defend=Animation(anim_dir="anim/defend_a"),
    riposte=Animation(anim_dir="anim/skill_a1"),
    battle_complete_sfx="audio/Scourge_SK7 {fa1467a6-b782-45c9-bf88-92ae1ac64bf6}.wav"
) for i in range(4)]

mode_b = Mode(
    affliction_combat_skill_id=skill_a_to_c,
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
    str_bark_override="我就是恐惧的化身！",
    combat=Animation(anim_dir="anim/combat_c"),
    # defend=Animation(anim_dir="anim/defend_c"),
    riposte=Animation(anim_dir="anim/skill_c2")
)

mode_base = Mode(
    afflicted=Animation(anim_dir="anim/afflicted"),
    camp=Animation(anim_dir="anim/camp"),
    heroic=Animation(anim_dir="anim/heroic"),
    idle=Animation(anim_dir="anim/idle"),
    investigate=Animation(anim_dir="anim/investigate"),
    defend=Animation(anim_dir="anim/defend"),
    walk=Animation(anim_dir="anim/walk")
)

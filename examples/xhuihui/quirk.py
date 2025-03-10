from effects import *
from xddtools.colour import notable
from xddtools.enums import QuirkTag
from xddtools.quirks import Quirk

huihui_quirk = Quirk(
    quirk_name=auto_name.new_quirk(),
    random_chance=0,
    tags=(QuirkTag.CANT_LOCK,),
    can_modify_in_activity=False,
    can_remove_with_camping_skill=False,
    can_be_replaced_by_new_quirk=False,
    buffs=(
        poison_h1,
        tag_h2,
        stun_h4,
        Buff(
            buff_name=auto_name.new_buff(),
            stat_type=BuffType.STRESS_DMG_RECEIVED_PERCENT,
            amount=0.5,
            has_description=False,
            is_clear_debuff_valid=False,
        )
    ),
    localization=(
        f'{notable("爆裂魔法·奥义")}',
        "毫无保留，一发，爽！"
    ),
)

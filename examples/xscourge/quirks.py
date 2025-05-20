from modes import mode_c
from xddtools.entries import Quirk, Buff, BuffRule
from xddtools.enum import QuirkTag, BuffType, STDisableCombatSkillAttribute, BuffRuleType

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

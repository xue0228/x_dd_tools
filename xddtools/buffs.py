from enum import Enum
from typing import Union, Optional

from xddtools.animation import Animation
from xddtools.base import BaseJsonData, BaseLocalization
from xddtools.buff_rules import BaseBuffRule, BRAlways
from xddtools.enums import BuffType, BuffDurationType, HealSource, STCombatStatMultiply, STCombatStatAdd, \
    STResistance, StressSource, STActivitySideEffectChance, STDisableCombatSkillAttribute


class Buff(BaseLocalization, BaseJsonData):
    def __init__(
            self,
            buff_name: str,
            stat_type: BuffType,
            stat_sub_type: Union[Enum, str] = "",
            amount: float = 1.0,
            duration_type: Optional[BuffDurationType] = None,
            duration: Optional[int] = None,
            has_description: bool = True,
            remove_on_battle_complete: bool = False,
            remove_if_not_active: bool = False,
            is_clear_debuff_valid: bool = True,
            buff_rule: Optional[BaseBuffRule] = None,
            fx: Union[Animation, str, None] = None,
            localization: Optional[str] = None
    ):
        self.stat_type = stat_type
        self.stat_sub_type = stat_sub_type
        self.amount = amount
        self.duration_type = duration_type
        self.duration = duration
        self.has_description = has_description
        self.remove_on_battle_complete = remove_on_battle_complete
        self.remove_if_not_active = remove_if_not_active
        self.is_clear_debuff_valid = is_clear_debuff_valid
        if buff_rule is None:
            buff_rule = BRAlways()
        self.buff_rule = buff_rule
        self.fx = fx
        super().__init__(
            name=buff_name,
            localization=localization,
            entry_id_prefix="buff_stat_tooltip_"
        )

        self.check_valid()

    @property
    def localization_id(self) -> Optional[str]:
        if self.stat_sub_type == "":
            return self.stat_type.value
        else:
            res = [
                self.stat_type.value,
                self.stat_sub_type.value if isinstance(self.stat_sub_type, Enum) else self.stat_sub_type
            ]
            return "_".join(res)

    def check_valid(self):
        assert isinstance(self.stat_type, BuffType), f"{self.stat_type}必须是BuffType"

        if self.stat_type in [
            BuffType.HP_HEAL_AMOUNT,
            BuffType.HP_HEAL_PERCENT,
            BuffType.HP_HEAL_RECEIVED_PERCENT
        ] and self.stat_sub_type != "":
            assert isinstance(self.stat_sub_type, HealSource), f"{self.stat_type}的stat_sub_type必须是HealSource"

        elif self.stat_type == BuffType.COMBAT_STAT_MULTIPLY:
            assert isinstance(self.stat_sub_type, STCombatStatMultiply), \
                f"{self.stat_type}的stat_sub_type必须是STCombatStatMultiply"

        elif self.stat_type == BuffType.COMBAT_STAT_ADD:
            assert isinstance(self.stat_sub_type, STCombatStatAdd), \
                f"{self.stat_type}的stat_sub_type必须是STCombatStatAdd"

        elif self.stat_type == BuffType.RESISTANCE:
            assert isinstance(self.stat_sub_type, STResistance), \
                f"{self.stat_type}的stat_sub_type必须是STResistance"

        elif self.stat_type in [
            BuffType.STRESS_DMG_PERCENT,
            BuffType.STRESS_DMG_RECEIVED_PERCENT,
            BuffType.STRESS_HEAL_PERCENT,
            BuffType.STRESS_HEAL_RECEIVED_PERCENT
        ] and self.stat_sub_type != "":
            assert isinstance(self.stat_sub_type, StressSource), f"{self.stat_type}的stat_sub_type必须是StressSource"

        elif self.stat_type == BuffType.UPGRADE_DISCOUNT:
            assert isinstance(self.stat_sub_type, str) and self.stat_sub_type != "", \
                f"{self.stat_type}的stat_sub_type不能为空，应为armour、weapon、combat_skill、camping_skill或其他自定义字符串"

        elif self.stat_type == BuffType.ACTIVITY_SIDE_EFFECT_CHANCE:
            assert isinstance(self.stat_sub_type, STActivitySideEffectChance), \
                f"{self.stat_type}的stat_sub_type必须是STActivitySideEffectChance"

        elif self.stat_type == BuffType.DISABLE_COMBAT_SKILL_ATTRIBUTE:
            assert isinstance(self.stat_sub_type, STDisableCombatSkillAttribute), \
                f"{self.stat_type}的stat_sub_type必须是STDisableCombatSkillAttribute"

        elif self.stat_type == BuffType.RIPOSTE:
            assert isinstance(self.stat_sub_type, str) and self.stat_sub_type != "", \
                f"{self.stat_type}的stat_sub_type不能为空，应为effect_ID"

        elif self.stat_type == BuffType.QUIRK_TAG_EVOLUTION_DURATION:
            assert isinstance(self.stat_sub_type, str) and self.stat_sub_type != "", \
                f"{self.stat_type}的stat_sub_type不能为空，应为Quirk Tag"

        else:
            assert self.stat_sub_type == "", \
                f"{self.stat_type}的stat_sub_type应为空字符串"

    # def generate_name(self) -> str:
    #     duration_type_short_form_table = {
    #         BuffDurationType.ROUND: "r",
    #         BuffDurationType.COMBAT_END: "ce",
    #         BuffDurationType.QUEST_END: "qe",
    #         BuffDurationType.QUEST_COMPLETE: "qc",
    #         BuffDurationType.QUEST_NOT_COMPLETE: "qn",
    #         BuffDurationType.ACTIVITY_END: "ae",
    #         BuffDurationType.IDLE_START_TOWN_VISIT: "i",
    #         BuffDurationType.TILL_REMOVE: "tr",
    #         BuffDurationType.NONE: "ne",
    #         BuffDurationType.BEFORE_TURN: "bt",
    #         BuffDurationType.AFTER_TURN: "at",
    #         BuffDurationType.AFTER_ROUND: "ar",
    #         None: "category"
    #     }
    #     res1 = [
    #         str_or_none_to_short_form_str(self.stat_type.value),
    #         str_or_none_to_short_form_str(
    #             self.stat_sub_type.value if isinstance(self.stat_sub_type, Enum) else self.stat_sub_type
    #         ),
    #         float_to_legal_str(self.amount)
    #     ]
    #     res2 = [
    #         duration_type_short_form_table[self.duration_type],
    #         int_or_none_to_str(self.duration)
    #     ]
    #     res3 = [
    #         str_or_none_to_short_form_str(self.buff_rule.rule_type),
    #         float_to_legal_str(self.buff_rule.rule_data_float),
    #         str_or_none_to_short_form_str(self.buff_rule.rule_data_string),
    #     ]
    #     res4 = [
    #         bool_to_short_form_str(self.has_description),
    #         bool_to_short_form_str(self.remove_on_battle_complete),
    #         bool_to_short_form_str(self.remove_if_not_active),
    #         bool_to_short_form_str(self.is_clear_debuff_valid),
    #         bool_to_short_form_str(self.buff_rule.is_false_rule)
    #     ]
    #     return "_".join([
    #         "_".join(res1), "".join(res2), "".join(res3), "".join(res4),
    #         str_or_none_to_short_form_str(
    #             os.path.split(self.fx.anim_dir)[1] if isinstance(self.fx, Animation) else self.fx
    #         )
    #     ])

    def dict(self):
        res = {
            "id": self.id,
            "stat_type": self.stat_type.value,
            "stat_sub_type": self.stat_sub_type.value if isinstance(self.stat_sub_type, Enum) else self.stat_sub_type,
            "amount": self.amount,
        }
        if self.duration_type is not None:
            res["duration_type"] = self.duration_type.value
        if self.duration is not None:
            res["duration"] = self.duration
        if not self.has_description:
            res["has_description"] = self.has_description
        if self.remove_on_battle_complete:
            res["remove_on_battle_complete"] = self.remove_on_battle_complete
        # if not self.remove_if_not_active:
        res["remove_if_not_active"] = self.remove_if_not_active
        if not self.is_clear_debuff_valid:
            res["is_clear_debuff_valid"] = self.is_clear_debuff_valid
        res.update(self.buff_rule.dict())
        if self.fx is not None:
            res["fx"] = self.fx.id if isinstance(self.fx, Animation) else self.fx
        return res


if __name__ == '__main__':
    b = Buff(
        "xue",
        BuffType.HP_HEAL_AMOUNT,
    )
    print(b.id)
    print(b)

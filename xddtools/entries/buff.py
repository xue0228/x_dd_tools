from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator

from xddtools.base import JsonData, AnimationEntry, BuffEntry, EffectEntry, QuirkEntry, Entry
from xddtools.base import get_entry_id
from xddtools.entries.buff_rule import BuffRule, BuffRuleType
from xddtools.enum.buff import BuffType, BuffDurationType, HealSource, STCombatStatMultiply, STCombatStatAdd, \
    STResistance, StressSource, STActivitySideEffectChance, STDisableCombatSkillAttribute
from xddtools.name import AutoName

_buff_rule_always = BuffRule(rule_type=BuffRuleType.ALWAYS)


class Buff(JsonData, BuffEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    stat_type: BuffType
    stat_sub_type: Union[Entry, Enum, str] = ""
    amount: float = 1.0
    duration_type: Optional[BuffDurationType] = None
    duration: Optional[int] = None
    has_description: bool = True
    remove_on_battle_complete: bool = False
    remove_if_not_active: bool = False
    is_clear_debuff_valid: bool = True
    buff_rule: BuffRule = Field(default_factory=lambda x: _buff_rule_always)
    fx: Union[AnimationEntry, str, None] = None
    buff_stat_tooltip: Optional[str] = None
    entry_id: str = Field(default_factory=lambda x: AutoName().new_buff(), frozen=True)

    def get_dict(self) -> dict:
        res = {
            "id": self.id(),
            "stat_type": self.stat_type.value,
            "stat_sub_type": get_entry_id(self.stat_sub_type),
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
        res["remove_if_not_active"] = self.remove_if_not_active
        if not self.is_clear_debuff_valid:
            res["is_clear_debuff_valid"] = self.is_clear_debuff_valid
        res.update(self.buff_rule.get_dict())
        if self.fx is not None:
            res["fx"] = get_entry_id(self.fx)
        return res

    @model_validator(mode="after")
    def _check_after(self):
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
            assert isinstance(self.stat_sub_type, (EffectEntry, str)) and self.stat_sub_type != "", \
                f"{self.stat_type}的stat_sub_type不能为空，应为EffectEntry或str"

        elif self.stat_type == BuffType.QUIRK_TAG_EVOLUTION_DURATION:
            assert isinstance(self.stat_sub_type, (QuirkEntry, str)) and self.stat_sub_type != "", \
                f"{self.stat_type}的stat_sub_type不能为空，应为QuirkEntry或str"

        else:
            assert self.stat_sub_type == "", \
                f"{self.stat_type}的stat_sub_type应为空字符串"

        return self


if __name__ == '__main__':
    z = Buff(stat_type=BuffType.TAG, entry_id="test")
    z2 = Buff(stat_type=BuffType.TAG_BLOCKED, entry_id="test")
    print(z == z2)

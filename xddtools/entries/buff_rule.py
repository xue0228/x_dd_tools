from enum import Enum
from typing import Optional, Union, Dict, Any

from pydantic import BaseModel, ConfigDict, model_validator

from xddtools.base import Entry, SkillEntry, QuirkEntry, ModeEntry, ItemEntry, JsonData, HeroEntry, MonsterEntry
from xddtools.base import get_entry_id
from xddtools.enum.buff_rule import ActorStatus, DungeonType, TownActivityType, MonsterType, QuirkType, MonsterClass, \
    ItemID, ItemType, HeroClass, BuffRuleType


class BuffRule(JsonData, BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    rule_type: BuffRuleType
    rule_data_float: Union[float, int] = 0
    rule_data_string: Union[Enum, Entry, str] = ""
    is_false_rule: bool = False
    rule_data_string_tooltip: Optional[str] = None

    def get_dict(self) -> dict:
        res = {"rule_type": self.rule_type.value, "is_false_rule": self.is_false_rule,
               "rule_data": {"float": self.rule_data_float, "string": get_entry_id(self.rule_data_string)}}
        return res

    @model_validator(mode="before")
    @classmethod
    def _check_before(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        rule_type = values["rule_type"]
        rule_data_float = values.get("rule_data_float", 0)
        rule_data_string = values.get("rule_data_string", "")
        rule_data_string_tooltip = values.get("rule_data_string_tooltip", None)

        if rule_type in [
            BuffRuleType.ALWAYS,
            BuffRuleType.RIPOSTE,
            BuffRuleType.RANGED_ONLY,
            BuffRuleType.MELEE_ONLY,
            BuffRuleType.FIRST_ROUND_ONLY,
            BuffRuleType.IN_CAMP,
            BuffRuleType.IN_ROOM,
            BuffRuleType.IN_CORRIDOR,
            BuffRuleType.AT_DEATHS_DOOR,
            BuffRuleType.VIRTUED,
            BuffRuleType.AFFLICTED,
            BuffRuleType.IN_VAMPIRE,
            BuffRuleType.TARGET_IS_VAMPIRE,
            BuffRuleType.WALKING_BACKWARDS,
            BuffRuleType.IN_GUARDED,
            BuffRuleType.TARGET_IS_GUARDED,
            BuffRuleType.IS_GUARDING,
            BuffRuleType.TARGET_IS_GUARDING,
            BuffRuleType.IS_STEALTHED,
            BuffRuleType.TARGET_IS_STEALTHED,
            BuffRuleType.NO_TRINKETS,
            BuffRuleType.ACTIVATED_LAST,
            BuffRuleType.ACTIVATED_FIRST,
            BuffRuleType.ON_DEATHS_DOOR_ENTER
        ]:
            assert rule_data_float == 0, f"{rule_type}的rule_data_float必须为0"
            assert rule_data_string == "", f"{rule_type}的rule_data_string必须为空"
            assert rule_data_string_tooltip is None, f"{rule_type}的rule_data_string_tooltip必须为空"
        elif rule_type in [
            BuffRuleType.SKILL,
            BuffRuleType.ACTOR_STATUS,
            BuffRuleType.IS_ACTOR_STATUS,
            BuffRuleType.IN_DUNGEON,
            BuffRuleType.IN_ACTIVITY,
            BuffRuleType.MONSTER_TYPE,
            BuffRuleType.ATTACKING_MONSTER_TYPE,
            BuffRuleType.HAS_QUIRK,
            BuffRuleType.ACTOR_BASE_CLASS,
            BuffRuleType.IN_MODE,
            BuffRuleType.HAS_ITEM_ID,
            BuffRuleType.HAS_ITEM_TYPE
        ]:
            assert rule_data_float == 0, f"{rule_type}的rule_data_float必须为0"

            if rule_type == BuffRuleType.SKILL:
                assert isinstance(rule_data_string, (SkillEntry, str)), \
                    f"{rule_type}的rule_data_string必须为SkillEntry或str"
            elif rule_type == BuffRuleType.ACTOR_STATUS:
                assert isinstance(rule_data_string, ActorStatus), \
                    f"{rule_type}的rule_data_string必须为ActorStatus"
            elif rule_type == BuffRuleType.IS_ACTOR_STATUS:
                assert isinstance(rule_data_string, ActorStatus), \
                    f"{rule_type}的rule_data_string必须为ActorStatus"
            elif rule_type == BuffRuleType.IN_DUNGEON:
                assert isinstance(rule_data_string, (DungeonType, str)), \
                    f"{rule_type}的rule_data_string必须为DungeonType或str"
            elif rule_type == BuffRuleType.IN_ACTIVITY:
                assert isinstance(rule_data_string, TownActivityType), \
                    f"{rule_type}的rule_data_string必须为TownActivityType"
            elif rule_type == BuffRuleType.MONSTER_TYPE:
                assert isinstance(rule_data_string, (MonsterType, str)), \
                    f"{rule_type}的rule_data_string必须为MonsterType或str"
            elif rule_type == BuffRuleType.ATTACKING_MONSTER_TYPE:
                assert isinstance(rule_data_string, (MonsterType, str)), \
                    f"{rule_type}的rule_data_string必须为MonsterType或str"
            elif rule_type == BuffRuleType.HAS_QUIRK:
                assert isinstance(rule_data_string, (QuirkType, QuirkEntry, str)), \
                    f"{rule_type}的rule_data_string必须为QuirkType或QuirkEntry或str"
            elif rule_type == BuffRuleType.ACTOR_BASE_CLASS:
                assert isinstance(rule_data_string, (MonsterClass, HeroClass, HeroEntry, MonsterEntry, str)), \
                    f"{rule_type}的rule_data_string必须为MonsterClass或HeroClass或或HeroEntry或MonsterEntry或str"
            elif rule_type == BuffRuleType.IN_MODE:
                assert isinstance(rule_data_string, (ModeEntry, str)), \
                    f"{rule_type}的rule_data_string必须为ModeEntry或str"
            elif rule_type == BuffRuleType.HAS_ITEM_ID:
                assert isinstance(rule_data_string, (ItemEntry, ItemID, str)), \
                    f"{rule_type}的rule_data_string必须为ItemEntry或ItemID或str"
            elif rule_type == BuffRuleType.HAS_ITEM_TYPE:
                assert isinstance(rule_data_string, (ItemType, str)), \
                    f"{rule_type}的rule_data_string必须为ItemType或str"
        elif rule_type in [
            BuffRuleType.MONSTER_SIZE,
            BuffRuleType.IN_RANK,
            BuffRuleType.HP_BELOW,
            BuffRuleType.HP_ABOVE,
            BuffRuleType.LIGHT_BELOW,
            BuffRuleType.LIGHT_ABOVE,
            BuffRuleType.TARGET_HP_BELOW,
            BuffRuleType.TARGET_HP_ABOVE,
        ]:
            assert rule_data_string == "", f"{rule_type}的rule_data_string必须为空"
            assert rule_data_string_tooltip is None, f"{rule_type}的rule_data_string_tooltip必须为空"

            if rule_type == BuffRuleType.MONSTER_SIZE:
                assert rule_data_float in [0, 1, 2, 3, 4], f"{rule_type}的rule_data_float必须在0,1,2,3,4中"
                values["rule_data_float"] = int(rule_data_float)
            elif rule_type == BuffRuleType.IN_RANK:
                assert rule_data_float in [0, 1, 2, 3], f"{rule_type}的rule_data_float必须在0,1,2,3中"
                values["rule_data_float"] = int(rule_data_float)
            else:
                assert rule_data_float >= 0, f"{rule_type}的rule_data_float必须大于等于0"
        else:
            if rule_type == BuffRuleType.MONSTER_TYPE_COUNT_MIN:
                assert rule_data_float in [1, 2, 3, 4], f"{rule_type}的rule_data_float必须在1,2,3,4中"
                assert isinstance(rule_data_string, (MonsterType, str)), \
                    f"{rule_type}的rule_data_string必须为MonsterType或str"
                values["rule_data_float"] = int(rule_data_float)
            else:
                raise ValueError(f"未知的rule_type: {rule_type}")

        return values


if __name__ == '__main__':
    x = BuffRule(
        rule_type=BuffRuleType.MONSTER_SIZE,
        rule_data_float=4
    )
    print(x)

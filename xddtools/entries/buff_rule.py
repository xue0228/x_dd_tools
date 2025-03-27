from enum import Enum
from typing import Optional, Union, Dict, Any

from pydantic import BaseModel, ConfigDict, model_validator

from xddtools.base import Entry, SkillEntry, QuirkEntry, ModeEntry, ItemEntry, JsonData, HeroEntry, MonsterEntry
from xddtools.base import get_entry_id
from xddtools.enum.buff_rule import ActorStatus, DungeonType, TownActivityType, MonsterType, QuirkType, MonsterClass, \
    ItemID, ItemType, HeroClass


class BuffRuleType(Enum):
    # 只需要 rule_type
    ALWAYS = "always"  # 常驻生效（大部分buff都是这个条件）
    RIPOSTE = "riposte"  # 触发自身反击后生效
    RANGED_ONLY = "rangedonly"  # 远程技能（ranged），在进攻者身上才能根据技能类型激活
    MELEE_ONLY = "meleeonly"  # 近战技能（melee），在进攻者身上才能根据技能类型激活
    FIRST_ROUND_ONLY = "firstroundonly"  # 场战斗的第一回合，更严格说是第一【整轮】即第一个“大回合”期间
    IN_CAMP = "in_camp"  # 扎营
    IN_ROOM = "in_room"  # 在房间
    IN_CORRIDOR = "in_corridor"  # 在走廊
    AT_DEATHS_DOOR = "at_deaths_door"  # 处于死门时
    VIRTUED = "virtued"  # 美德时
    AFFLICTED = "afflicted"  # 折磨时
    IN_VAMPIRE = "in_vampire"  # 有猩红诅咒时
    TARGET_IS_VAMPIRE = "target_is_vampire"  # 目标具有猩红诅咒时
    WALKING_BACKWARDS = "walking_backwards"  # 在走廊后退时
    IN_GUARDED = "in_guarded"  # 被守护
    TARGET_IS_GUARDED = "target_is_guarded"  # 目标被守护时
    IS_GUARDING = "is_guarding"  # 提供守护时
    TARGET_IS_GUARDING = "target_is_guarding"  # 目标是提供守护的单位
    IS_STEALTHED = "is_stealthed"  # 潜行时
    TARGET_IS_STEALTHED = "target_is_stealthed"  # 目标潜行时
    NO_TRINKETS = "no_trinkets"  # 自身没有佩戴任何饰品时
    ACTIVATED_LAST = "activated_last"  # 最后行动，马戏团专属buff,经测试在单机模式依然生效
    ACTIVATED_FIRST = "activated_first"  # 首先行动，马戏团专属buff,经测试在单机模式依然生效
    ON_DEATHS_DOOR_ENTER = "ondeathsdoorenter"  # 进入死门时（触发英雄info的死门进入代码时），由扣除生命值上限导致的进入死门，不会触发此rule

    # 需要 rule_type 和 string
    """
    对某个技能有效（非skill期间时，修饰的buff不会工作）（对反击技能不生效）
    """
    SKILL = "skill"

    """
    技能或effect的作用目标具有特定的状态时激活此rule修饰的buff
    此种buff在effect指向多个目标时，会根据每个目标单独判定
    因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，此buff将会单独【干涉】【符合rule的单位】的技能或effect流程
    经测试，dazed不可用
    """
    ACTOR_STATUS = "actorStatus"

    """
    for "if virtued/afflicted" use virtued or afflicted rules
    对于美德时和折磨时的状态，要使用美德时和折磨时的触发条件
    is_actor_status指对自身状态的判定
    经测试，dazed不可用
    在地牢探索中，此rule的判定时间是战斗内外，每时每刻
    """
    IS_ACTOR_STATUS = "is_actor_status"

    """
    副本（遗迹、海湾等，内容填入区域ID）
    """
    IN_DUNGEON = "in_dungeon"

    """
    城镇活动，冥想、赌博等
    """
    IN_ACTIVITY = "in_activity"

    """
    技能或effect的作用目标具有特定的monster type时激活此rule修饰的buff
    此种buff在effect指向多个目标时，会根据每个目标单独判定
    因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，此buff将会单独【干涉】【符合rule的单位】的技能或effect流程
    """
    MONSTER_TYPE = "monsterType"

    """
    【被】某类怪物攻击时
    attacking_monster_type为被某类怪物攻击时触发，属于防御型条件，
    配合防御是参与计算的buff（抗性、闪避、防御、伤害减免等）才有意义。
    """
    ATTACKING_MONSTER_TYPE = "attacking_monster_type"

    """
    有某个怪癖（疾病也可以）时
    """
    HAS_QUIRK = "has_quirk"

    """
    技能或effect的作用目标的id匹配时激活此rule修饰的buff，当反转目标时，buff挂在对方身上，id填自身的monster【大类id】或英雄职业id。
    此种buff在effect指向多个目标时，会根据每个目标单独判定，因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，
    此buff将会单独【干涉】【符合rule的单位】的技能或effect流程。
    """
    ACTOR_BASE_CLASS = "actor_base_class"

    """
    在某个模式下
    """
    IN_MODE = "in_mode"

    """
    背包内有某个物品时（如绷带、草药等）
    """
    HAS_ITEM_ID = "has_item_id"

    """
    背包内有某类物品时（如补给品、宝石等道具类别）
    """
    HAS_ITEM_TYPE = "has_item_type"

    # 需要 rule_type 和 float
    """
    技能或effect的作用目标的size（体型）【大于等于】特定值时激活此rule修饰的buff。此种buff在effect指向多个目标时，会根据每个目标单独判定
    因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，此buff将会单独【干涉】【符合rule的单位】的技能或effect流程
    怪物的info文件中，size可以写0，这种召唤物被称为“size0”，可以利用其召唤后的spawn: effect玩出很多花样，之后通过kill_enemy_types自灭即可
    注意：size0不显示大多数动画效果，死亡时可能触发老祖语音，在场上时常常会遮挡敌方4个位置中的一个，使得鼠标无法选中此位置，因此需要尽快自灭。
    注意：当行动结束后才会更新动画，而不结束回合的技能不会更新动画，这意味着在不结束回合的技能中，即使size0自灭，它仍然会因为动画未更新而遮挡区域
    """
    MONSTER_SIZE = "monsterSize"

    """
    站位：0，1，2，3
    注意该rule自0起，0才是一号位rank 1
    """
    IN_RANK = "in_rank"

    """
    below：低于百分比
    above:高于百分比
    """
    HP_BELOW = "hpbelow"
    HP_ABOVE = "hpabove"
    LIGHT_BELOW = "lightbelow"
    LIGHT_ABOVE = "lightabove"
    STRESS_BELOW = "stress_below"
    STRESS_ABOVE = "stress_above"
    TARGET_HP_ABOVE = "target_hpabove"
    TARGET_HP_BELOW = "target_hpbelow"

    # 需要 rule_type、string 和 float
    """
    例子：血裔的镜子
    这个是场上有血裔时携带者+4速的buff
    {
        "id" : "cc_trinket_speed_vs_vamps",
        "stat_type" : "combat_stat_add",
        "stat_sub_type" : "speed_rating",
        "amount" : 4,
        "remove_if_not_active" : false,
        "rule_type" : "monster_type_count_min",
        "is_false_rule" : false,
        "rule_data" : {
            "float" : 1,         这里写怪物的最少个数（别写0，写0这辈子都不生效）
            "string" : "vampire" 这里写怪物类型
        }
    },
    注意一点：
    1.attacking_monster_type为被某类怪物攻击时触发，属于防御型条件，
    配合防御是参与计算的buff（抗性、闪避、防御、伤害减免等）才有意义。
    2.monster_type_count_min为场上有某类怪时触发，属于条件向buff，
    其他buff都能使用该条件，但速度buff尤其适合使用该条件。
    3.monster_type_count_min在怪物侧不适用（详见本表标题）
    4.monster_type_count_min不会计算size为0的单位
    因速度判定是每个大回合（火把里的数字）开始，而不是挨打或者进攻，哪怕速度真的配其他两个有效，你也只有攻击和挨打瞬间提速，无法影响大回合开始，导致提速等于没提。
    """
    MONSTER_TYPE_COUNT_MIN = "monster_type_count_min"


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

from typing import Union, Optional

from xddtools.base import BaseLocalization, BaseID
from xddtools.enums import ActorStatus, DungeonID, TownActivityType, MonsterType, QuirkType, MonsterClass, HeroClass, \
    ItemID, ItemType


class BaseBuffRule(BaseLocalization):
    """
    Buff Rules（buff触发条件）
    rule当有【判定目标】时，举例skill rule在skill执行期间才有【判定目标】，此时，依据判定和反转，结果可以为真或假。
    当rule没有【判定目标】，或特定rule在英雄/怪物侧不适用时，代码呈现不合法（null），结果视为假，且null无法通过反转变为真。
    """

    def __init__(
            self,
            rule_type: str,
            rule_data_float: Union[float, int] = 0,
            rule_data_string: str = "",
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        self.rule_type = rule_type
        self.is_false_rule = is_false_rule
        self.rule_data_float = rule_data_float
        self.rule_data_string = rule_data_string
        super().__init__(
            name="",
            localization=localization,
            entry_id_prefix="buff_rule_data_tooltip_"
        )

    @property
    def localization_id(self) -> Optional[str]:
        if self.rule_data_string == "":
            return None
        else:
            return self.rule_data_string

    def dict(self):
        res = {"rule_type": self.rule_type, "is_false_rule": self.is_false_rule,
               "rule_data": {"float": self.rule_data_float, "string": self.rule_data_string}}
        return res

    def __str__(self):
        return self.dict().__str__()


# 只需要 rule_type

class BRAlways(BaseBuffRule):
    """
    常驻生效（大部分buff都是这个条件）
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("always", 0, "", is_false_rule, localization)


class BRRiposte(BaseBuffRule):
    """
    触发自身反击后生效
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("riposte", 0, "", is_false_rule, localization)


class BRRangedOnly(BaseBuffRule):
    """
    远程技能（ranged）
    在进攻者身上才能根据技能类型激活
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("rangedonly", 0, "", is_false_rule, localization)


class BRMeleeOnly(BaseBuffRule):
    """
    近战技能（melee）
    在进攻者身上才能根据技能类型激活
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("meleeonly", 0, "", is_false_rule, localization)


class BRFirstRoundOnly(BaseBuffRule):
    """
    每场战斗的第一回合
    更严格说是第一【整轮】即第一个“大回合”期间
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("firstroundonly", 0, "", is_false_rule, localization)


class BRInCamp(BaseBuffRule):
    """
    扎营
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("in_camp", 0, "", is_false_rule, localization)


class BRInRoom(BaseBuffRule):
    """
    在房间
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("in_room", 0, "", is_false_rule, localization)


class BRInCorridor(BaseBuffRule):
    """
    在走廊
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("in_corridor", 0, "", is_false_rule, localization)


class BRAtDeathsDoor(BaseBuffRule):
    """
    处于死门时
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("at_deaths_door", 0, "", is_false_rule, localization)


class BRVirtued(BaseBuffRule):
    """
    美德时
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("virtued", 0, "", is_false_rule, localization)


class BRAfflicted(BaseBuffRule):
    """
    折磨时
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("afflicted", 0, "", is_false_rule, localization)


class BRIsVampire(BaseBuffRule):
    """
    有猩红诅咒时
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("is_vampire", 0, "", is_false_rule, localization)


class BRTargetIsVampire(BaseBuffRule):
    """
    目标具有猩红诅咒时
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("target_is_vampire", 0, "", is_false_rule, localization)


class BRWalkingBackwards(BaseBuffRule):
    """
    在走廊后退时
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("walking_backwards", 0, "", is_false_rule, localization)


class BRIsGuarded(BaseBuffRule):
    """
    被守护
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("is_guarded", 0, "", is_false_rule, localization)


class BRTargetIsGuarded(BaseBuffRule):
    """
    目标被守护时
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("target_is_guarded", 0, "", is_false_rule, localization)


class BRIsGuarding(BaseBuffRule):
    """
    提供守护时
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("is_guarding", 0, "", is_false_rule, localization)


class BRTargetIsGuarding(BaseBuffRule):
    """
    目标是提供守护的单位
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("target_is_guarding", 0, "", is_false_rule, localization)


class BRIsStealthed(BaseBuffRule):
    """
    潜行时
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("is_stealthed", 0, "", is_false_rule, localization)


class BRTargetIsStealthed(BaseBuffRule):
    """
    目标潜行时
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("target_is_stealthed", 0, "", is_false_rule, localization)


class BRNoTrinkets(BaseBuffRule):
    """
    自身没有佩戴任何饰品时
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("no_trinkets", 0, "", is_false_rule, localization)


class BRActivatedLast(BaseBuffRule):
    """
    最后行动
    马戏团专属buff,经测试在单机模式依然生效
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("activated_last", 0, "", is_false_rule, localization)


class BRActivatedFirst(BaseBuffRule):
    """
    首先行动
    马戏团专属buff,经测试在单机模式依然生效
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("activated_first", 0, "", is_false_rule, localization)


class BROnDeathsDoorEnter(BaseBuffRule):
    """
    进入死门时（触发英雄info的死门进入代码时）
    由扣除生命值上限导致的进入死门，不会触发此rule
    """

    def __init__(
            self,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("ondeathsdoorenter", 0, "", is_false_rule, localization)


# 需要 rule_type 和 string

class BRSkill(BaseBuffRule):
    """
    对某个技能有效（非skill期间时，修饰的buff不会工作）（对反击技能不生效）
    """

    def __init__(
            self,
            skill_id: str,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("skill", 0, skill_id, is_false_rule, localization)


class BRActorStatus(BaseBuffRule):
    """
    技能或effect的作用目标具有特定的状态时激活此rule修饰的buff
    此种buff在effect指向多个目标时，会根据每个目标单独判定
    因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，此buff将会单独【干涉】【符合rule的单位】的技能或effect流程
    经测试，dazed不可用
    """

    def __init__(
            self,
            actor_status: ActorStatus,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("actorStatus", 0, actor_status.value, is_false_rule, localization)


class BRIsActorStatus(BaseBuffRule):
    """
    for "if virtued/afflicted" use virtued or afflicted rules
    对于美德时和折磨时的状态，要使用美德时和折磨时的触发条件
    is_actor_status指对自身状态的判定
    经测试，dazed不可用
    在地牢探索中，此rule的判定时间是战斗内外，每时每刻
    """

    def __init__(
            self,
            actor_status: ActorStatus,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("is_actor_status", 0, actor_status.value, is_false_rule, localization)


class BRInDungeon(BaseBuffRule):
    """
    副本（遗迹、海湾等，内容填入区域ID）
    """

    def __init__(
            self,
            dungeon_id: Union[DungeonID, str],
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if isinstance(dungeon_id, DungeonID):
            dungeon_id = dungeon_id.value
        super().__init__("in_dungeon", 0, dungeon_id, is_false_rule, localization)


class BRInActivity(BaseBuffRule):
    """
    城镇活动，冥想、赌博等
    """

    def __init__(
            self,
            activity_type: TownActivityType,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("in_activity", 0, activity_type.value, is_false_rule, localization)


class BRMonsterType(BaseBuffRule):
    """
    技能或effect的作用目标具有特定的monster type时激活此rule修饰的buff
    此种buff在effect指向多个目标时，会根据每个目标单独判定
    因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，此buff将会单独【干涉】【符合rule的单位】的技能或effect流程
    """

    def __init__(
            self,
            monster_type: Union[MonsterType, str],
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if isinstance(monster_type, MonsterType):
            monster_type = monster_type.value
        super().__init__("monsterType", 0, monster_type, is_false_rule, localization)


class BRAttackingMonsterType(BaseBuffRule):
    """
    【被】某类怪物攻击时
    attacking_monster_type为被某类怪物攻击时触发，属于防御型条件，
    配合防御是参与计算的buff（抗性、闪避、防御、伤害减免等）才有意义。
    """

    def __init__(
            self,
            monster_type: Union[MonsterType, str],
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if isinstance(monster_type, MonsterType):
            monster_type = monster_type.value
        super().__init__("attacking_monster_type", 0, monster_type, is_false_rule, localization)


class BRHasQuirk(BaseBuffRule):
    """
    有某个怪癖（疾病也可以）时
    """

    def __init__(
            self,
            quirk_id: Union[BaseID, QuirkType, str],
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if isinstance(quirk_id, QuirkType):
            quirk_id = quirk_id.value
        elif isinstance(quirk_id, BaseID):
            quirk_id = quirk_id.id
        super().__init__("has_quirk", 0, quirk_id, is_false_rule, localization)


class BRActorBaseClass(BaseBuffRule):
    """
    技能或effect的作用目标的id匹配时激活此rule修饰的buff，当反转目标时，buff挂在对方身上，id填自身的monster【大类id】或英雄职业id。
    此种buff在effect指向多个目标时，会根据每个目标单独判定，因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，
    此buff将会单独【干涉】【符合rule的单位】的技能或effect流程。
    """

    def __init__(
            self,
            monster_or_hero_class: Union[MonsterClass, HeroClass, str],
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if isinstance(monster_or_hero_class, MonsterClass):
            monster_or_hero_class = monster_or_hero_class.value
        elif isinstance(monster_or_hero_class, HeroClass):
            monster_or_hero_class = monster_or_hero_class.value
        super().__init__("actor_base_class", 0, monster_or_hero_class, is_false_rule, localization)


class BRInMode(BaseBuffRule):
    """
    在某个模式下
    """

    def __init__(
            self,
            mode_id,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        super().__init__("in_mode", 0, mode_id, is_false_rule, localization)


class BRHasItemId(BaseBuffRule):
    """
    背包内有某个物品时（如绷带、草药等）
    """

    def __init__(
            self,
            item_id: Union[ItemID, str],
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if isinstance(item_id, ItemID):
            item_id = item_id.value
        super().__init__("has_item_id", 0, item_id, is_false_rule, localization)


class BRHasItemType(BaseBuffRule):
    """
    背包内有某类物品时（如补给品、宝石等道具类别）
    """

    def __init__(
            self,
            item_type: Union[ItemType, str],
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if isinstance(item_type, ItemType):
            item_type = item_type.value
        super().__init__("has_item_type", 0, item_type, is_false_rule, localization)


# 需要 rule_type 和 float

class BRMonsterSize(BaseBuffRule):
    """
    技能或effect的作用目标的size（体型）【大于等于】特定值时激活此rule修饰的buff。此种buff在effect指向多个目标时，会根据每个目标单独判定
    因而，携带被此rule修饰的buff，执行对多个单位生效的技能或effect，此buff将会单独【干涉】【符合rule的单位】的技能或effect流程
    怪物的info文件中，size可以写0，这种召唤物被称为“size0”，可以利用其召唤后的spawn: effect玩出很多花样，之后通过kill_enemy_types自灭即可
    注意：size0不显示大多数动画效果，死亡时可能触发老祖语音，在场上时常常会遮挡敌方4个位置中的一个，使得鼠标无法选中此位置，因此需要尽快自灭。
    注意：当行动结束后才会更新动画，而不结束回合的技能不会更新动画，这意味着在不结束回合的技能中，即使size0自灭，它仍然会因为动画未更新而遮挡区域
    """

    def __init__(
            self,
            monster_size: int,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if monster_size < 0:
            raise ValueError("Monster size must be greater than or equal to 0")
        super().__init__("monsterSize", monster_size, "", is_false_rule, localization)


class BRInRank(BaseBuffRule):
    """
    站位：0，1，2，3
    注意该rule自0起，0才是一号位rank 1
    """

    def __init__(
            self,
            rank: int,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if rank < 0 or rank > 3:
            raise ValueError("Rank must be between 0 and 3")
        super().__init__("in_rank", rank, "", is_false_rule, localization)


class BRHpBelow(BaseBuffRule):
    """
    below：低于百分比
    above:高于百分比
    """

    def __init__(
            self,
            value: float,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1")
        super().__init__("hpbelow", value, "", is_false_rule, localization)


class BRHpAbove(BaseBuffRule):
    """
    below：低于百分比
    above:高于百分比
    """

    def __init__(
            self,
            value: float,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1")
        super().__init__("hpabove", value, "", is_false_rule, localization)


class BRLightBelow(BaseBuffRule):
    """
    below：低于百分比
    above:高于百分比
    """

    def __init__(
            self,
            value: float,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1")
        super().__init__("lightbelow", value, "", is_false_rule, localization)


class BRLightAbove(BaseBuffRule):
    """
    below：低于百分比
    above:高于百分比
    """

    def __init__(
            self,
            value: float,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1")
        super().__init__("lightabove", value, "", is_false_rule, localization)


class BRStressBelow(BaseBuffRule):
    """
    below：低于百分比
    above:高于百分比
    怪物侧没有压力，此对rule不成立
    """

    def __init__(
            self,
            value: float,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1")
        super().__init__("stress_below", value, "", is_false_rule, localization)


class BRStressAbove(BaseBuffRule):
    """
    below：低于百分比
    above:高于百分比
    怪物侧没有压力，此对rule不成立
    """

    def __init__(
            self,
            value: float,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1")
        super().__init__("stress_above", value, "", is_false_rule, localization)


class BRTargetHpAbove(BaseBuffRule):
    """
    目标生命值高于设定数值触发
    """

    def __init__(
            self,
            hp: float,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if hp < 0:
            raise ValueError("HP must be greater than or equal to 0")
        super().__init__("target_hpabove", hp, "", is_false_rule, localization)


class BRTargetHpBelow(BaseBuffRule):
    """
    目标生命值低于设定数值触发
    """

    def __init__(
            self,
            hp: float,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if hp < 0:
            raise ValueError("HP must be greater than or equal to 0")
        super().__init__("target_hpbelow", hp, "", is_false_rule, localization)


# 需要 rule_type、string 和 float

class BRMonsterTypeCountMin(BaseBuffRule):
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

    def __init__(
            self,
            monster_type: Union[MonsterType, str],
            number: int,
            is_false_rule: bool = False,
            localization: Optional[str] = None
    ):
        if number < 1:
            raise ValueError("Number must be greater than or equal to 1")
        if isinstance(monster_type, MonsterType):
            monster_type = monster_type.value
        super().__init__("monster_type_count_min", number, monster_type, is_false_rule, localization)


if __name__ == '__main__':
    print(BaseBuffRule("always"))
    print(BRAlways())

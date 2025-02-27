import math
from copy import deepcopy
from typing import Optional, Iterable, Dict, Tuple

import numpy as np

from xddtools.enums import Level, UpgradeRequirementCode
from xddtools.utils import float_to_percent_str, bool_to_lower_str, clamp_string


class Resistance:
    """
    角色抗性，此处设定的值为 1 级英雄的抗性值，
    随着英雄等级的提升，每级都会增加 10% 全抗。
    也就是说 6 级英雄即使初始抗性为 0%，也会有至少 50% 全抗。
    官方角色基础抗性参考：
    abomination  : .stun 40% .poison 60% .bleed 30% .disease 20% .move 40% .debuff 20% .death_blow 67% .trap 10%
    antiquarian  : .stun 20% .poison 20% .bleed 20% .disease 20% .move 20% .debuff 20% .death_blow 67% .trap 10%
    arbalest     : .stun 40% .poison 30% .bleed 30% .disease 30% .move 40% .debuff 30% .death_blow 67% .trap 10%
    bounty_hunter: .stun 40% .poison 30% .bleed 30% .disease 20% .move 40% .debuff 30% .death_blow 67% .trap 40%
    crusader     : .stun 40% .poison 30% .bleed 30% .disease 30% .move 40% .debuff 30% .death_blow 67% .trap 10%
    grave_robber : .stun 20% .poison 50% .bleed 30% .disease 30% .move 20% .debuff 30% .death_blow 67% .trap 50%
    hellion      : .stun 40% .poison 40% .bleed 40% .disease 30% .move 40% .debuff 30% .death_blow 67% .trap 20%
    highwayman   : .stun 30% .poison 30% .bleed 30% .disease 30% .move 30% .debuff 30% .death_blow 67% .trap 40%
    houndmaster  : .stun 40% .poison 40% .bleed 40% .disease 30% .move 40% .debuff 30% .death_blow 67% .trap 40%
    jester       : .stun 20% .poison 40% .bleed 30% .disease 20% .move 20% .debuff 40% .death_blow 67% .trap 30%
    leper        : .stun 60% .poison 40% .bleed 10% .disease 20% .move 60% .debuff 40% .death_blow 67% .trap 10%
    man_at_arms  : .stun 40% .poison 30% .bleed 40% .disease 30% .move 40% .debuff 30% .death_blow 67% .trap 10%
    occultist    : .stun 20% .poison 30% .bleed 40% .disease 40% .move 20% .debuff 60% .death_blow 67% .trap 10%
    plague_doctor: .stun 20% .poison 60% .bleed 20% .disease 50% .move 20% .debuff 50% .death_blow 67% .trap 20%
    vestal       : .stun 30% .poison 30% .bleed 40% .disease 30% .move 30% .debuff 30% .death_blow 67% .trap 10%
    """

    def __init__(
            self,
            stun: float,
            poison: float,
            bleed: float,
            disease: float,
            move: float,
            debuff: float,
            death_blow: float,
            trap: float,
    ):
        """
        初始化
        :param stun: 眩晕
        :param poison: 腐蚀
        :param bleed: 流血
        :param disease: 疾病
        :param move: 位移
        :param debuff: 减益
        :param death_blow: 致死
        :param trap: 陷阱
        """
        self.stun = stun
        self.poison = poison
        self.bleed = bleed
        self.disease = disease
        self.move = move
        self.debuff = debuff
        self.death_blow = death_blow
        self.trap = trap

    def __str__(self):
        return f"resistances: .stun {float_to_percent_str(self.stun)}% " \
               f".poison {float_to_percent_str(self.poison)}% " \
               f".bleed {float_to_percent_str(self.bleed)}% " \
               f".disease {float_to_percent_str(self.disease)}% " \
               f".move {float_to_percent_str(self.move)}% " \
               f".debuff {float_to_percent_str(self.debuff)}% " \
               f".death_blow {float_to_percent_str(self.death_blow)}% " \
               f".trap {float_to_percent_str(self.trap)}%\n"


class Weapon:
    """
    武器属性，官方角色的武器一般只提供伤害、暴击和速度。
    官方角色武器属性参考：
    weapon: .name "abomination_weapon_0"   .atk 0% .dmg  6 11 .crit  2% .spd 7
    weapon: .name "abomination_weapon_4"   .atk 0% .dmg 11 20 .crit  6% .spd 9

    weapon: .name "antiquarian_weapon_0"   .atk 0% .dmg  3  5 .crit  1% .spd 5
    weapon: .name "antiquarian_weapon_4"   .atk 0% .dmg  5  9 .crit  5% .spd 7

    weapon: .name "arbalest_weapon_0"      .atk 0% .dmg  4  8 .crit  6% .spd 3
    weapon: .name "arbalest_weapon_4"      .atk 0% .dmg  7 14 .crit 10% .spd 5

    weapon: .name "bounty_hunter_weapon_0" .atk 0% .dmg  5 10 .crit  4% .spd 5
    weapon: .name "bounty_hunter_weapon_4" .atk 0% .dmg  8 16 .crit  8% .spd 7

    weapon: .name "crusader_weapon_0"      .atk 0% .dmg  6 12 .crit  3% .spd 1
    weapon: .name "crusader_weapon_4"      .atk 0% .dmg 10 19 .crit  7% .spd 3

    weapon: .name "grave_robber_weapon_0"  .atk 0% .dmg  4  8 .crit  6% .spd 8
    weapon: .name "grave_robber_weapon_4"  .atk 0% .dmg  7 14 .crit 10% .spd 10

    weapon: .name "hellion_weapon_0"       .atk 0% .dmg  6 12 .crit  5% .spd 4
    weapon: .name "hellion_weapon_4"       .atk 0% .dmg 10 19 .crit  9% .spd 6

    weapon: .name "highwayman_weapon_0"    .atk 0% .dmg  5 10 .crit  5% .spd 5
    weapon: .name "highwayman_weapon_4"    .atk 0% .dmg  9 16 .crit  9% .spd 7

    weapon: .name "houndmaster_weapon_0"   .atk 0% .dmg  4  7 .crit  4% .spd 5
    weapon: .name "houndmaster_weapon_4"   .atk 0% .dmg  7 13 .crit  8% .spd 7

    weapon: .name "jester_weapon_0"        .atk 0% .dmg  4  7 .crit  4% .spd 7
    weapon: .name "jester_weapon_4"        .atk 0% .dmg  7 13 .crit  8% .spd 9

    weapon: .name "leper_weapon_0"         .atk 0% .dmg  8 16 .crit  1% .spd 2
    weapon: .name "leper_weapon_4"         .atk 0% .dmg 13 26 .crit  5% .spd 4

    weapon: .name "man_at_arms_weapon_0"   .atk 0% .dmg  5  9 .crit  2% .spd 3
    weapon: .name "man_at_arms_weapon_4"   .atk 0% .dmg  8 14 .crit  6% .spd 5

    weapon: .name "occultist_weapon_0"     .atk 0% .dmg  4  7 .crit  6% .spd 6
    weapon: .name "occultist_weapon_4"     .atk 0% .dmg  7 13 .crit 10% .spd 8

    weapon: .name "plague_doctor_weapon_0" .atk 0% .dmg  4  7 .crit  2% .spd 7
    weapon: .name "plague_doctor_weapon_4" .atk 0% .dmg  7 13 .crit  6% .spd 9

    weapon: .name "vestal_weapon_0"        .atk 0% .dmg  4  8 .crit  1% .spd 4
    weapon: .name "vestal_weapon_4"        .atk 0% .dmg  7 14 .crit  5% .spd 6
    """

    def __init__(
            self,
            level: Level,
            attack: float,
            damage_low: int,
            damage_high: int,
            critical_rate: float,
            speed: int,
            upgrade_requirement_code: Optional[UpgradeRequirementCode] = None,
            hero_name: Optional[str] = None,
    ):
        """
        初始化
        :param level: 等级
        :param attack: 精准修正
        :param damage_low: 基础伤害下限
        :param damage_high: 基础伤害上限
        :param critical_rate: 暴击率
        :param speed: 速度
        :param upgrade_requirement_code: 解锁该属性所需的装备等级
        举例：
            weapon: .name "antiquarian_weapon_0" .atk 0% .dmg 3 5 .crit 1% .spd 5
            weapon: .name "antiquarian_weapon_1" .atk 0% .dmg 4 6 .crit 2% .spd 5 .upgradeRequirementCode 0
            weapon: .name "antiquarian_weapon_2" .atk 0% .dmg 4 7 .crit 3% .spd 6 .upgradeRequirementCode 0
            weapon: .name "antiquarian_weapon_3" .atk 0% .dmg 5 8 .crit 4% .spd 6 .upgradeRequirementCode 0
            weapon: .name "antiquarian_weapon_4" .atk 0% .dmg 5 9 .crit 5% .spd 7 .upgradeRequirementCode 0
            这种情况下只需要在铁匠铺升级一次装备就可以直接获得"antiquarian_weapon_4"对应的装备属性
        :param hero_name: 所属英雄名称
        """
        if damage_low > damage_high:
            raise ValueError(f"damage_low must be not more than damage_high,"
                             f"but get {damage_low} and {damage_high}")
        if hero_name is None:
            hero_name = ""
        self.hero_name = hero_name
        self.level = level
        self.attack = attack
        self.damage_low = damage_low
        self.damage_high = damage_high
        self.critical_rate = critical_rate
        self.speed = speed
        self.upgrade_requirement_code = upgrade_requirement_code

    def __str__(self):
        res = f'weapon: .name "{self.hero_name}_weapon_{self.level.value}" ' \
              f'.atk {float_to_percent_str(self.attack)}% ' \
              f'.dmg {self.damage_low} {self.damage_high} ' \
              f'.crit {float_to_percent_str(self.critical_rate)}% ' \
              f'.spd {self.speed}'
        if self.level != Level.ZERO:
            if self.upgrade_requirement_code is None:
                res += f' .upgradeRequirementCode {self.level.value - 1}'
            else:
                res += f' .upgradeRequirementCode {self.upgrade_requirement_code.value}'
        return res + "\n"


class Armour:
    """
    护甲属性，官方角色的护甲一般只提供闪避和最大生命。
    官方角色护甲属性参考：
    armour: .name "abomination_armour_0"   .def  7.5% .prot 0 .hp 26 .spd 0
    armour: .name "abomination_armour_4"   .def 27.5% .prot 0 .hp 46 .spd 0

    armour: .name "antiquarian_armour_0"   .def   10% .prot 0 .hp 17 .spd 0
    armour: .name "antiquarian_armour_4"   .def   30% .prot 0 .hp 29 .spd 0

    armour: .name "arbalest_armour_0"      .def    0% .prot 0 .hp 27 .spd 0
    armour: .name "arbalest_armour_4"      .def   20% .prot 0 .hp 47 .spd 0

    armour: .name "bounty_hunter_armour_0" .def    5% .prot 0 .hp 25 .spd 0
    armour: .name "bounty_hunter_armour_4" .def   25% .prot 0 .hp 45 .spd 0

    armour: .name "crusader_armour_0"      .def    5% .prot 0 .hp 33 .spd 0
    armour: .name "crusader_armour_4"      .def   25% .prot 0 .hp 61 .spd 0

    armour: .name "grave_robber_armour_0"  .def   10% .prot 0 .hp 20 .spd 0
    armour: .name "grave_robber_armour_4"  .def   30% .prot 0 .hp 36 .spd 0

    armour: .name "hellion_armour_0"       .def   10% .prot 0 .hp 26 .spd 0
    armour: .name "hellion_armour_4"       .def   30% .prot 0 .hp 46 .spd 0

    armour: .name "highwayman_armour_0"    .def   10% .prot 0 .hp 23 .spd 0
    armour: .name "highwayman_armour_4"    .def   30% .prot 0 .hp 43 .spd 0

    armour: .name "houndmaster_armour_0"   .def   10% .prot 0 .hp 21 .spd 0
    armour: .name "houndmaster_armour_4"   .def   30% .prot 0 .hp 37 .spd 0

    armour: .name "jester_armour_0"        .def   15% .prot 0 .hp 19 .spd 0
    armour: .name "jester_armour_4"        .def   35% .prot 0 .hp 35 .spd 0

    armour: .name "leper_armour_0"         .def    0% .prot 0 .hp 35 .spd 0
    armour: .name "leper_armour_4"         .def   20% .prot 0 .hp 63 .spd 0

    armour: .name "man_at_arms_armour_0"   .def    5% .prot 0 .hp 31 .spd 0
    armour: .name "man_at_arms_armour_4"   .def   25% .prot 0 .hp 55 .spd 0

    armour: .name "occultist_armour_0"     .def   10% .prot 0 .hp 19 .spd 0
    armour: .name "occultist_armour_4"     .def   30% .prot 0 .hp 35 .spd 0

    armour: .name "plague_doctor_armour_0" .def    0% .prot 0 .hp 22 .spd 0
    armour: .name "plague_doctor_armour_4" .def   20% .prot 0 .hp 38 .spd 0

    armour: .name "vestal_armour_0"        .def    0% .prot 0 .hp 24 .spd 0
    armour: .name "vestal_armour_4"        .def   20% .prot 0 .hp 44 .spd 0
    """

    def __init__(
            self,
            level: Level,
            defense: float,
            protection: float,
            hp: int,
            speed: int,
            upgrade_requirement_code: Optional[UpgradeRequirementCode] = None,
            hero_name: Optional[str] = None,
    ):
        """
        初始化
        :param level: 等级
        :param defense: 闪避
        :param protection: 防御
        :param hp: 最大生命
        :param speed: 速度
        :param upgrade_requirement_code: 解锁该属性所需的装备等级
        :param hero_name: 所属英雄名称
        """
        if hero_name is None:
            hero_name = ""
        self.hero_name = hero_name
        self.level = level
        self.defense = defense
        self.protection = protection
        self.hp = hp
        self.speed = speed
        self.upgrade_requirement_code = upgrade_requirement_code

    def __str__(self):
        res = f'armour: .name "{self.hero_name}_armour_{self.level.value}" ' \
              f'.def {float_to_percent_str(self.defense)}% ' \
              f'.prot {float_to_percent_str(self.protection)}% ' \
              f'.hp {self.hp} .spd {self.speed}'
        if self.level != Level.ZERO:
            if self.upgrade_requirement_code is None:
                res += f' .upgradeRequirementCode {self.level.value - 1}'
            else:
                res += f' .upgradeRequirementCode {self.upgrade_requirement_code.value}'
        return res + "\n"


class WeaponGroup:
    def __init__(
            self,
            weapons: Optional[Iterable[Weapon]] = None,
            hero_name: Optional[str] = None,
    ):
        if hero_name is None:
            hero_name = ""
        self.hero_name = hero_name
        self.weapons: Dict[Level, Optional[Weapon]] = {
            Level.ZERO: None,
            Level.ONE: None,
            Level.TWO: None,
            Level.THREE: None,
            Level.FOUR: None
        }
        if weapons is not None:
            self.add_weapons(weapons)

    def add_weapon(self, weapon: Weapon):
        weapon = deepcopy(weapon)
        weapon.hero_name = self.hero_name
        self.weapons[weapon.level] = weapon

    def add_weapons(self, weapons: Iterable[Weapon]):
        for weapon in weapons:
            self.add_weapon(weapon)

    def autocomplete(self):
        """
        自动补全中间等级的武器属性，特殊需求的 upgradeRequirementCode 属性需要手动设置
        :return:
        """
        if self.weapons[Level.ZERO] is None or self.weapons[Level.FOUR] is None:
            raise ValueError('weapon group must have 0 and 4 level weapons')
        x = []
        target_x = []
        atk = []
        dmg_low = []
        dmg_high = []
        crit = []
        spd = []
        for k, v in self.weapons.items():
            if v is not None:
                x.append(k.value)
                atk.append(v.attack)
                dmg_low.append(v.damage_low)
                dmg_high.append(v.damage_high)
                crit.append(v.critical_rate)
                spd.append(v.speed)
            else:
                target_x.append(k.value)
        if len(target_x) == 0:
            return
        target_atk = np.interp(target_x, x, atk)
        target_dmg_low = np.interp(target_x, x, dmg_low)
        target_dmg_high = np.interp(target_x, x, dmg_high)
        target_crit = np.interp(target_x, x, crit)
        target_spd = np.interp(target_x, x, spd)

        for i in range(len(target_x)):
            self.add_weapon(Weapon(
                level=Level(target_x[i]),
                attack=target_atk[i],
                damage_low=round(target_dmg_low[i]),
                damage_high=round(target_dmg_high[i]),
                critical_rate=target_crit[i],
                # 一般第一次升级后速度并不会改变，所以这里向下取整
                speed=round(target_spd[i]) if target_x[i] != 1 else math.floor(target_spd[i])
            ))

    def __str__(self):
        res = ""
        for k, v in self.weapons.items():
            if v is not None:
                res += str(v)
        return res


class ArmourGroup:
    def __init__(
            self,
            armours: Optional[Iterable[Armour]] = None,
            hero_name: Optional[str] = None,
    ):
        if hero_name is None:
            hero_name = ""
        self.hero_name = hero_name
        self.armours: Dict[Level, Optional[Armour]] = {
            Level.ZERO: None,
            Level.ONE: None,
            Level.TWO: None,
            Level.THREE: None,
            Level.FOUR: None
        }
        if armours is not None:
            self.add_armours(armours)

    def add_armour(self, armour: Armour):
        armour = deepcopy(armour)
        armour.hero_name = self.hero_name
        self.armours[armour.level] = armour

    def add_armours(self, armours: Iterable[Armour]):
        for armour in armours:
            self.add_armour(armour)

    def autocomplete(self):
        """
        自动补全中间等级的护甲属性，特殊需求的 upgradeRequirementCode 属性需要手动设置
        :return:
        """
        if self.armours[Level.ZERO] is None or self.armours[Level.FOUR] is None:
            raise ValueError('armour group must have 0 and 4 level armours')
        x = []
        target_x = []
        defense = []
        prot = []
        hp = []
        spd = []

        for k, v in self.armours.items():
            if v is not None:
                x.append(k.value)
                defense.append(v.defense)
                prot.append(v.protection)
                hp.append(v.hp)
                spd.append(v.speed)
            else:
                target_x.append(k.value)
        if len(target_x) == 0:
            return
        target_defense = np.interp(target_x, x, defense)
        target_prot = np.interp(target_x, x, prot)
        target_hp = np.interp(target_x, x, hp)
        target_spd = np.interp(target_x, x, spd)

        for i in range(len(target_x)):
            self.add_armour(Armour(
                level=Level(target_x[i]),
                defense=target_defense[i],
                protection=target_prot[i],
                hp=round(target_hp[i]),
                # 一般第一次升级后速度并不会改变，所以这里向下取整
                speed=round(target_spd[i]) if target_x[i] != 1 else math.floor(target_spd[i])
            ))

    def __str__(self):
        res = ""
        for k, v in self.armours.items():
            if v is not None:
                res += str(v)
        return res


class Mode:
    """
    变身英雄或怪物的模式，不同模式下有不同的技能组
    """

    def __init__(
            self,
            mode_name: str,
            is_raid_default: bool = False,
            always_guard_actor_base_class_ids: Optional[Tuple[str, ...]] = None,
            is_targetable: bool = True,
            keep_rounds_in_ranks: bool = False,
            stress_damage_per_turn: int = 0,
            is_bark_override: bool = False,
            affliction_combat_skill_id: Optional[str] = None,
            battle_complete_combat_skill_id: Optional[str] = None,
            prefix: Optional[str] = None,
    ):
        """
        初始化
        :param mode_name: 模式名称
        :param is_raid_default: 是否为默认状态，可配置多个默认模式，但是每个默认模式都必须有待机、行走等动画
        :param always_guard_actor_base_class_ids: 总是守护某些单位
        :param is_targetable: 是否可以被选中
        :param keep_rounds_in_ranks: 用于官方DLC农场中的犁马怪物的犁地相关技能，与对应的怪物AI有关
        :param stress_damage_per_turn: 每回合受到的压力伤害
        :param is_bark_override: 是否有变身文本
        :param affliction_combat_skill_id: 进入折磨时会使用的技能
        :param battle_complete_combat_skill_id: 战斗结束后会使用的技能
        :param prefix: 前缀，与 mode_name 一起组成 id
        """
        self.mode_name = mode_name
        self.is_raid_default = is_raid_default
        self.always_guard_actor_base_class_ids = always_guard_actor_base_class_ids
        self.is_targetable = is_targetable
        self.keep_rounds_in_ranks = keep_rounds_in_ranks
        self.stress_damage_per_turn = stress_damage_per_turn
        self.is_bark_override = is_bark_override
        self.affliction_combat_skill_id = affliction_combat_skill_id
        self.battle_complete_combat_skill_id = battle_complete_combat_skill_id
        self.prefix = prefix

    @property
    def id(self):
        if self.prefix is not None:
            return f"{self.prefix}_{self.mode_name}"
        return clamp_string(self.mode_name)

    @property
    def bark_override_id(self):
        if self.is_bark_override:
            return f"str_{self.id}_bark"
        return None

    def __str__(self):
        res = f"mode: .id {self.id}"
        if self.is_raid_default:
            res += " .is_raid_default true"
        if self.always_guard_actor_base_class_ids is not None and len(self.always_guard_actor_base_class_ids) > 0:
            res += f" .always_guard_actor_base_class_ids {' '.join(self.always_guard_actor_base_class_ids)}"
        if not self.is_targetable:
            res += " .is_targetable false"
        if self.keep_rounds_in_ranks:
            res += " .keep_rounds_in_ranks true"
        if self.is_bark_override:
            res += f" .bark_override_id {self.bark_override_id}"
        if self.affliction_combat_skill_id is not None:
            res += f" .affliction_combat_skill_id {self.affliction_combat_skill_id}"
        if self.battle_complete_combat_skill_id is not None:
            res += f" .battle_complete_combat_skill_id {self.battle_complete_combat_skill_id}"
        if self.stress_damage_per_turn != 0:
            res += f" .stress_damage_per_turn {self.stress_damage_per_turn}"
        return res + "\n"


class Generation:
    """
    英雄马车生成相关参数
    """

    def __init__(
            self,
            is_generation_enabled: bool = True,
            town_event_dependency: Optional[str] = None,
            number_of_positive_quirks_min: int = 1,
            number_of_positive_quirks_max: int = 2,
            number_of_negative_quirks_min: int = 1,
            number_of_negative_quirks_max: int = 2,
            number_of_class_specific_camping_skills: int = 2,
            number_of_shared_camping_skills: int = 1,
            number_of_random_combat_skills: int = 4,
            number_of_cards_in_deck: int = 6,
            card_chance: float = 1.0,
            reduce_number_of_cards_in_deck_hero_class_id: Optional[str] = None,
            reduce_number_of_cards_in_deck_amount: int = 0
    ):
        """
        初始化
        :param is_generation_enabled: 马车能否生成该英雄
        :param town_event_dependency: 依赖的城镇事件
        :param number_of_positive_quirks_min: 生成时的最小正面怪癖数量
        :param number_of_positive_quirks_max: 生成时的最大正面怪癖数量
        :param number_of_negative_quirks_min: 生成时的最小负面怪癖数量
        :param number_of_negative_quirks_max: 生成时的最大负面怪癖数量
        :param number_of_class_specific_camping_skills: 生成时拥有的角色专属扎营技能数量
        :param number_of_shared_camping_skills: 生成时拥有的共享扎营技能数量
        :param number_of_random_combat_skills: 生成时解锁的战斗技能数量
        :param number_of_cards_in_deck: 牌堆中该角色的卡牌数量
        :param card_chance: 从牌堆中抽到该角色的概率
        :param reduce_number_of_cards_in_deck_hero_class_id: 减少指定角色在牌堆中的卡牌（未验证）
        :param reduce_number_of_cards_in_deck_amount: 减少的卡牌数量（未验证）
        """
        self.is_generation_enabled = is_generation_enabled
        self.town_event_dependency = town_event_dependency
        self.number_of_positive_quirks_min = number_of_positive_quirks_min
        self.number_of_positive_quirks_max = number_of_positive_quirks_max
        self.number_of_negative_quirks_min = number_of_negative_quirks_min
        self.number_of_negative_quirks_max = number_of_negative_quirks_max
        self.number_of_class_specific_camping_skills = number_of_class_specific_camping_skills
        self.number_of_shared_camping_skills = number_of_shared_camping_skills
        self.number_of_random_combat_skills = number_of_random_combat_skills
        self.number_of_cards_in_deck = number_of_cards_in_deck
        self.card_chance = card_chance
        self.reduce_number_of_cards_in_deck_hero_class_id = reduce_number_of_cards_in_deck_hero_class_id
        self.reduce_number_of_cards_in_deck_amount = reduce_number_of_cards_in_deck_amount

    def __str__(self):
        res = f"generation: .is_generation_enabled {bool_to_lower_str(self.is_generation_enabled)}"
        if self.town_event_dependency is not None:
            res += f' .town_event_dependency "{self.town_event_dependency}"'
        res += f' .number_of_positive_quirks_min {self.number_of_positive_quirks_min} ' \
               f'.number_of_positive_quirks_max {self.number_of_positive_quirks_max} ' \
               f'.number_of_negative_quirks_min {self.number_of_negative_quirks_min} ' \
               f'.number_of_negative_quirks_max {self.number_of_negative_quirks_max} ' \
               f'.number_of_class_specific_camping_skills {self.number_of_class_specific_camping_skills} ' \
               f'.number_of_shared_camping_skills {self.number_of_shared_camping_skills} ' \
               f'.number_of_random_combat_skills {self.number_of_random_combat_skills} ' \
               f'.number_of_cards_in_deck {self.number_of_cards_in_deck} ' \
               f'.card_chance {self.card_chance:.1f}'
        if self.reduce_number_of_cards_in_deck_hero_class_id is not None \
                and self.reduce_number_of_cards_in_deck_amount != 0:
            res += f' .reduce_number_of_cards_in_deck_hero_class_id ' \
                   f'{self.reduce_number_of_cards_in_deck_hero_class_id} ' \
                   f'.reduce_number_of_cards_in_deck_amount {self.reduce_number_of_cards_in_deck_amount}'
        return res + "\n"


class ActoutDisplay:
    def __init__(
            self,
            attack_friendly_anim: Optional[str] = None,
            attack_friendly_fx: Optional[str] = None,
            attack_friendly_targchestfx: Optional[str] = None,
            attack_friendly_sfx: Optional[str] = None,
    ):
        self.attack_friendly_anim = attack_friendly_anim
        self.attack_friendly_fx = attack_friendly_fx
        self.attack_friendly_targchestfx = attack_friendly_targchestfx
        self.attack_friendly_sfx = attack_friendly_sfx

    def __str__(self):
        res = ["act_out_display:"]
        none_str = {
            "attack_friendly_anim": self.attack_friendly_anim,
            "attack_friendly_fx": self.attack_friendly_fx,
            "attack_friendly_targchestfx": self.attack_friendly_targchestfx,
            "attack_friendly_sfx": self.attack_friendly_sfx,
        }
        for k, v in none_str.items():
            if v is not None:
                res.append(f'.{k} "{v}"')

        return " ".join(res) + "\n"

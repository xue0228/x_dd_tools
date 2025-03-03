import math
import os
from dataclasses import dataclass
from typing import Optional, Iterable, Dict, Tuple, Union, List

import numpy as np

from xddtools.base import BaseID, LocalizationWriter
from xddtools.buffs import Buff
from xddtools.effects import Effect
from xddtools.enums import Level, UpgradeRequirementCode, TagID, TownActivityType, DeathFx, ItemType
from xddtools.items import Item
from xddtools.loot import LootTable
from xddtools.path import HERO_SAVE_DIR, DATA_PATH
from xddtools.quirks import Quirk
from xddtools.skills import Skill
from xddtools.traits import Trait
from xddtools.utils import float_to_percent_str, bool_to_lower_str, clamp_string, is_image, resize_image, split_list
from xddtools.writers import BuffWriter, EffectWriter


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


class WeaponGroup(BaseID):
    def __init__(
            self,
            hero_name: str,
            weapons: Optional[Iterable[Weapon]] = None,
            image_paths: Optional[Iterable[str]] = None,
            # localization: Optional[Union[Tuple[str, ...], str]] = None,
    ):
        if image_paths is not None:
            images = []
            for image in image_paths:
                if is_image(image):
                    images.append(image)
                else:
                    raise ValueError(f"{image} is not a image file")
            image_paths = images
        self.image_paths = image_paths

        self.weapons: Dict[Level, Optional[Weapon]] = {
            Level.ZERO: None,
            Level.ONE: None,
            Level.TWO: None,
            Level.THREE: None,
            Level.FOUR: None
        }
        if weapons is not None:
            self.add_weapons(weapons)
        super().__init__(
            name=hero_name,
            # localization=localization,
            # entry_id_prefix=(
            #     f"upgrade_tree_name_{hero_name}.weapon"
            #     f"{hero_name}_weapon_0",
            #     f"{hero_name}_weapon_1",
            #     f"{hero_name}_weapon_2",
            #     f"{hero_name}_weapon_3",
            #     f"{hero_name}_weapon_4",
            # ),
        )

    def add_weapon(self, weapon: Weapon):
        # weapon = deepcopy(weapon)
        weapon.hero_name = self.id
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

    def export_image(self, root_dir: Optional[str] = None) -> Tuple[str]:
        if self.image_paths is None:
            raise ValueError("weapon group image paths is None")
        if root_dir is None:
            root_dir = "./"
        save_dir = os.path.join(root_dir, HERO_SAVE_DIR, self.id, "icons_equip")
        res: List[str] = []
        for i in range(len(self.image_paths)):
            filename = f"eqp_weapon_{i}.png"
            res.append(
                resize_image(self.image_paths[i], os.path.join(save_dir, filename))
            )
        return tuple(res)


class ArmourGroup(BaseID):
    def __init__(
            self,
            hero_name: str,
            armours: Optional[Iterable[Armour]] = None,
            image_paths: Optional[Iterable[str]] = None,
            # localization: Optional[Union[Tuple[str, ...], str]] = None,
    ):
        if image_paths is not None:
            images = []
            for image in image_paths:
                if is_image(image):
                    images.append(image)
                else:
                    raise ValueError(f"{image} is not a image file")
            image_paths = images
        self.image_paths = image_paths

        self.armours: Dict[Level, Optional[Armour]] = {
            Level.ZERO: None,
            Level.ONE: None,
            Level.TWO: None,
            Level.THREE: None,
            Level.FOUR: None
        }
        if armours is not None:
            self.add_armours(armours)
        super().__init__(
            name=hero_name,
            # localization=localization,
            # entry_id_prefix=(
            #     f"upgrade_tree_name_{hero_name}.armour"
            #     f"{hero_name}_armour_0",
            #     f"{hero_name}_armour_1",
            #     f"{hero_name}_armour_2",
            #     f"{hero_name}_armour_3",
            #     f"{hero_name}_armour_4",
            # ),
        )

    def add_armour(self, armour: Armour):
        # armour = deepcopy(armour)
        armour.hero_name = self.id
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

    def export_image(self, root_dir: Optional[str] = None) -> Tuple[str]:
        if self.image_paths is None:
            raise ValueError("armour group image paths is None")
        if root_dir is None:
            root_dir = "./"
        save_dir = os.path.join(root_dir, HERO_SAVE_DIR, self.id, "icons_equip")
        res: List[str] = []
        for i in range(len(self.image_paths)):
            filename = f"eqp_armour_{i}.png"
            res.append(
                resize_image(self.image_paths[i], os.path.join(save_dir, filename))
            )
        return tuple(res)


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


@dataclass(frozen=True)
class OverstressedModify:
    trait_id: Union[Trait, str]
    chance: int = 1


@dataclass(frozen=True)
class ActivityModify:
    activity_ids: Iterable[TownActivityType]
    stress_removal_amount_low: int = 100
    stress_removal_amount_high: int = 100


@dataclass(frozen=True)
class ExtraLoot:
    code: Union[LootTable, str]
    count: int = 1


@dataclass(frozen=True)
class ExtraStackLimit:
    item_type: ItemType
    item_id: Union[Item, str]
    amount: int

    @property
    def id(self) -> str:
        item_id = self.item_id.id if isinstance(self.item_id, Item) else self.item_id
        return "_".join([self.item_type.value, item_id])

    def __str__(self) -> str:
        item_id = self.item_id.id if isinstance(self.item_id, Item) else self.item_id
        return f'extra_stack_limit: .id {self.id} ' \
               f'.item_type {self.item_type.value} ' \
               f'.item_id "{item_id}" ' \
               f'.amount {self.amount}\n'


@dataclass(frozen=True)
class HeroLocalization:
    weapon_upgrade: str
    weapon_0: str
    weapon_1: str
    weapon_2: str
    weapon_3: str
    weapon_4: str
    armour_upgrade: str
    armour_0: str
    armour_1: str
    armour_2: str
    armour_3: str
    armour_4: str


class Hero(BaseID):
    def __init__(
            self,
            hero_name: str,
            id_index: int,
            resistances: Resistance,
            crit_effects: Iterable[Union[Effect, str]],
            skills: Iterable[Skill],
            target_rank: int,
            weapons: Iterable[Weapon],
            armours: Iterable[Armour],
            weapon_image_path: Optional[str] = None,
            armour_image_path: Optional[str] = None,
            tags: Optional[Iterable[Union[TagID, str]]] = None,
            overstressed_modifier: Optional[Iterable[OverstressedModify]] = None,
            deaths_door_buffs: Optional[Iterable[Union[Buff, str]]] = None,
            recovery_buffs: Optional[Iterable[Union[Buff, str]]] = None,
            recovery_heart_attack_buffs: Optional[Iterable[Union[Buff, str]]] = None,
            can_select_combat_skills: bool = True,
            number_of_selected_combat_skills_max: int = 4,
            can_self_party: bool = True,
            generation: Optional[Generation] = None,
            activity_modifier: Optional[ActivityModify] = None,
            quirk_modifier: Optional[Iterable[Union[Quirk, str]]] = None,
            extra_battle_loot: Optional[ExtraLoot] = None,
            extra_curio_loot: Optional[ExtraLoot] = None,
            extra_stack_limit: Optional[Iterable[ExtraStackLimit]] = None,
            extra_shard_bonus: Optional[float] = None,
            death_fx: Union[DeathFx, str] = DeathFx.DEATH_MEDIUM,
            auto_display: Optional[ActoutDisplay] = None,
            hero_localization: Optional[HeroLocalization] = None,

            buff_writer: Optional[BuffWriter] = None,
            effect_writer: Optional[EffectWriter] = None,
            localization_writer: Optional[LocalizationWriter] = None,
    ):
        if id_index <= 17:
            raise ValueError("id_index must be greater than 17")

        if target_rank < 1 or target_rank > 4:
            raise ValueError("target_rank must be in range [1, 4]")

        if tags is None:
            tags = (TagID.LIGHT, TagID.NON_RELIGIOUS, TagID.OUTSIDERS_BONFIRE)

        eqp_dir = os.path.join(DATA_PATH, "template", "icons_equip")
        if weapon_image_path is None:
            weapon_image_path = (
                os.path.join(eqp_dir, "eqp_weapon_0.png"),
                os.path.join(eqp_dir, "eqp_weapon_1.png"),
                os.path.join(eqp_dir, "eqp_weapon_2.png"),
                os.path.join(eqp_dir, "eqp_weapon_3.png"),
                os.path.join(eqp_dir, "eqp_weapon_4.png"),
            )
        if armour_image_path is None:
            armour_image_path = (
                os.path.join(eqp_dir, "eqp_armour_0.png"),
                os.path.join(eqp_dir, "eqp_armour_1.png"),
                os.path.join(eqp_dir, "eqp_armour_2.png"),
                os.path.join(eqp_dir, "eqp_armour_3.png"),
                os.path.join(eqp_dir, "eqp_armour_4.png"),
            )

        if deaths_door_buffs is None:
            deaths_door_buffs = (
                "deathsdoorACCDebuff",
                "deathsdoorDMGLowDebuff",
                "deathsdoorDMGHighDebuff",
                "deathsdoorSPDDebuff",
                "deathsdoorSRDebuff",
            )
        if recovery_buffs is None:
            recovery_buffs = (
                "mortalityACCDebuff",
                "mortalityDMGLowDebuff",
                "mortalityDMGHighDebuff",
                "mortalitySPDDebuff",
                "mortalitySRDebuff",
            )
        if recovery_heart_attack_buffs is None:
            recovery_heart_attack_buffs = (
                "heartattackACCDebuff",
                "heartattackDMGLowDebuff",
                "heartattackDMGHighDebuff",
                "heartattackSPDDebuff",
                "heartattackSRDebuff",
            )

        if generation is None:
            generation = Generation()

        self.id_index = id_index
        self.resistances = resistances
        self.crit_effects = crit_effects
        # self.weapons = weapons
        # self.armours = armours
        # self.weapon_image_path = weapon_image_path
        # self.armour_image_path = armour_image_path
        self.skills = skills
        self.target_rank = target_rank
        self.tags = tags
        self.overstressed_modifier = overstressed_modifier
        self.deaths_door_buffs = deaths_door_buffs
        self.recovery_buffs = recovery_buffs
        self.recovery_heart_attack_buffs = recovery_heart_attack_buffs
        self.can_select_combat_skills = can_select_combat_skills
        self.number_of_selected_combat_skills_max = number_of_selected_combat_skills_max
        self.can_self_party = can_self_party
        self.generation = generation
        self.activity_modifier = activity_modifier
        self.quirk_modifier = quirk_modifier
        self.extra_battle_loot = extra_battle_loot
        self.extra_curio_loot = extra_curio_loot
        self.extra_stack_limit = extra_stack_limit
        self.extra_shard_bonus = extra_shard_bonus
        self.death_fx = death_fx
        self.auto_display = auto_display
        self.hero_localization = hero_localization

        self._weapon_group = WeaponGroup(
            hero_name=hero_name,
            weapons=weapons,
            image_paths=weapon_image_path,
            # localization=(
            #     hero_localization.weapon_upgrade,
            #     hero_localization.weapon_0,
            #     hero_localization.weapon_1,
            #     hero_localization.weapon_2,
            #     hero_localization.weapon_3,
            #     hero_localization.weapon_4,
            # ) if hero_localization is not None else None
        )
        self._weapon_group.autocomplete()
        self._armour_group = ArmourGroup(
            hero_name=hero_name,
            armours=armours,
            image_paths=armour_image_path,
            # localization=(
            #     hero_localization.armour_upgrade,
            #     hero_localization.armour_0,
            #     hero_localization.armour_1,
            #     hero_localization.armour_2,
            #     hero_localization.armour_3,
            #     hero_localization.armour_4,
            # ) if hero_localization is not None else None
        )
        self._armour_group.autocomplete()

        self._buff_writer = buff_writer
        self._effect_writer = effect_writer
        self._localization_writer = localization_writer

        super().__init__(hero_name)

    def info(self) -> str:
        res = [str(self.resistances)]

        effects = [effect.id if isinstance(effect, Effect) else effect for effect in self.crit_effects]
        effects = " ".join([f'"{effect}"' for effect in effects])
        res.append(f'crit: .effects: {effects}\n')

        res.append(str(self._weapon_group))
        res.append(str(self._armour_group))

        for skill in self.skills:
            res.append(skill.info)

        for tag in self.tags:
            tag = tag.value if isinstance(tag, TagID) else tag
            res.append(f'tag: .id "{tag}"\n')

        if self.overstressed_modifier is not None:
            for modify in self.overstressed_modifier:
                trait_id = modify.trait_id.id if isinstance(modify.trait_id, Trait) else modify.trait_id
                res.append(f'overstressed_modifier: .override_trait_type_ids {trait_id} '
                           f'.override_trait_type_chances {modify.chance}\n')

        if self.activity_modifier is not None:
            activity_ids = " ".join([activity.value for activity in self.activity_modifier.activity_ids])
            res.append(f'activity_modifier: .override_valid_activity_ids {activity_ids} '
                       f'.override_stress_removal_amount_low {self.activity_modifier.stress_removal_amount_low} '
                       f'.override_stress_removal_amount_high {self.activity_modifier.stress_removal_amount_high}\n')

        if self.quirk_modifier is not None:
            quirks = [quirk.id if isinstance(quirk, Quirk) else quirk for quirk in self.quirk_modifier]
            quirks = split_list(quirks, 8)
            for quirk in quirks:
                res.append(f'quirk_modifier: .incompatible_class_ids {" ".join(quirk)}\n')

        tem = []
        for buff in self.deaths_door_buffs:
            buff = buff.id if isinstance(buff, Buff) else buff
            tem.append(buff)
        res.append(f'deaths_door: .buffs {" ".join(tem)}\n')

        res.append(f'controlled: .target_rank {self.target_rank}\n')
        res.append(f'id_index: .index {self.id_index}\n')

        res.append(f'skill_selection: .can_select_combat_skills {bool_to_lower_str(self.can_select_combat_skills)} '
                   f'.number_of_selected_combat_skills_max {self.number_of_selected_combat_skills_max}\n')

        if self.can_self_party:
            res.append(f'incompatible_party_member: .id {self.id}_limit .hero_tag {self.id}\n')

        if self.extra_battle_loot is not None:
            code = self.extra_battle_loot.code.id \
                if isinstance(self.extra_battle_loot.code, LootTable) else self.extra_battle_loot.code
            res.append(f'extra_battle_loot: .code "{code}" .count {self.extra_battle_loot.count}\n')

        if self.extra_curio_loot is not None:
            code = self.extra_curio_loot.code.id \
                if isinstance(self.extra_curio_loot.code, LootTable) else self.extra_curio_loot.code
            res.append(f'extra_curio_loot: .code "{code}" .count {self.extra_curio_loot.count}\n')

        if self.extra_stack_limit is not None:
            for limit in self.extra_stack_limit:
                res.append(f'extra_stack_limit: .id {limit.id}\n')

        if self.extra_shard_bonus is not None:
            res.append(f'extra_shard_bonus: .amount {self.extra_shard_bonus}\n')

        res.append(str(self.generation))

        return "".join(res)

    def art(self) -> str:
        res = [f'commonfx: .deathfx {self.death_fx.value}\n']

        weapon = "".join(f'weapon: .name "{self.id}_weapon_{i}" .icon "eqp_weapon_{i}.png"\n' for i in range(5))
        armour = "".join(f'armour: .name "{self.id}_armour_{i}" .icon "eqp_armour_{i}.png"\n' for i in range(5))
        res.append(weapon)
        res.append(armour)

        skill = "".join([item.art for item in self.skills])
        res.append(skill)

        if self.auto_display is not None:
            res.append(str(self.auto_display))

        return "\n".join(res)

    def __str__(self):
        return "\n".join([self.info(), self.art()])

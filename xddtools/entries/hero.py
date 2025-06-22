import math
import os
from typing import Optional, Union, Tuple, Sequence, List

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, model_validator

from xddtools.base import HeroEntry, SkillEntry, EffectEntry, TownEventEntry, get_entry_id, AnimationEntry, \
    TraitEntry, LootTableEntry, ItemEntry, QuirkEntry, BuffEntry, ModeEntry, MonsterEntry, BankEntry, JsonData
from xddtools.entries.skill import Skill, SkillInfo
from xddtools.enum import InnerFx
from xddtools.enum.buff_rule import TownActivityType, ItemType, MonsterClass, HeroClass, QuirkType, ItemID
from xddtools.enum.hero import DeathFx, TagID
from xddtools.name import AutoName
from xddtools.path import DATA_PATH
from xddtools.utils import float_to_percent_str, bool_to_lower_str, split_list, get_bark_list


class Resistance(BaseModel):
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

    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    stun: float
    poison: float
    bleed: float
    disease: float
    move: float
    debuff: float
    death_blow: float
    trap: float

    def __str__(self):
        return f"resistances: .stun {float_to_percent_str(self.stun)}% " \
               f".poison {float_to_percent_str(self.poison)}% " \
               f".bleed {float_to_percent_str(self.bleed)}% " \
               f".disease {float_to_percent_str(self.disease)}% " \
               f".move {float_to_percent_str(self.move)}% " \
               f".debuff {float_to_percent_str(self.debuff)}% " \
               f".death_blow {float_to_percent_str(self.death_blow)}% " \
               f".trap {float_to_percent_str(self.trap)}%"


class Weapon(BaseModel):
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

    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    attack: float
    damage_low: int
    damage_high: int
    critical_rate: float
    speed: int

    @model_validator(mode="after")
    def _check_after(self):
        if self.damage_low > self.damage_high:
            raise ValueError(f"damage_low must be not more than damage_high,"
                             f"but get {self.damage_low} and {self.damage_high}")
        return self

    def info(self, level: int, hero_name: str):
        res = f'weapon: .name "{hero_name}_weapon_{level}" ' \
              f'.atk {float_to_percent_str(self.attack)}% ' \
              f'.dmg {self.damage_low} {self.damage_high} ' \
              f'.crit {float_to_percent_str(self.critical_rate)}% ' \
              f'.spd {self.speed}'
        if level != 0:
            res += f' .upgradeRequirementCode {level - 1}'
        return res


class Armour(BaseModel):
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

    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    defense: float
    protection: float
    hp: int
    speed: int

    def info(self, level: int, hero_name: str):
        res = f'armour: .name "{hero_name}_armour_{level}" ' \
              f'.def {float_to_percent_str(self.defense)}% ' \
              f'.prot {float_to_percent_str(self.protection)}% ' \
              f'.hp {self.hp} .spd {self.speed}'
        if level != 0:
            res += f' .upgradeRequirementCode {level - 1}'
        return res


class Generation(BaseModel):
    """
    is_generation_enabled: 马车能否生成该英雄
    town_event_dependency: 依赖的城镇事件
    number_of_positive_quirks_min: 生成时的最小正面怪癖数量
    number_of_positive_quirks_max: 生成时的最大正面怪癖数量
    number_of_negative_quirks_min: 生成时的最小负面怪癖数量
    number_of_negative_quirks_max: 生成时的最大负面怪癖数量
    number_of_class_specific_camping_skills: 生成时拥有的角色专属扎营技能数量
    number_of_shared_camping_skills: 生成时拥有的共享扎营技能数量
    number_of_random_combat_skills: 生成时解锁的战斗技能数量
    number_of_cards_in_deck: 牌堆中该角色的卡牌数量
    card_chance: 从牌堆中抽到该角色的概率
    reduce_number_of_cards_in_deck_hero_class_id: 减少指定角色在牌堆中的卡牌（未验证）
    reduce_number_of_cards_in_deck_amount: 减少的卡牌数量（未验证）
    """
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    is_generation_enabled: bool = True
    town_event_dependency: Union[TownEventEntry, str, None] = None
    number_of_positive_quirks_min: int = 1
    number_of_positive_quirks_max: int = 2
    number_of_negative_quirks_min: int = 1
    number_of_negative_quirks_max: int = 2
    number_of_class_specific_camping_skills: int = 2
    number_of_shared_camping_skills: int = 1
    number_of_random_combat_skills: int = 4
    number_of_cards_in_deck: int = 6
    card_chance: float = 1.0
    reduce_number_of_cards_in_deck_hero_class_id: Union[HeroEntry, str, None] = None
    reduce_number_of_cards_in_deck_amount: int = 0

    def __str__(self):
        res = f"generation: .is_generation_enabled {bool_to_lower_str(self.is_generation_enabled)}"
        if self.town_event_dependency is not None:
            res += f' .town_event_dependency "{get_entry_id(self.town_event_dependency)}"'
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
                   f'{get_entry_id(self.reduce_number_of_cards_in_deck_hero_class_id)} ' \
                   f'.reduce_number_of_cards_in_deck_amount {self.reduce_number_of_cards_in_deck_amount}'
        return res


class ActoutDisplay(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    attack_friendly_anim: Union[AnimationEntry, str, None] = None
    attack_friendly_fx: Union[InnerFx, AnimationEntry, str, None] = None
    attack_friendly_targchestfx: Union[InnerFx, AnimationEntry, str, None] = None
    attack_friendly_sfx: Union[BankEntry, str, None] = None

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
                res.append(f'.{k} "{get_entry_id(v)}"')

        return " ".join(res)


class OverstressedModify(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    trait_id: Union[TraitEntry, str]
    chance: int = 1


class ActivityModify(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    activity_ids: Sequence[TownActivityType]
    stress_removal_amount_low: int = 100
    stress_removal_amount_high: int = 100


class ExtraLoot(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    code: Union[LootTableEntry, str]
    count: int = 1


class ExtraStackLimit(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    item_type: ItemType
    item_id: Union[ItemEntry, str] = ""
    amount: int

    def id(self, hero_name: str) -> str:
        entry_id = [hero_name, self.item_type.value]
        if self.item_id != "":
            entry_id.append(get_entry_id(self.item_id))
        return "_".join(entry_id)

    def info(self, hero_name: str) -> str:
        return f'extra_stack_limit: .id {self.id(hero_name)} ' \
               f'.item_type {self.item_type.value} ' \
               f'.item_id "{get_entry_id(self.item_id)}" ' \
               f'.amount {self.amount}'


class HpReaction(BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    hp_ratio: float = Field(..., ge=0.0, le=1.0)
    is_under: bool = True
    effects: Sequence[Union[EffectEntry, str]] = Field(default_factory=list)

    def __str__(self):
        res = [f'hp_reaction: .hp_ratio {self.hp_ratio} .is_under {bool_to_lower_str(self.is_under)}']
        if len(self.effects) > 0:
            res.append(".effects")
            for effect in self.effects:
                res.append(f'"{get_entry_id(effect)}"')
        return " ".join(res)


class DeathReaction(BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    target_allies: bool = False
    target_enemies: bool = True
    effects: Sequence[Union[EffectEntry, str]] = Field(default_factory=list)

    def __str__(self):
        res = [f'death_reaction: .target_allies {bool_to_lower_str(self.target_allies)} '
               f'.target_enemies {bool_to_lower_str(self.target_enemies)}']
        if len(self.effects) > 0:
            res.append(".effects")
            for effect in self.effects:
                res.append(f'"{get_entry_id(effect)}"')
        return " ".join(res)


class HeroLocalization(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    # 英雄名称
    hero_class_name: str

    # 铁匠铺描述
    blacksmith_verbose: str
    # 工会描述
    guild_verbose: str
    # 营地描述
    camping_verbose: str

    # 武器名称
    weapon_upgrade: str
    weapon_0: str
    weapon_1: str
    weapon_2: str
    weapon_3: str
    weapon_4: str

    # 护甲名称
    armour_upgrade: str
    armour_0: str
    armour_1: str
    armour_2: str
    armour_3: str
    armour_4: str

    # 夜袭台词
    # 注意！夜袭台词不遵循常规的同条多行写法，而是必须0123逐条
    night_ambush_bark_0: Optional[str] = None
    night_ambush_bark_1: Optional[str] = None
    night_ambush_bark_2: Optional[str] = None
    night_ambush_bark_3: Optional[str] = None

    # 确认进入城镇活动时触发
    bar_committed: Union[Sequence[str], str, None] = None
    gambling_committed: Union[Sequence[str], str, None] = None
    brothel_committed: Union[Sequence[str], str, None] = None
    meditation_committed: Union[Sequence[str], str, None] = None
    prayer_committed: Union[Sequence[str], str, None] = None
    flagellation_committed: Union[Sequence[str], str, None] = None
    treatment_committed: Union[Sequence[str], str, None] = None
    disease_treatment_committed: Union[Sequence[str], str, None] = None

    # 通用活动受限台词，当info下直接编写活动受限时需使用本条
    override_invalid_rejection: Union[Sequence[str], str, None] = None

    # 城镇闲置台词
    # 下述内容为英雄于城镇界面右侧列表闲置时的弹出式台词
    roster_list_bar: Union[Sequence[str], str, None] = None
    roster_list_gambling: Union[Sequence[str], str, None] = None
    roster_list_brothel: Union[Sequence[str], str, None] = None
    roster_list_meditation: Union[Sequence[str], str, None] = None
    roster_list_prayer: Union[Sequence[str], str, None] = None
    roster_list_flagellation: Union[Sequence[str], str, None] = None
    roster_list_treatment: Union[Sequence[str], str, None] = None
    roster_list_disease_treatment: Union[Sequence[str], str, None] = None
    roster_list_low_stress: Union[Sequence[str], str, None] = None
    roster_list_medium_stress: Union[Sequence[str], str, None] = None
    roster_list_high_stress: Union[Sequence[str], str, None] = None
    roster_dd_survivor: Union[Sequence[str], str, None] = None

    # 马车招募台词
    # 马车闲置台词
    stagecoach_idle: Union[Sequence[str], str, None] = None
    # 兵营满员台词
    stagecoach_roster_full_rejection: Union[Sequence[str], str, None] = None

    # 地图触发界面台词
    quest_too_hard: Union[Sequence[str], str, None] = None
    quest_too_easy: Union[Sequence[str], str, None] = None

    # 自身互斥组队台词
    incompatible_self_party: Union[Sequence[str], str, None] = None

    # 副本内台词，探索及战斗
    # 探索台词：开始移动
    start_moving: Union[Sequence[str], str, None] = None
    # 探索台词：停止移动
    stop_moving: Union[Sequence[str], str, None] = None
    # 探索台词：后退移动
    backing_up: Union[Sequence[str], str, None] = None
    # 探索台词：触发陷阱
    comment_trap_triggered: Union[Sequence[str], str, None] = None
    # 探索及战斗台词：自身压力提升
    increasing_stress: Union[Sequence[str], str, None] = None
    # 战斗台词：自身暴击
    crit_by_hero: Union[Sequence[str], str, None] = None
    # 战斗台词：被击退(包括自身和友方造成的击退
    combat_knock_back: Union[Sequence[str], str, None] = None
    # 战斗台词：拖延时间导致增援触发警告
    combat_wasting_time: Union[Sequence[str], str, None] = None
    # 战斗台词：自身承受重伤
    big_wound: Union[Sequence[str], str, None] = None
    # 战斗台词：友方承受重伤
    big_wound_ally: Union[Sequence[str], str, None] = None
    # 战斗台词：自身死门
    deathsdoor: Union[Sequence[str], str, None] = None
    # 战斗台词：友方死门
    deathsdoor_ally: Union[Sequence[str], str, None] = None
    # 战斗台词：自身脱离死门
    deathsdoor_survive: Union[Sequence[str], str, None] = None
    # 战斗台词：友方脱离死门
    deathsdoor_survive_ally: Union[Sequence[str], str, None] = None
    # 战斗台词：自身心衰(注意官方原版是存在单独且非折磨的心衰台词，意味不明)
    heart_attack: Union[Sequence[str], str, None] = None
    # 战斗台词：自身腐蚀生效
    poison_dot: Union[Sequence[str], str, None] = None
    # 战斗台词：自身流血生效
    bleed_dot: Union[Sequence[str], str, None] = None
    # 战斗台词：自身愈合生效
    hp_heal_dot: Union[Sequence[str], str, None] = None

    # 降低亮度台词
    torch_0: Union[Sequence[str], str, None] = None
    torch_1: Union[Sequence[str], str, None] = None
    torch_2: Union[Sequence[str], str, None] = None

    # 奇物互动台词
    curio_good: Union[Sequence[str], str, None] = None
    curio_bad: Union[Sequence[str], str, None] = None
    # 奇物互动无事发生
    curio_meh: Union[Sequence[str], str, None] = None

    # 扎营台词
    # 队伍平均状态
    stress_party_high: Union[Sequence[str], str, None] = None
    stress_party_low: Union[Sequence[str], str, None] = None
    hp_party_high: Union[Sequence[str], str, None] = None
    hp_party_low: Union[Sequence[str], str, None] = None
    # 自身状态
    stress_self_high: Union[Sequence[str], str, None] = None
    stress_self_low: Union[Sequence[str], str, None] = None
    hp_self_high: Union[Sequence[str], str, None] = None
    hp_self_low: Union[Sequence[str], str, None] = None
    # 队伍总体状态
    party_poor_condition: Union[Sequence[str], str, None] = None
    party_great_condition: Union[Sequence[str], str, None] = None
    # 营火储备
    firewood_high: Union[Sequence[str], str, None] = None
    firewood_low: Union[Sequence[str], str, None] = None
    # 食物储备
    provisions_high: Union[Sequence[str], str, None] = None
    provisions_low: Union[Sequence[str], str, None] = None
    # 扎营友谊聊天(扎营收尾时)
    companionship: Union[Sequence[str], str, None] = None

    def get_localization_entries(self, hero_name: str) -> List[Tuple[str, str]]:
        res = [
            (f"hero_class_name_{hero_name}", self.hero_class_name),

            (f"action_verbose_body_blacksmith_{hero_name}", self.blacksmith_verbose),
            (f"action_verbose_body_guild_{hero_name}", self.guild_verbose),
            (f"action_verbose_body_camping_trainer_{hero_name}", self.camping_verbose),

            (f"upgrade_tree_name_{hero_name}.weapon", self.weapon_upgrade),
            (f"{hero_name}_weapon_0", self.weapon_0),
            (f"{hero_name}_weapon_1", self.weapon_1),
            (f"{hero_name}_weapon_2", self.weapon_2),
            (f"{hero_name}_weapon_3", self.weapon_3),
            (f"{hero_name}_weapon_4", self.weapon_4),

            (f"upgrade_tree_name_{hero_name}.armour", self.armour_upgrade),
            (f"{hero_name}_armour_0", self.armour_0),
            (f"{hero_name}_armour_1", self.armour_1),
            (f"{hero_name}_armour_2", self.armour_2),
            (f"{hero_name}_armour_3", self.armour_3),
            (f"{hero_name}_armour_4", self.armour_4),
        ]

        if self.night_ambush_bark_0 is not None:
            res.append((f"{hero_name}+str_night_ambush_bark_0", self.night_ambush_bark_0))
        if self.night_ambush_bark_1 is not None:
            res.append((f"{hero_name}+str_night_ambush_bark_1", self.night_ambush_bark_1))
        if self.night_ambush_bark_2 is not None:
            res.append((f"{hero_name}+str_night_ambush_bark_2", self.night_ambush_bark_2))
        if self.night_ambush_bark_3 is not None:
            res.append((f"{hero_name}+str_night_ambush_bark_3", self.night_ambush_bark_3))

        res.extend([(f"{hero_name}+str_bar_committed", bark)
                    for bark in get_bark_list(self.bar_committed)])
        res.extend([(f"{hero_name}+str_gambling_committed", bark)
                    for bark in get_bark_list(self.gambling_committed)])
        res.extend([(f"{hero_name}+str_brothel_committed", bark)
                    for bark in get_bark_list(self.brothel_committed)])
        res.extend([(f"{hero_name}+str_meditation_committed", bark)
                    for bark in get_bark_list(self.meditation_committed)])
        res.extend([(f"{hero_name}+str_prayer_committed", bark)
                    for bark in get_bark_list(self.prayer_committed)])
        res.extend([(f"{hero_name}+str_flagellation_committed", bark)
                    for bark in get_bark_list(self.flagellation_committed)])
        res.extend([(f"{hero_name}+str_treatment_committed", bark)
                    for bark in get_bark_list(self.treatment_committed)])
        res.extend([(f"{hero_name}+str_disease_treatment_committed", bark)
                    for bark in get_bark_list(self.disease_treatment_committed)])

        res.extend([(f"{hero_name}+str_override_invalid_rejection", bark)
                    for bark in get_bark_list(self.override_invalid_rejection)])

        res.extend([(f"{hero_name}+str_roster_list_bar_bark", bark)
                    for bark in get_bark_list(self.roster_list_bar)])
        res.extend([(f"{hero_name}+str_roster_list_gambling_bark", bark)
                    for bark in get_bark_list(self.roster_list_gambling)])
        res.extend([(f"{hero_name}+str_roster_list_brothel_bark", bark)
                    for bark in get_bark_list(self.roster_list_brothel)])
        res.extend([(f"{hero_name}+str_roster_list_meditation_bark", bark)
                    for bark in get_bark_list(self.roster_list_meditation)])
        res.extend([(f"{hero_name}+str_roster_list_prayer_bark", bark)
                    for bark in get_bark_list(self.roster_list_prayer)])
        res.extend([(f"{hero_name}+str_roster_list_flagellation_bark", bark)
                    for bark in get_bark_list(self.roster_list_flagellation)])
        res.extend([(f"{hero_name}+str_roster_list_treatment_bark", bark)
                    for bark in get_bark_list(self.roster_list_treatment)])
        res.extend([(f"{hero_name}+str_roster_list_disease_treatment_bark", bark)
                    for bark in get_bark_list(self.roster_list_disease_treatment)])
        res.extend([(f"{hero_name}+str_roster_list_low_stress_bark", bark)
                    for bark in get_bark_list(self.roster_list_low_stress)])
        res.extend([(f"{hero_name}+str_roster_list_medium_stress_bark", bark)
                    for bark in get_bark_list(self.roster_list_medium_stress)])
        res.extend([(f"{hero_name}+str_roster_list_high_stress_bark", bark)
                    for bark in get_bark_list(self.roster_list_high_stress)])
        res.extend([(f"{hero_name}+str_roster_darkest_dungeon_survivor_bark", bark)
                    for bark in get_bark_list(self.roster_dd_survivor)])

        res.extend([(f"{hero_name}+str_stagecoach_idle", bark)
                    for bark in get_bark_list(self.stagecoach_idle)])
        res.extend([(f"{hero_name}+str_stagecoach_roster_full_rejection", bark)
                    for bark in get_bark_list(self.stagecoach_roster_full_rejection)])

        res.extend([(f"{hero_name}+str_quest_too_hard", bark)
                    for bark in get_bark_list(self.quest_too_hard)])
        res.extend([(f"{hero_name}+str_quest_too_easy", bark)
                    for bark in get_bark_list(self.quest_too_easy)])

        if self.incompatible_self_party is not None:
            tem = get_bark_list(self.incompatible_self_party)
            # res.extend([(f"str_incompatible_party_{hero_name}_limit", bark) for bark in tem])
            res.extend([(f"str_incompatible_party_member_{hero_name}_limit", bark) for bark in tem])

        res.extend([(f"{hero_name}+str_bark_startmoving", bark)
                    for bark in get_bark_list(self.start_moving)])
        res.extend([(f"{hero_name}+str_bark_stopmoving", bark)
                    for bark in get_bark_list(self.stop_moving)])
        res.extend([(f"{hero_name}+str_bark_backingup", bark)
                    for bark in get_bark_list(self.backing_up)])
        res.extend([(f"{hero_name}+str_comment_trap_triggered", bark)
                    for bark in get_bark_list(self.comment_trap_triggered)])
        res.extend([(f"{hero_name}+str_bark_increasingstress", bark)
                    for bark in get_bark_list(self.increasing_stress)])
        res.extend([(f"{hero_name}+str_critbyhero", bark)
                    for bark in get_bark_list(self.crit_by_hero)])
        res.extend([(f"{hero_name}+str_combat_knockback", bark)
                    for bark in get_bark_list(self.combat_knock_back)])
        res.extend([(f"{hero_name}+str_combat_wastingtime", bark)
                    for bark in get_bark_list(self.combat_wasting_time)])
        res.extend([(f"{hero_name}+str_bark_bigwound", bark)
                    for bark in get_bark_list(self.big_wound)])
        res.extend([(f"{hero_name}+str_bark_bigwound_ally", bark)
                    for bark in get_bark_list(self.big_wound_ally)])
        res.extend([(f"{hero_name}+str_bark_deathsdoor", bark)
                    for bark in get_bark_list(self.deathsdoor)])
        res.extend([(f"{hero_name}+str_bark_deathsdoor_ally", bark)
                    for bark in get_bark_list(self.deathsdoor_ally)])
        res.extend([(f"{hero_name}+str_bark_deathsdoorsurvive", bark)
                    for bark in get_bark_list(self.deathsdoor_survive)])
        res.extend([(f"{hero_name}+str_bark_deathsdoorsurvive_ally", bark)
                    for bark in get_bark_list(self.deathsdoor_survive_ally)])
        res.extend([(f"{hero_name}+str_heart_attack", bark)
                    for bark in get_bark_list(self.heart_attack)])
        res.extend([(f"{hero_name}+str_bark_poisondot", bark)
                    for bark in get_bark_list(self.poison_dot)])
        res.extend([(f"{hero_name}+str_bark_bleeddot", bark)
                    for bark in get_bark_list(self.bleed_dot)])
        res.extend([(f"{hero_name}+str_bark_hp_heal_dot", bark)
                    for bark in get_bark_list(self.hp_heal_dot)])

        res.extend([(f"{hero_name}+str_bark_torch_0", bark)
                    for bark in get_bark_list(self.torch_0)])
        res.extend([(f"{hero_name}+str_bark_torch_1", bark)
                    for bark in get_bark_list(self.torch_1)])
        res.extend([(f"{hero_name}+str_bark_torch_2", bark)
                    for bark in get_bark_list(self.torch_2)])

        res.extend([(f"{hero_name}+str_bark_curiogood", bark)
                    for bark in get_bark_list(self.curio_good)])
        res.extend([(f"{hero_name}+str_bark_curiobad", bark)
                    for bark in get_bark_list(self.curio_bad)])
        res.extend([(f"{hero_name}+str_bark_curiomeh", bark)
                    for bark in get_bark_list(self.curio_meh)])

        res.extend([(f"{hero_name}+str_bark_stress_partyhigh", bark)
                    for bark in get_bark_list(self.stress_party_high)])
        res.extend([(f"{hero_name}+str_bark_stress_partylow", bark)
                    for bark in get_bark_list(self.stress_party_low)])
        res.extend([(f"{hero_name}+str_bark_hp_partyhigh", bark)
                    for bark in get_bark_list(self.hp_party_high)])
        res.extend([(f"{hero_name}+str_bark_hp_partylow", bark)
                    for bark in get_bark_list(self.hp_party_low)])
        res.extend([(f"{hero_name}+str_bark_stress_selfhigh", bark)
                    for bark in get_bark_list(self.stress_self_high)])
        res.extend([(f"{hero_name}+str_bark_stress_selflow", bark)
                    for bark in get_bark_list(self.stress_self_low)])
        res.extend([(f"{hero_name}+str_bark_hp_selfhigh", bark)
                    for bark in get_bark_list(self.hp_self_high)])
        res.extend([(f"{hero_name}+str_bark_hp_selflow", bark)
                    for bark in get_bark_list(self.hp_self_low)])
        res.extend([(f"{hero_name}+str_bark_party_poor_condition", bark)
                    for bark in get_bark_list(self.party_poor_condition)])
        res.extend([(f"{hero_name}+str_bark_party_great_condition", bark)
                    for bark in get_bark_list(self.party_great_condition)])
        res.extend([(f"{hero_name}+str_bark_firewood_low", bark)
                    for bark in get_bark_list(self.firewood_low)])
        res.extend([(f"{hero_name}+str_bark_firewood_high", bark)
                    for bark in get_bark_list(self.firewood_high)])
        res.extend([(f"{hero_name}+str_bark_provisions_low", bark)
                    for bark in get_bark_list(self.provisions_low)])
        res.extend([(f"{hero_name}+str_bark_provisions_high", bark)
                    for bark in get_bark_list(self.provisions_high)])
        res.extend([(f"{hero_name}+str_bark_companionship", bark) 
                    for bark in get_bark_list(self.companionship)])

        return res


class Mode(ModeEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    is_raid_default: bool = False
    always_guard_actor_base_class_ids: Optional[
        Sequence[Union[HeroEntry, MonsterEntry, MonsterClass, HeroClass, str]]] = None
    is_targetable: bool = True
    keep_rounds_in_ranks: bool = False
    stress_damage_per_turn: int = 0
    str_bark_override: Union[Sequence[str], str, None] = None
    affliction_combat_skill_id: Union[SkillEntry, str, None] = None
    battle_complete_combat_skill_id: Union[SkillEntry, str, None] = None
    battle_complete_sfx: Union[BankEntry, str, None] = None  # 战斗结束后使用上一个参数变身时触发的音效

    afflicted: Union[AnimationEntry, str, None] = None
    camp: Union[AnimationEntry, str, None] = None
    combat: Union[AnimationEntry, str, None] = None
    defend: Union[AnimationEntry, str, None] = None
    heroic: Union[AnimationEntry, str, None] = None
    idle: Union[AnimationEntry, str, None] = None
    investigate: Union[AnimationEntry, str, None] = None
    riposte: Union[AnimationEntry, str, None] = None
    walk: Union[AnimationEntry, str, None] = None

    actor_mode_name: Optional[str] = None
    str_skill_mode_info: Optional[str] = None
    entry_id: str = Field(default_factory=lambda x: AutoName().new_mode(), frozen=True)

    def bark_override_id(self) -> Optional[str]:
        if self.str_bark_override:
            return f"str_{self.id()}_bark"

    def __str__(self):
        res = f"mode: .id {self.id()}"
        if self.is_raid_default:
            res += " .is_raid_default true"
        if self.always_guard_actor_base_class_ids is not None and len(self.always_guard_actor_base_class_ids) > 0:
            tem = [get_entry_id(x) for x in self.always_guard_actor_base_class_ids]
            res += f" .always_guard_actor_base_class_ids {' '.join(tem)}"
        if not self.is_targetable:
            res += " .is_targetable false"
        if self.keep_rounds_in_ranks:
            res += " .keep_rounds_in_ranks true"
        if self.str_bark_override is not None:
            res += f" .bark_override_id {self.bark_override_id()}"
        if self.affliction_combat_skill_id is not None:
            res += f" .affliction_combat_skill_id {get_entry_id(self.affliction_combat_skill_id)}"
        if self.battle_complete_combat_skill_id is not None:
            res += f" .battle_complete_combat_skill_id {get_entry_id(self.battle_complete_combat_skill_id)}"
        if self.stress_damage_per_turn != 0:
            res += f" .stress_damage_per_turn {self.stress_damage_per_turn}"
        return res


class HealthBar(BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    damage_bottom: Union[str, Tuple[int, int, int, int]] = "#a32a00"
    damage_top: Union[str, Tuple[int, int, int, int]] = "#ffa500"
    heal_bottom: Union[str, Tuple[int, int, int, int]] = "#004e21"
    heal_top: Union[str, Tuple[int, int, int, int]] = "#00e500"
    current_bottom: Union[str, Tuple[int, int, int, int]] = "#150000"
    current_top: Union[str, Tuple[int, int, int, int]] = "#cd0000"


class RaidStartingItem(JsonData, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    item_type: ItemType = ItemType.ESTATE
    item_id: Union[ItemEntry, ItemID, str] = ""
    item_amount: int = 1

    def get_dict(self) -> dict:
        return {
            "type": self.item_type.value,
            "id": get_entry_id(self.item_id),
            "amount": self.item_amount
        }


class Hero(HeroEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    entry_id: str = Field(default_factory=lambda x: AutoName().new_hero(), frozen=True)

    id_index: int
    resistances: Resistance
    crit_effects: Sequence[Union[EffectEntry, str]] = Field(default_factory=list)
    skills: Sequence[SkillEntry] = Field(default_factory=list)
    target_rank: int
    weapons: Sequence[Weapon]
    armours: Sequence[Armour]
    weapon_images: Optional[Sequence[str]] = None
    armour_images: Optional[Sequence[str]] = None
    guild_header_image_path: Optional[str] = None
    portrait_roster_image_path: Optional[str] = None
    hp_reactions: Optional[Sequence[HpReaction]] = None
    death_reactions: Optional[Sequence[DeathReaction]] = None
    weapon_golds: Tuple[int, int, int, int] = (750, 1750, 3000, 6000)
    armour_golds: Tuple[int, int, int, int] = (750, 1750, 3000, 6000)
    tags: Optional[Sequence[Union[TagID, str]]] = None
    overstressed_modifier: Optional[Sequence[OverstressedModify]] = None
    deaths_door_buffs: Optional[Sequence[Union[BuffEntry, str]]] = None
    recovery_buffs: Optional[Sequence[Union[BuffEntry, str]]] = None
    recovery_heart_attack_buffs: Optional[Sequence[Union[BuffEntry, str]]] = None
    enter_effects: Optional[Sequence[Union[EffectEntry, str]]] = None
    enter_effect_round_cooldown: int = 6
    can_select_combat_skills: bool = True
    number_of_selected_combat_skills_max: int = 4
    can_self_party: bool = True  # TODO: 因为不了解多英雄互斥的写法，此处暂时写为只支持自身互斥
    generation: Optional[Generation] = None
    activity_modifier: Optional[ActivityModify] = None
    quirk_modifier: Optional[Sequence[Union[QuirkEntry, QuirkType, str]]] = None
    extra_battle_loot: Optional[ExtraLoot] = None
    extra_curio_loot: Optional[ExtraLoot] = None
    extra_stack_limit: Optional[Sequence[ExtraStackLimit]] = None
    extra_shard_bonus: Optional[float] = None
    death_fx: Union[DeathFx, str] = DeathFx.DEATH_MEDIUM
    actout_display: Optional[ActoutDisplay] = None
    sort_position_z_rank_override: Optional[int] = None
    hero_localization: Optional[HeroLocalization] = None
    base_mode: Optional[ModeEntry] = None
    health_bar: Optional[HealthBar] = None
    raid_starting_hero_items: Optional[Sequence[RaidStartingItem]] = None

    def _complete_weapons(self):
        if len(self.weapons) == 5:
            return
        weapon_0 = self.weapons[0]
        weapon_4 = self.weapons[1]
        x = [0, 4]
        target_x = [1, 2, 3]
        atk = [weapon_0.attack, weapon_4.attack]
        dmg_low = [weapon_0.damage_low, weapon_4.damage_low]
        dmg_high = [weapon_0.damage_high, weapon_4.damage_high]
        crit = [weapon_0.critical_rate, weapon_4.critical_rate]
        spd = [weapon_0.speed, weapon_4.speed]
        res = [weapon_0]
        for i in target_x:
            res.append(Weapon(
                attack=np.interp(i, x, atk),
                damage_low=round(np.interp(i, x, dmg_low)),
                damage_high=round(np.interp(i, x, dmg_high)),
                critical_rate=np.interp(i, x, crit),
                speed=round(np.interp(i, x, spd)) if i != 1 else math.floor(np.interp(i, x, spd))
            ))
        res.append(weapon_4)
        self.weapons = res

    def _complete_armours(self):
        if len(self.armours) == 5:
            return
        armour_0 = self.armours[0]
        armour_4 = self.armours[1]
        x = [0, 4]
        target_x = [1, 2, 3]
        defense = [armour_0.defense, armour_4.defense]
        prot = [armour_0.protection, armour_4.protection]
        hp = [armour_0.hp, armour_4.hp]
        spd = [armour_0.speed, armour_4.speed]
        res = [armour_0]
        for i in target_x:
            res.append(Armour(
                defense=np.interp(i, x, defense),
                protection=np.interp(i, x, prot),
                hp=round(np.interp(i, x, hp)),
                speed=round(np.interp(i, x, spd)) if i != 1 else math.floor(np.interp(i, x, spd))
            ))
        res.append(armour_4)
        self.armours = res

    @model_validator(mode="after")
    def _check_after(self):
        if self.id_index <= 17:
            raise ValueError("id_index must be greater than 17")
        if self.target_rank < 1 or self.target_rank > 4:
            raise ValueError("target_rank must be in range [1, 4]")

        if len(self.weapons) not in (2, 5):
            raise ValueError("num of weapons must be 2 or 5")
        if len(self.armours) not in (2, 5):
            raise ValueError("num of armours must be 2 or 5")
        self._complete_weapons()
        self._complete_armours()

        if self.tags is None:
            self.tags = (TagID.LIGHT, TagID.NON_RELIGIOUS, TagID.OUTSIDERS_BONFIRE)

        if self.guild_header_image_path is None:
            self.guild_header_image_path = os.path.join(DATA_PATH, "template", "hero", "unknown_guild_header.png")

        if self.portrait_roster_image_path is None:
            self.portrait_roster_image_path = os.path.join(DATA_PATH, "template", "hero", "unknown_portrait_roster.png")

        eqp_dir = os.path.join(DATA_PATH, "template", "icons_equip")
        if self.weapon_images is None:
            self.weapon_images = (
                os.path.join(eqp_dir, "eqp_weapon_0.png"),
                os.path.join(eqp_dir, "eqp_weapon_1.png"),
                os.path.join(eqp_dir, "eqp_weapon_2.png"),
                os.path.join(eqp_dir, "eqp_weapon_3.png"),
                os.path.join(eqp_dir, "eqp_weapon_4.png"),
            )
        if self.armour_images is None:
            self.armour_images = (
                os.path.join(eqp_dir, "eqp_armour_0.png"),
                os.path.join(eqp_dir, "eqp_armour_1.png"),
                os.path.join(eqp_dir, "eqp_armour_2.png"),
                os.path.join(eqp_dir, "eqp_armour_3.png"),
                os.path.join(eqp_dir, "eqp_armour_4.png"),
            )

        if self.deaths_door_buffs is None:
            self.deaths_door_buffs = (
                "deathsdoorACCDebuff",
                "deathsdoorDMGLowDebuff",
                "deathsdoorDMGHighDebuff",
                "deathsdoorSPDDebuff",
                "deathsdoorSRDebuff",
            )
        if self.recovery_buffs is None:
            self.recovery_buffs = (
                "mortalityACCDebuff",
                "mortalityDMGLowDebuff",
                "mortalityDMGHighDebuff",
                "mortalitySPDDebuff",
                "mortalitySRDebuff",
            )
        if self.recovery_heart_attack_buffs is None:
            self.recovery_heart_attack_buffs = (
                "heartattackACCDebuff",
                "heartattackDMGLowDebuff",
                "heartattackDMGHighDebuff",
                "heartattackSPDDebuff",
                "heartattackSRDebuff",
            )

        if self.generation is None:
            self.generation = Generation()

        return self

    def get_modes(self) -> List[ModeEntry]:
        modes = {}
        for skill in self.skills:  # type: Skill
            if isinstance(skill.skill_info, SkillInfo):
                skill_info = [skill.skill_info]
            else:
                skill_info = skill.skill_info
            for info in skill_info:
                if info.valid_modes_and_effects is not None:
                    for mode_effects in info.valid_modes_and_effects:
                        if mode_effects.valid_mode.id() not in modes:
                            modes[mode_effects.valid_mode.id()] = mode_effects.valid_mode
        return list(modes.values())

    def info(self) -> str:
        # 抗性
        res = [str(self.resistances)]

        # 暴击特效
        if len(self.crit_effects) > 0:
            effects = " ".join([f'"{get_entry_id(effect)}"' for effect in self.crit_effects])
            res.append(f'crit: .effects {effects}')

        # 生命值变化
        if self.hp_reactions is not None:
            res.append("\n".join([str(reaction) for reaction in self.hp_reactions]))

        # 武器和护甲
        res.append("\n".join([weapon.info(level, self.id()) for level, weapon in enumerate(self.weapons)]))
        res.append("\n".join([armour.info(level, self.id()) for level, armour in enumerate(self.armours)]))

        # 技能
        for skill in self.skills:  # type: Skill
            res.append(skill.info())

        # 标签
        tem = []
        for tag in self.tags:
            tem.append(f'tag: .id "{get_entry_id(tag)}"')
        # tem.append(f'tag: .id "{self.id()}"')
        res.append("\n".join(tem))

        # 修改爆压后获得 trait 的概率
        if self.overstressed_modifier is not None:
            tem = []
            for modify in self.overstressed_modifier:
                tem.append(f'overstressed_modifier: .override_trait_type_ids {get_entry_id(modify.trait_id)} '
                           f'.override_trait_type_chances {modify.chance}')
            res.append("\n".join(tem))

        # 修改城镇活动减压效果
        if self.activity_modifier is not None:
            activity_ids = " ".join([activity.value for activity in self.activity_modifier.activity_ids])
            res.append(f'activity_modifier: .override_valid_activity_ids {activity_ids} '
                       f'.override_stress_removal_amount_low {self.activity_modifier.stress_removal_amount_low} '
                       f'.override_stress_removal_amount_high {self.activity_modifier.stress_removal_amount_high}')

        # 修改冲突怪癖
        if self.quirk_modifier is not None:
            quirks = [get_entry_id(quirk) for quirk in self.quirk_modifier]
            quirks = split_list(quirks, 8)
            tem = []
            for quirk in quirks:
                tem.append(f'quirk_modifier: .incompatible_class_ids {" ".join(quirk)}')
            res.append("\n".join(tem))

        # 死亡特效
        if self.death_reactions is not None:
            res.append("\n".join([str(reaction) for reaction in self.death_reactions]))

        # 死门特效
        tem = []
        if self.deaths_door_buffs is not None and len(self.deaths_door_buffs) > 0:
            tem.append(f'.buffs {" ".join([get_entry_id(buff) for buff in self.deaths_door_buffs])}')
        if self.recovery_buffs is not None and len(self.recovery_buffs) > 0:
            tem.append(f'.recovery_buffs {" ".join([get_entry_id(buff) for buff in self.recovery_buffs])}')
        if self.recovery_heart_attack_buffs is not None and len(self.recovery_heart_attack_buffs) > 0:
            tem.append(f'.recovery_heart_attack_buffs '
                       f'{" ".join([get_entry_id(buff) for buff in self.recovery_heart_attack_buffs])}')
        if self.enter_effects is not None and len(self.enter_effects) > 0:
            tem.append(f'.enter_effects {" ".join([get_entry_id(effect) for effect in self.enter_effects])} '
                       f'.enter_effect_round_cooldown {self.enter_effect_round_cooldown}')
        if len(tem) > 0:
            res.append(f'deaths_door: {" ".join(tem)}')

        # 推荐位置
        res.append(f'controlled: .target_rank {self.target_rank}')

        # 英雄编号
        res.append(f'id_index: .index {self.id_index}')

        # 技能选择
        res.append(f'skill_selection: .can_select_combat_skills {bool_to_lower_str(self.can_select_combat_skills)} '
                   f'.number_of_selected_combat_skills_max {self.number_of_selected_combat_skills_max}')

        # 能否自组队
        if not self.can_self_party:
            res.append(f'incompatible_party_member: .id {self.id()}_limit .hero_tag {self.id()}')

        # 额外战斗掉落
        if self.extra_battle_loot is not None:
            code = get_entry_id(self.extra_battle_loot.code)
            res.append(f'extra_battle_loot: .code "{code}" .count {self.extra_battle_loot.count}')

        # 额外奇物互动掉落
        if self.extra_curio_loot is not None:
            code = get_entry_id(self.extra_curio_loot.code)
            res.append(f'extra_curio_loot: .code "{code}" .count {self.extra_curio_loot.count}')

        # 额外物品堆叠上限
        if self.extra_stack_limit is not None:
            for limit in self.extra_stack_limit:
                res.append(f'extra_stack_limit: .id {limit.id(self.id())}')

        # 额外奖励加成
        if self.extra_shard_bonus is not None:
            res.append(f'extra_shard_bonus: .amount {self.extra_shard_bonus}')

        # 模式
        modes = self.get_modes()
        if len(modes) > 0:
            res.append("\n".join([str(mode) for mode in modes]))

        # 马车生成参数
        res.append(str(self.generation))

        # 演出动画
        # if self.actout_display is not None:
        #     res.append(str(self.actout_display))

        return "\n\n".join(res)

    def art(self) -> str:
        res = [f'commonfx: .deathfx {self.death_fx.value}']

        if self.health_bar is not None:
            res.append(f'health_bar: .type "{self.id()}"')

        weapon = "".join(f'weapon: .name "{self.id()}_weapon_{i}" .icon "eqp_weapon_{i}.png"\n' for i in range(5))
        armour = "".join(f'armour: .name "{self.id()}_armour_{i}" .icon "eqp_armour_{i}.png"\n' for i in range(5))
        res.append(weapon.rstrip("\n"))
        res.append(armour.rstrip("\n"))

        tem = []
        for skill in self.skills:  # type: Skill
            tem.append(skill.art())
        if len(tem) > 0:
            res.append("\n".join(tem))

        if self.actout_display is not None:
            res.append(str(self.actout_display))

        if self.sort_position_z_rank_override is not None:
            res.append(f'rendering: .sort_position_z_rank_override {self.sort_position_z_rank_override}')

        return "\n\n".join(res)

    @staticmethod
    def _get_requirement_dict(
            code: int,
            cost: int,
            requirements: Sequence[Tuple[str, str]],
            resolve_level: int
    ):
        currency_cost = [{"type": "gold", "amount": cost}]
        prerequisite_requirements = [
            {
                "tree_id": requirement[0],
                "requirement_code": requirement[1]
            }
            for requirement in requirements
        ]
        return {
            "code": str(code),
            "currency_cost": currency_cost,
            "prerequisite_requirements": prerequisite_requirements,
            "prerequisite_resolve_level": resolve_level
        }

    def _get_equipment_dict(
            self, equipment_type: str,
            golds: Tuple[int, int, int, int]
    ):
        codes = ["a", "b", "c", "d"]
        levels = [1, 2, 3, 5]
        requirements = []
        for i in range(4):
            if i != 0:
                tem = [(f"{self.id()}.{equipment_type}", str(i - 1))]
            else:
                tem = []
            tem.append((f"blacksmith.{equipment_type}", codes[i]))
            requirements.append(self._get_requirement_dict(
                code=i,
                cost=golds[i],
                requirements=tem,
                resolve_level=levels[i]
            ))
        return {
            "id": f"{self.id()}.{equipment_type}",
            "is_instanced": True,
            "tags": [equipment_type, "first_level_not_upgrade"],
            "requirements": requirements
        }

    def _get_combat_skill_dict(self, skill_name: str, level_num: int, upgrade_golds: Sequence[int]):
        codes = ["a", "b", "c", "d"]
        levels = [0, 1, 2, 3, 5]
        requirements = []
        for i in range(level_num):
            if i != 0:
                tem = [
                    (f"{self.id()}.{skill_name}", str(i - 1)),
                    ("guild.skill_levels", codes[i - 1])
                ]
            else:
                tem = []
            requirements.append(self._get_requirement_dict(
                code=i,
                cost=upgrade_golds[i],
                requirements=tem,
                resolve_level=levels[i]
            ))
        return {
            "id": f"{self.id()}.{skill_name}",
            "is_instanced": True,
            "tags": ["combat_skill"],
            "requirements": requirements
        }

    def get_upgrade_dict(self) -> dict:
        res = [
            self._get_equipment_dict("weapon", self.weapon_golds),
            self._get_equipment_dict("armour", self.armour_golds)
        ]
        for skill in self.skills:  # type: Skill
            if isinstance(skill.skill_info, SkillInfo):
                info = [skill.skill_info]
            else:
                info = skill.skill_info
            if len(info) > 1 or skill.can_upgraded:
                res.append(self._get_combat_skill_dict(
                    skill.id(),
                    len(info),
                    skill.upgrade_golds
                ))
        return {"trees": res}


if __name__ == '__main__':
    from xddtools.entries.skill import ModeEffects

    h = Hero(
        id_index=18,
        target_rank=1,
        resistances=Resistance(
            stun=0.2,
            poison=0.2,
            bleed=0.2,
            disease=0.2,
            move=0.2,
            trap=0.2,
            debuff=0.2,
            death_blow=0.6
        ),
        crit_effects=[],
        skills=[Skill(
            skill_info=SkillInfo(
                valid_modes_and_effects=[
                    ModeEffects(
                        valid_mode=Mode(),
                        effects=[]
                    ),
                    ModeEffects(
                        valid_mode=Mode(is_raid_default=True),
                        effects=[]
                    )
                ]
            )
        )],
        tags=(TagID.LIGHT, TagID.NON_RELIGIOUS, TagID.OUTSIDERS_BONFIRE),
        weapons=(
            Weapon(attack=0, damage_low=5, damage_high=7, critical_rate=0.05, speed=5),
            Weapon(attack=1, damage_low=11, damage_high=16, critical_rate=0.09, speed=9),
        ),
        armours=(
            Armour(defense=0, protection=0, hp=20, speed=5),
            Armour(defense=1, protection=1, hp=100, speed=8),
        ),
    )
    print(h.art())

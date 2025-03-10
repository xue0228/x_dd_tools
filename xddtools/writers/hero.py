import os
from dataclasses import dataclass
from typing import Optional, Iterable, Tuple, Union, List

from xddtools.animation import Animation
from xddtools.base import BaseID, LocalizationWriter
from xddtools.base import BaseJsonData, BaseWriter
from xddtools.buffs import Buff
from xddtools.effects import Effect
from xddtools.enums import Level, TagID, DeathFx
from xddtools.hero import Resistance, Weapon, Armour, OverstressedModify, Generation, ActivityModify, ExtraLoot, \
    ExtraStackLimit, ActoutDisplay, HeroLocalization, Mode, WeaponGroup, ArmourGroup
from xddtools.items import Item
from xddtools.loot import LootTable
from xddtools.path import HERO_SAVE_DIR, DATA_PATH
from xddtools.path import HERO_UPGRADE_SAVE_DIR, HERO_UPGRADE_FILE_EXTENSION
from xddtools.quirks import Quirk
from xddtools.skills import Skill
from xddtools.traits import Trait
from xddtools.utils import bool_to_lower_str, resize_image, split_list, \
    make_dirs, get_rename_skel_dict_func
from xddtools.writers import BuffWriter, EffectWriter, DDWriter, QuirkWriter, LootTableWriter, ItemWriter


@dataclass(frozen=True)
class CurrencyCost:
    amount: int
    type: str = "gold"


@dataclass(frozen=True)
class PrerequisiteRequirement:
    tree_id: str
    requirement_code: str


class HeroUpgradeWriter(BaseJsonData, BaseWriter):
    def __init__(
            self,
            hero_name: str,
            combat_skills: Tuple[Union[Skill, str], ...],
            combat_skill_golds: Tuple[Tuple[int, int, int, int, int], ...] = (
                    (1000, 250, 750, 1250, 2500),
            ),
            weapon_golds: Tuple[int, int, int, int] = (750, 1750, 3000, 6000),
            armour_golds: Tuple[int, int, int, int] = (750, 1750, 3000, 6000),
    ):
        if len(combat_skill_golds) != 1 and len(combat_skills) != len(combat_skill_golds):
            raise ValueError("combat_skills and combat_skill_golds must have the same length")
        self.combat_skills = combat_skills
        self.combat_skill_golds = combat_skill_golds
        self.weapon_golds = weapon_golds
        self.armour_golds = armour_golds
        super().__init__(
            name=hero_name,
            items=None,
            relative_save_dir=HERO_UPGRADE_SAVE_DIR,
            extension=HERO_UPGRADE_FILE_EXTENSION
        )

    @staticmethod
    def get_requirement_dict(
            code: int,
            currency_cost: Union[CurrencyCost, Tuple[CurrencyCost, ...]] = (),
            prerequisite_requirements: Union[PrerequisiteRequirement, Tuple[PrerequisiteRequirement, ...]] = (),
            prerequisite_resolve_level: int = 0
    ):
        if isinstance(currency_cost, CurrencyCost):
            currency_cost = [{"type": currency_cost.type, "amount": currency_cost.amount}]
        else:
            currency_cost = [
                {"type": currency_cost.type, "amount": currency_cost.amount}
                for currency_cost in currency_cost
            ]

        if isinstance(prerequisite_requirements, PrerequisiteRequirement):
            prerequisite_requirements = [{
                "tree_id": prerequisite_requirements.tree_id,
                "requirement_code": prerequisite_requirements.requirement_code
            }]
        else:
            prerequisite_requirements = [
                {
                    "tree_id": prerequisite_requirements.tree_id,
                    "requirement_code": prerequisite_requirements.requirement_code
                }
                for prerequisite_requirements in prerequisite_requirements
            ]

        return {
            "code": str(code),
            "currency_cost": currency_cost,
            "prerequisite_requirements": prerequisite_requirements,
            "prerequisite_resolve_level": prerequisite_resolve_level
        }

    def get_equipment_dict(
            self,
            equipment_type: str,
            golds: Tuple[int, int, int, int] = (750, 1750, 3000, 6000)
    ):
        codes = ["a", "b", "c", "d"]
        levels = [1, 2, 3, 5]
        requirements = []
        for i in range(4):
            if i != 0:
                tem = [PrerequisiteRequirement(
                    tree_id=f"{self.id}.{equipment_type}",
                    requirement_code=str(i - 1)
                )]
            else:
                tem = []
            tem.append(PrerequisiteRequirement(
                tree_id=f"blacksmith.{equipment_type}",
                requirement_code=codes[i]
            ))
            requirements.append(self.get_requirement_dict(
                code=i,
                currency_cost=CurrencyCost(amount=golds[i], type="gold"),
                prerequisite_requirements=tuple(tem),
                prerequisite_resolve_level=levels[i]
            ))
        return {
            "id": f"{self.id}.{equipment_type}",
            "is_instanced": True,
            "tags": [equipment_type, "first_level_not_upgrade"],
            "requirements": requirements
        }

    def get_combat_skill_dict(
            self,
            skill_name: str,
            golds: Tuple[int, int, int, int, int] = (1000, 250, 750, 1250, 2500)
    ):
        codes = ["a", "b", "c", "d"]
        levels = [0, 1, 2, 3, 5]
        requirements = []
        for i in range(5):
            if i != 0:
                tem = [
                    PrerequisiteRequirement(
                        tree_id=f"{self.id}.{skill_name}",
                        requirement_code=str(i - 1)
                    ),
                    PrerequisiteRequirement(
                        tree_id="guild.skill_levels",
                        requirement_code=codes[i - 1]
                    )
                ]
            else:
                tem = []
            requirements.append(self.get_requirement_dict(
                code=i,
                currency_cost=CurrencyCost(amount=golds[i], type="gold"),
                prerequisite_requirements=tuple(tem),
                prerequisite_resolve_level=levels[i]
            ))
        return {
            "id": f"{self.id}.{skill_name}",
            "is_instanced": True,
            "tags": ["combat_skill"],
            "requirements": requirements
        }

    def dict(self) -> dict:
        res = [
            self.get_equipment_dict("weapon", self.weapon_golds),
            self.get_equipment_dict("armour", self.armour_golds)
        ]
        if len(self.combat_skill_golds) == 1:
            for skill in self.combat_skills:
                skill = skill.id if isinstance(skill, Skill) else skill
                res.append(self.get_combat_skill_dict(skill, self.combat_skill_golds[0]))
        else:
            for skill, gold in zip(self.combat_skills, self.combat_skill_golds):
                skill = skill.id if isinstance(skill, Skill) else skill
                res.append(self.get_combat_skill_dict(skill, gold))
        return {"trees": res}


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
            weapon_image_path: Optional[Iterable[str]] = None,
            armour_image_path: Optional[Iterable[str]] = None,
            guild_header_image_path: Optional[str] = None,
            portrait_roster_image_path: Optional[str] = None,
            weapon_golds: Tuple[int, int, int, int] = (750, 1750, 3000, 6000),
            armour_golds: Tuple[int, int, int, int] = (750, 1750, 3000, 6000),
            combat_skill_golds: Tuple[int, int, int, int, int] = (1000, 250, 750, 1250, 2500),
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
            actout_display: Optional[ActoutDisplay] = None,
            sort_position_z_rank_override: Optional[int] = None,
            hero_localization: Optional[HeroLocalization] = None,
            base_mode: Optional[Mode] = None,

            buff_writer: Optional[BuffWriter] = None,
            effect_writer: Optional[EffectWriter] = None,
            quirk_writer: Optional[QuirkWriter] = None,
            table_writer: Optional[LootTableWriter] = None,
            item_writer: Optional[ItemWriter] = None,
            localization_writer: Optional[LocalizationWriter] = None,
            dd_writer: Optional[DDWriter] = None,
    ):
        super().__init__(hero_name)

        if id_index <= 17:
            raise ValueError("id_index must be greater than 17")

        if target_rank < 1 or target_rank > 4:
            raise ValueError("target_rank must be in range [1, 4]")

        if tags is None:
            tags = (TagID.LIGHT, TagID.NON_RELIGIOUS, TagID.OUTSIDERS_BONFIRE)

        if guild_header_image_path is None:
            guild_header_image_path = os.path.join(DATA_PATH, "template", "hero", "unknown_guild_header.png")

        if portrait_roster_image_path is None:
            portrait_roster_image_path = os.path.join(DATA_PATH, "template", "hero", "unknown_portrait_roster.png")

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
        self.actout_display = actout_display
        self.sort_position_z_rank_override = sort_position_z_rank_override
        self.hero_localization = hero_localization
        self.base_mode = base_mode
        self._guild_header_image_path = guild_header_image_path
        self._portrait_roster_image_path = portrait_roster_image_path

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
        self._quirk_writer = quirk_writer
        self._table_writer = table_writer
        self._item_writer = item_writer

        if dd_writer is not None:
            self._buff_writer = dd_writer.buff_writer
            self._effect_writer = dd_writer.effect_writer
            self._localization_writer = dd_writer.localization_writer
            self._quirk_writer = dd_writer.quirk_writer
            self._table_writer = dd_writer.loot_writer
            self._item_writer = dd_writer.item_writer

        self._upgrade_skills = set()
        for skill in self.skills:
            if skill.level != Level.ZERO:
                self._upgrade_skills.add(skill.id)
        self._upgrade_writer = HeroUpgradeWriter(
            hero_name=hero_name,
            combat_skills=tuple(self._upgrade_skills),
            combat_skill_golds=(combat_skill_golds,),
            weapon_golds=weapon_golds,
            armour_golds=armour_golds,
        )

    def _init_writers(self):
        if self._effect_writer is not None and self.crit_effects is not None:
            for effect in self.crit_effects:
                if isinstance(effect, Effect):
                    self._effect_writer.add_item(effect)

        if self._buff_writer is not None:
            if self.deaths_door_buffs is not None:
                for buff in self.deaths_door_buffs:
                    if isinstance(buff, Buff):
                        self._buff_writer.add_item(buff)
                        if self._localization_writer is not None:
                            self._localization_writer.add_entries(buff.entries)

            if self.recovery_buffs is not None:
                for buff in self.recovery_buffs:
                    if isinstance(buff, Buff):
                        self._buff_writer.add_item(buff)
                        if self._localization_writer is not None:
                            self._localization_writer.add_entries(buff.entries)

            if self.recovery_heart_attack_buffs is not None:
                for buff in self.recovery_heart_attack_buffs:
                    if isinstance(buff, Buff):
                        self._buff_writer.add_item(buff)
                        if self._localization_writer is not None:
                            self._localization_writer.add_entries(buff.entries)

        if self._quirk_writer is not None and self.quirk_modifier is not None:
            for quirk in self.quirk_modifier:
                if isinstance(quirk, Quirk):
                    self._quirk_writer.add_item(quirk)
                    if self._localization_writer is not None:
                        self._localization_writer.add_entries(quirk.entries)

        if self._table_writer is not None:
            if self.extra_battle_loot is not None and isinstance(self.extra_battle_loot.code, LootTable):
                self._table_writer.add_item(self.extra_battle_loot.code)
            if self.extra_curio_loot is not None and isinstance(self.extra_curio_loot.code, LootTable):
                self._table_writer.add_item(self.extra_curio_loot.code)

        if self._item_writer is not None and self.extra_stack_limit is not None:
            for item in self.extra_stack_limit:
                if isinstance(item.item_id, Item):
                    self._item_writer.add_item(item.item_id)
                    if self._localization_writer is not None:
                        self._localization_writer.add_entries(item.item_id.entries)

        self._modes = {}
        for skill in self.skills:
            if skill.level == Level.ZERO:
                if skill.localization is not None:
                    if self._localization_writer is not None:
                        self._localization_writer.add_entry(
                            f"combat_skill_name_{self.id}_{skill.id}", skill.localization
                        )
                        if skill.id in self._upgrade_skills:
                            self._localization_writer.add_entry(
                                f"upgrade_tree_name_{self.id}.{skill.id}", skill.localization
                            )

            if self._effect_writer is not None:
                if skill.effect_ids is not None:
                    for effect in skill.effect_ids:
                        if isinstance(effect, Effect):
                            self._effect_writer.add_item(effect)

                if skill.valid_modes_and_effects is not None:
                    for _, effects in skill.valid_modes_and_effects:
                        if effects is not None:
                            for effect in effects:
                                if isinstance(effect, Effect):
                                    self._effect_writer.add_item(effect)

            if skill.valid_modes_and_effects is not None:
                for mode, _ in skill.valid_modes_and_effects:
                    if isinstance(mode, Mode):
                        self._modes[mode.id] = mode
                        if self._localization_writer is not None:
                            self._localization_writer.add_entries(mode.entries)

        if self.hero_localization is not None:
            if self._localization_writer is not None:
                self._localization_writer.add_entries(self.hero_localization.get_entries(self.id))

    def info(self) -> str:
        res = [str(self.resistances)]

        effects = [effect.id if isinstance(effect, Effect) else effect for effect in self.crit_effects]
        effects = " ".join([f'"{effect}"' for effect in effects])
        res.append(f'crit: .effects {effects}\n')

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
        if len(tem) > 0:
            tem = f'.buffs {" ".join(tem)}'
        else:
            tem = None
        tem2 = []
        for buff in self.recovery_buffs:
            buff = buff.id if isinstance(buff, Buff) else buff
            tem2.append(buff)
        if len(tem2) > 0:
            tem2 = f'.recovery_buffs {" ".join(tem2)}'
        else:
            tem2 = None
        tem3 = []
        for buff in self.recovery_heart_attack_buffs:
            buff = buff.id if isinstance(buff, Buff) else buff
            tem3.append(buff)
        if len(tem3) > 0:
            tem3 = f'.recovery_heart_attack_buffs {" ".join(tem3)}'
        else:
            tem3 = None
        death_tem = [item for item in [tem, tem2, tem3] if item is not None]
        if len(death_tem) > 0:
            res.append(f'deaths_door: {" ".join(death_tem)}\n')

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

        if len(self._modes) > 0:
            for mode in self._modes.values():
                res.append(str(mode))

        res.append(str(self.generation))

        return "".join(res)

    def art(self) -> str:
        res = [f'commonfx: .deathfx {self.death_fx.value}\n']

        weapon = "".join(f'weapon: .name "{self.id}_weapon_{i}" .icon "eqp_weapon_{i}.png"\n' for i in range(5))
        armour = "".join(f'armour: .name "{self.id}_armour_{i}" .icon "eqp_armour_{i}.png"\n' for i in range(5))
        res.append(weapon)
        res.append(armour)

        skill = "".join([item.art for item in self.skills if item.level == Level.ZERO])
        res.append(skill)

        if self.actout_display is not None:
            res.append(str(self.actout_display))

        if self.sort_position_z_rank_override is not None:
            res.append(f'rendering: .sort_position_z_rank_override {self.sort_position_z_rank_override}\n')

        return "\n".join(res)

    def __str__(self):
        return "\n".join([self.info(), self.art()])

    def export(self, root_dir: Optional[str] = None) -> Tuple[str]:
        self._init_writers()

        if root_dir is None:
            root_dir = "./"
        res: List[str, ...] = []
        hero_dir = os.path.join(root_dir, HERO_SAVE_DIR, self.id)

        # 导出info文件
        file = os.path.join(hero_dir, f'{self.id}.info.darkest')
        make_dirs(os.path.dirname(file))
        with open(file, 'w', encoding='utf-8') as f:
            f.write(self.info())
        res.append(os.path.normpath(file))

        # 导出art文件
        file = os.path.join(hero_dir, f'{self.id}.art.darkest')
        make_dirs(os.path.dirname(file))
        with open(file, 'w', encoding='utf-8') as f:
            f.write(self.art())
        res.append(os.path.normpath(file))

        # 导出升级文件
        self._upgrade_writer.export(root_dir)

        # 导出武器护甲图片
        self._weapon_group.export_image(root_dir)
        self._armour_group.export_image(root_dir)

        # 导出升级背景图
        file = os.path.join(hero_dir, f'{self.id}_guild_header.png')
        make_dirs(os.path.dirname(file))
        res.append(resize_image(self._guild_header_image_path, file, (715, 630)))

        # 导出头像图片
        file = os.path.join(hero_dir, f'{self.id}_A', f'{self.id}_portrait_roster.png')
        make_dirs(os.path.dirname(file))
        res.append(resize_image(self._portrait_roster_image_path, file, (85, 85)))

        # 导出技能动画
        skills = set()
        for skill in self.skills:
            if skill.id in skills or skill.level != Level.ZERO:
                continue
            if skill.image_path is None:
                src = os.path.join(DATA_PATH, "template", "hero", "unknown_skill.png")
            else:
                src = skill.image_path
            if skill.icon is None:
                dst = os.path.join(hero_dir, f'{self.id}.ability.{skill.id}.png')
            else:
                dst = os.path.join(hero_dir, f'{self.id}.ability.{skill.icon}.png')
            if skill.icon != "generic_move":
                make_dirs(os.path.dirname(dst))
                res.append(resize_image(src, dst, (72, 72)))

            if skill.anim is not None and isinstance(skill.anim, Animation):
                res.extend(skill.anim.copy_and_rename_animation(
                    root_dir=root_dir,
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func(skill.anim.id)
                ))
            if skill.fx is not None and isinstance(skill.fx, Animation):
                res.extend(skill.fx.copy_and_rename_animation(
                    root_dir=root_dir,
                    is_fx=True,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func(skill.fx.id)
                ))
            if skill.targfx is not None and isinstance(skill.targfx, Animation):
                res.extend(skill.targfx.copy_and_rename_animation(
                    root_dir=root_dir,
                    is_fx=True,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func(skill.targfx.id)
                ))
            if skill.targchestfx is not None and isinstance(skill.targchestfx, Animation):
                res.extend(skill.targchestfx.copy_and_rename_animation(
                    root_dir=root_dir,
                    is_fx=True,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func(skill.targchestfx.id)
                ))
            if skill.targheadfx is not None and isinstance(skill.targheadfx, Animation):
                res.extend(skill.targheadfx.copy_and_rename_animation(
                    root_dir=root_dir,
                    is_fx=True,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func(skill.targheadfx.id)
                ))
            if skill.misstargfx is not None and isinstance(skill.misstargfx, Animation):
                res.extend(skill.misstargfx.copy_and_rename_animation(
                    root_dir=root_dir,
                    is_fx=True,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func(skill.misstargfx.id)
                ))
            if skill.misstargheadfx is not None and isinstance(skill.misstargheadfx, Animation):
                res.extend(skill.misstargheadfx.copy_and_rename_animation(
                    root_dir=root_dir,
                    is_fx=True,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func(skill.misstargheadfx.id)
                ))
            if skill.misstargchestfx is not None and isinstance(skill.misstargchestfx, Animation):
                res.extend(skill.misstargchestfx.copy_and_rename_animation(
                    root_dir=root_dir,
                    is_fx=True,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func(skill.misstargchestfx.id)
                ))
            skills.add(skill.id)
            # if skill.custom_target_anim is not None and isinstance(skill.custom_target_anim, Animation):
            #     res.extend(skill.custom_target_anim.copy_and_rename_animation(
            #         root_dir=root_dir,
            #         is_fx=False,
            #         hero_name=self.id,
            #         dict_func=get_rename_skel_dict_func(skill.custom_target_anim.id)
            #     ))

        # 导出演出动画
        if self.actout_display is not None:
            if self.actout_display.attack_friendly_anim is not None \
                    and isinstance(self.actout_display.attack_friendly_anim, Animation):
                res.extend(self.actout_display.attack_friendly_anim.copy_and_rename_animation(
                    root_dir=root_dir,
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func(self.actout_display.attack_friendly_anim.id)
                ))
            if self.actout_display.attack_friendly_fx is not None \
                    and isinstance(self.actout_display.attack_friendly_fx, Animation):
                res.extend(self.actout_display.attack_friendly_fx.copy_and_rename_animation(
                    root_dir=root_dir,
                    is_fx=True,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func(self.actout_display.attack_friendly_fx.id)
                ))
            if self.actout_display.attack_friendly_targchestfx is not None \
                    and isinstance(self.actout_display.attack_friendly_targchestfx, Animation):
                res.extend(self.actout_display.attack_friendly_targchestfx.copy_and_rename_animation(
                    root_dir=root_dir,
                    is_fx=True,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func(self.actout_display.attack_friendly_targchestfx.id)
                ))

        # 导出无模式英雄基本动画
        if self.base_mode is not None:
            if self.base_mode.afflicted is not None and isinstance(self.base_mode.afflicted, Animation):
                res.extend(self.base_mode.afflicted.copy_and_rename_animation(
                    root_dir=root_dir,
                    anim_name="afflicted",
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func("afflicted")
                ))
            if self.base_mode.camp is not None and isinstance(self.base_mode.camp, Animation):
                res.extend(self.base_mode.camp.copy_and_rename_animation(
                    root_dir=root_dir,
                    anim_name="camp",
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func("camp")
                ))
            if self.base_mode.combat is not None and isinstance(self.base_mode.combat, Animation):
                res.extend(self.base_mode.combat.copy_and_rename_animation(
                    root_dir=root_dir,
                    anim_name="combat",
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func("combat")
                ))
            if self.base_mode.death is not None and isinstance(self.base_mode.death, Animation):
                res.extend(self.base_mode.death.copy_and_rename_animation(
                    root_dir=root_dir,
                    anim_name="death",
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func("death")
                ))
            if self.base_mode.defend is not None and isinstance(self.base_mode.defend, Animation):
                res.extend(self.base_mode.defend.copy_and_rename_animation(
                    root_dir=root_dir,
                    anim_name="defend",
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func("defend")
                ))
            if self.base_mode.heroic is not None and isinstance(self.base_mode.heroic, Animation):
                res.extend(self.base_mode.heroic.copy_and_rename_animation(
                    root_dir=root_dir,
                    anim_name="heroic",
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func("heroic")
                ))
            if self.base_mode.idle is not None and isinstance(self.base_mode.idle, Animation):
                res.extend(self.base_mode.idle.copy_and_rename_animation(
                    root_dir=root_dir,
                    anim_name="idle",
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func("idle")
                ))
            if self.base_mode.investigate is not None and isinstance(self.base_mode.investigate, Animation):
                res.extend(self.base_mode.investigate.copy_and_rename_animation(
                    root_dir=root_dir,
                    anim_name="investigate",
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func("investigate")
                ))
            if self.base_mode.riposte is not None and isinstance(self.base_mode.riposte, Animation):
                res.extend(self.base_mode.riposte.copy_and_rename_animation(
                    root_dir=root_dir,
                    anim_name="riposte",
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func("riposte")
                ))
            if self.base_mode.walk is not None and isinstance(self.base_mode.walk, Animation):
                res.extend(self.base_mode.walk.copy_and_rename_animation(
                    root_dir=root_dir,
                    anim_name="walk",
                    is_fx=False,
                    hero_name=self.id,
                    dict_func=get_rename_skel_dict_func("walk")
                ))

        # 导出有模式英雄基本动画
        if len(self._modes) > 0:
            for k, v in self._modes:
                if v.afflicted is not None and isinstance(v.afflicted, Animation):
                    res.extend(v.afflicted.copy_and_rename_animation(
                        root_dir=root_dir,
                        anim_name=f"afflicted_{k}",
                        is_fx=False,
                        hero_name=self.id,
                        dict_func=get_rename_skel_dict_func(f"afflicted_{k}")
                    ))
                if v.camp is not None and isinstance(v.camp, Animation):
                    res.extend(v.camp.copy_and_rename_animation(
                        root_dir=root_dir,
                        anim_name=f"camp_{k}",
                        is_fx=False,
                        hero_name=self.id,
                        dict_func=get_rename_skel_dict_func(f"camp_{k}")
                    ))
                if v.combat is not None and isinstance(v.combat, Animation):
                    res.extend(v.combat.copy_and_rename_animation(
                        root_dir=root_dir,
                        anim_name=f"combat_{k}",
                        is_fx=False,
                        hero_name=self.id,
                        dict_func=get_rename_skel_dict_func(f"combat_{k}")
                    ))
                if v.death is not None and isinstance(v.death, Animation):
                    res.extend(v.death.copy_and_rename_animation(
                        root_dir=root_dir,
                        anim_name=f"death_{k}",
                        is_fx=False,
                        hero_name=self.id,
                        dict_func=get_rename_skel_dict_func(f"death_{k}")
                    ))
                if v.defend is not None and isinstance(v.defend, Animation):
                    res.extend(v.defend.copy_and_rename_animation(
                        root_dir=root_dir,
                        anim_name=f"defend_{k}",
                        is_fx=False,
                        hero_name=self.id,
                        dict_func=get_rename_skel_dict_func(f"defend_{k}")
                    ))
                if v.heroic is not None and isinstance(v.heroic, Animation):
                    res.extend(v.heroic.copy_and_rename_animation(
                        root_dir=root_dir,
                        anim_name=f"heroic_{k}",
                        is_fx=False,
                        hero_name=self.id,
                        dict_func=get_rename_skel_dict_func(f"heroic_{k}")
                    ))
                if v.idle is not None and isinstance(v.idle, Animation):
                    res.extend(v.idle.copy_and_rename_animation(
                        root_dir=root_dir,
                        anim_name=f"idle_{k}",
                        is_fx=False,
                        hero_name=self.id,
                        dict_func=get_rename_skel_dict_func(f"idle_{k}")
                    ))
                if v.investigate is not None and isinstance(v.investigate, Animation):
                    res.extend(v.investigate.copy_and_rename_animation(
                        root_dir=root_dir,
                        anim_name=f"investigate_{k}",
                        is_fx=False,
                        hero_name=self.id,
                        dict_func=get_rename_skel_dict_func(f"investigate_{k}")
                    ))
                if v.riposte is not None and isinstance(v.riposte, Animation):
                    res.extend(v.riposte.copy_and_rename_animation(
                        root_dir=root_dir,
                        anim_name=f"riposte_{k}",
                        is_fx=False,
                        hero_name=self.id,
                        dict_func=get_rename_skel_dict_func(f"riposte_{k}")
                    ))
                if v.walk is not None and isinstance(v.walk, Animation):
                    res.extend(v.walk.copy_and_rename_animation(
                        root_dir=root_dir,
                        anim_name=f"walk_{k}",
                        is_fx=False,
                        hero_name=self.id,
                        dict_func=get_rename_skel_dict_func(f"walk_{k}")
                    ))

        return tuple(res)

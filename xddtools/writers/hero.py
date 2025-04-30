import json
import os
from typing import List, Optional

from xddtools.base import BaseWriter, Entry, HeroEntry, get_entry_id
from xddtools.entries.actor_dot import ActorDot
from xddtools.entries.animation import Animation
from xddtools.entries.bank import Bank
from xddtools.entries.colour import Colour
from xddtools.entries.effect import Effect
from xddtools.entries.hero import Hero, Mode
from xddtools.entries.localization import Localization
from xddtools.entries.skill import Skill, SkillInfo
from xddtools.enum import BankDir, BankSource, SkillHeadType
from xddtools.path import HERO_SAVE_DIR, HERO_UPGRADE_FILE_EXTENSION, HERO_UPGRADE_SAVE_DIR, \
    EXTRA_STACK_LIMIT_SAVE_DIR, EXTRA_STACK_LIMIT_FILE_EXTENSION, PROVISION_FILE_EXTENSION, PROVISION_SAVE_DIR
from xddtools.utils import write_str_to_file, resize_image


class HeroWriter(BaseWriter):
    def __init__(self, prefix: Optional[str] = None):
        super().__init__(prefix=prefix)

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, HeroEntry)

    def add_entry(self, entry: Hero) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)

        res = []

        # 多模式动画
        modes = entry.get_modes()
        # if len(modes) > 0 and entry.base_mode is not None:
        #     raise ValueError(f"{entry.id()} has base mode {entry.base_mode.id()} "
        #                      f"but also has modes {','.join([m.id() for m in modes])}")
        for mode in modes:  # type: Mode
            if isinstance(mode.battle_complete_sfx, str):
                res.append(Bank(
                    bank_dir=BankDir.NONE,
                    bank_name=f"_{mode.id()}",
                    audio=mode.battle_complete_sfx,
                    source=BankSource.HERO
                ))
            elif isinstance(mode.battle_complete_sfx, Bank):
                res.append(mode.battle_complete_sfx.model_copy(update={
                    "bank_dir": BankDir.NONE,
                    "bank_name": f"_{mode.id()}",
                    "guid": mode.battle_complete_sfx.guid,
                    "audio": mode.battle_complete_sfx.audio,
                    "source": BankSource.HERO
                }))

            if mode.afflicted is not None and isinstance(mode.afflicted, Animation):
                anim = mode.afflicted
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": mode.id(),
                    "is_fx": False,
                    "anim_name": "afflicted"
                }))
            if mode.camp is not None and isinstance(mode.camp, Animation):
                anim = mode.camp
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": mode.id(),
                    "is_fx": False,
                    "anim_name": "camp"
                }))
            if mode.combat is not None and isinstance(mode.combat, Animation):
                anim = mode.combat
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": mode.id(),
                    "is_fx": False,
                    "anim_name": "combat"
                }))
            if mode.heroic is not None and isinstance(mode.heroic, Animation):
                anim = mode.heroic
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": mode.id(),
                    "is_fx": False,
                    "anim_name": "heroic"
                }))
            if mode.idle is not None and isinstance(mode.idle, Animation):
                anim = mode.idle
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": mode.id(),
                    "is_fx": False,
                    "anim_name": "idle"
                }))
            if mode.investigate is not None and isinstance(mode.investigate, Animation):
                anim = mode.investigate
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": mode.id(),
                    "is_fx": False,
                    "anim_name": "investigate"
                }))
            if mode.riposte is not None and isinstance(mode.riposte, Animation):
                anim = mode.riposte
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": mode.id(),
                    "is_fx": False,
                    "anim_name": "riposte"
                }))
            if mode.walk is not None and isinstance(mode.walk, Animation):
                anim = mode.walk
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": mode.id(),
                    "is_fx": False,
                    "anim_name": "walk"
                }))
            if mode.defend is not None and isinstance(mode.defend, Animation):
                anim = mode.defend

                # def get_tem_func(mode_id: str):
                #     def tem_func(d: Dict[str, Any]) -> dict:
                #         tem = {}
                #         if len(d["animations"]) != 2:
                #             raise ValueError("defend animation must have 2 animations,defend and death")
                #         for k, v in d["animations"].items():
                #             if k.startswith("defend"):
                #                 tem[f"defend_{mode_id}"] = v
                #             elif k.startswith("death"):
                #                 tem[f"death_{mode_id}"] = v
                #         if len(tem) != 2:
                #             raise ValueError("defend animation must have 2 animations,defend and death")
                #         # d["animations"] = {
                #         #     f"death_{mode_id}": tem[f"death_{mode_id}"],
                #         #     f"defend_{mode_id}": tem[f"defend_{mode_id}"]
                #         # }
                #         d["animations"] = tem
                #         return d
                #     return tem_func

                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": mode.id(),
                    "is_fx": False,
                    "anim_name": "defend",
                    "need_rename": False
                    # "dict_func": get_tem_func(mode.id()) if anim.dict_func is None else anim.dict_func
                }))

            if mode.actor_mode_name is not None:
                res.append(Localization(
                    entry_id=f"actor_mode_name_{mode.id()}",
                    text=mode.actor_mode_name
                ))
            if mode.str_skill_mode_info is not None:
                res.append(Localization(
                    entry_id=f"str_skill_mode_info_{mode.id()}",
                    text=mode.str_skill_mode_info
                ))

        # 基本模式动画
        mode: Optional[Mode] = entry.base_mode
        if mode is not None:
            if mode.afflicted is not None and isinstance(mode.afflicted, Animation):
                anim = mode.afflicted
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": None,
                    "is_fx": False,
                    "anim_name": "afflicted"
                }))
            if mode.camp is not None and isinstance(mode.camp, Animation):
                anim = mode.camp
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": None,
                    "is_fx": False,
                    "anim_name": "camp"
                }))
            if mode.combat is not None and isinstance(mode.combat, Animation):
                anim = mode.combat
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": None,
                    "is_fx": False,
                    "anim_name": "combat"
                }))
            if mode.heroic is not None and isinstance(mode.heroic, Animation):
                anim = mode.heroic
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": None,
                    "is_fx": False,
                    "anim_name": "heroic"
                }))
            if mode.idle is not None and isinstance(mode.idle, Animation):
                anim = mode.idle
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": None,
                    "is_fx": False,
                    "anim_name": "idle"
                }))
            if mode.investigate is not None and isinstance(mode.investigate, Animation):
                anim = mode.investigate
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": None,
                    "is_fx": False,
                    "anim_name": "investigate"
                }))
            if mode.riposte is not None and isinstance(mode.riposte, Animation):
                anim = mode.riposte
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": None,
                    "is_fx": False,
                    "anim_name": "riposte"
                }))
            if mode.walk is not None and isinstance(mode.walk, Animation):
                anim = mode.walk
                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": None,
                    "is_fx": False,
                    "anim_name": "walk"
                }))
            if mode.defend is not None and isinstance(mode.defend, Animation):
                anim = mode.defend

                # def tem_func(d: Dict[str, Any]) -> dict:
                #     tem = {}
                #     if len(d["animations"]) != 2:
                #         raise ValueError("defend animation must have 2 animations,defend and death")
                #     for k, v in d["animations"].items():
                #         if k.startswith("defend"):
                #             tem[f"defend"] = v
                #         elif k.startswith("death"):
                #             tem[f"death"] = v
                #     if len(tem) != 2:
                #         raise ValueError("defend animation must have 2 animations,defend and death")
                #     d["animations"] = tem
                #     return d

                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": None,
                    "is_fx": False,
                    "anim_name": "defend",
                    "need_rename": False
                    # "dict_func": tem_func if anim.dict_func is None else anim.dict_func
                }))

        # 暴击效果
        for effect in entry.crit_effects:
            if isinstance(effect, Effect):
                if isinstance(effect.actor_dot, ActorDot):
                    if isinstance(effect.actor_dot.fx, Animation):
                        effect.actor_dot.fx.hero_name = entry.id()
                res.append(effect)

        # 生命变化
        if entry.hp_reactions is not None:
            for reaction in entry.hp_reactions:
                for effect in reaction.effects:
                    if isinstance(effect, Effect):
                        if isinstance(effect.actor_dot, ActorDot):
                            if isinstance(effect.actor_dot.fx, Animation):
                                effect.actor_dot.fx.hero_name = entry.id()
                        res.append(effect)

        # 死亡效果
        if entry.death_reactions is not None:
            for reaction in entry.death_reactions:
                for effect in reaction.effects:
                    if isinstance(effect, Effect):
                        if isinstance(effect.actor_dot, ActorDot):
                            if isinstance(effect.actor_dot.fx, Animation):
                                effect.actor_dot.fx.hero_name = entry.id()
                        res.append(effect)

        # 技能
        for skill in entry.skills:  # type: Skill
            # 音效
            bank_modes = set()
            if skill.skill_head_type == SkillHeadType.RIPOSTE_SKILL:
                for mode in modes:
                    bank_modes.add(get_entry_id(mode))
            else:
                if isinstance(skill.skill_info, SkillInfo):
                    skill_info = [skill.skill_info]
                else:
                    skill_info = skill.skill_info
                for item in skill_info:
                    if item.valid_modes_and_effects is not None:
                        for mode_effects in item.valid_modes_and_effects:
                            bank_modes.add(get_entry_id(mode_effects.valid_mode))

            if len(bank_modes) == 0:
                if isinstance(skill.hit_sfx, str):
                    res.append(Bank(
                        bank_name=f"{entry.id()}_{skill.id()}",
                        audio=skill.hit_sfx,
                        source=BankSource.HERO
                    ))
                elif isinstance(skill.hit_sfx, Bank):
                    res.append(skill.hit_sfx.model_copy(update={
                        "bank_dir": BankDir.CHAR_ALLY,
                        "bank_name": f"{entry.id()}_{skill.id()}",
                        "guid": skill.hit_sfx.guid,
                        "audio": skill.hit_sfx.audio,
                        "source": BankSource.HERO
                    }))

                if isinstance(skill.miss_sfx, str):
                    res.append(Bank(
                        bank_name=f"{entry.id()}_{skill.id()}_miss",
                        audio=skill.miss_sfx,
                        source=BankSource.HERO
                    ))
                elif isinstance(skill.miss_sfx, Bank):
                    res.append(skill.miss_sfx.model_copy(update={
                        "bank_dir": BankDir.CHAR_ALLY,
                        "bank_name": f"{entry.id()}_{skill.id()}_miss",
                        "guid": skill.miss_sfx.guid,
                        "audio": skill.miss_sfx.audio,
                        "source": BankSource.HERO
                    }))
            else:
                if isinstance(skill.hit_sfx, str):
                    for idx, item in enumerate(bank_modes):
                        res.append(Bank(
                            bank_name=f"{entry.id()}_{skill.id()}_{item}",
                            audio=skill.hit_sfx if idx == 0 else None,
                            source=BankSource.HERO
                        ))
                elif isinstance(skill.hit_sfx, Bank):
                    for idx, item in enumerate(bank_modes):
                        res.append(skill.hit_sfx.model_copy(update={
                            "bank_dir": BankDir.CHAR_ALLY,
                            "bank_name": f"{entry.id()}_{skill.id()}_{item}",
                            "guid": skill.hit_sfx.guid,
                            "audio": skill.hit_sfx.audio if idx == 0 else None,
                            "source": BankSource.HERO
                        }))

                if isinstance(skill.miss_sfx, str):
                    for idx, item in enumerate(bank_modes):
                        res.append(Bank(
                            bank_name=f"{entry.id()}_{skill.id()}_miss_{item}",
                            audio=skill.miss_sfx if idx == 0 else None,
                            source=BankSource.HERO
                        ))
                elif isinstance(skill.miss_sfx, Bank):
                    for idx, item in enumerate(bank_modes):
                        res.append(skill.miss_sfx.model_copy(update={
                            "bank_dir": BankDir.CHAR_ALLY,
                            "bank_name": f"{entry.id()}_{skill.id()}_miss_{item}",
                            "guid": skill.miss_sfx.guid,
                            "audio": skill.miss_sfx.audio if idx == 0 else None,
                            "source": BankSource.HERO
                        }))

            # 翻译
            if skill.skill_name is not None:
                res.append(Localization(
                    entry_id=f"combat_skill_name_{entry.id()}_{skill.id()}",
                    text=skill.skill_name
                ))
            if skill.upgrade_tree_name is not None:
                res.append(Localization(
                    entry_id=f"upgrade_tree_name_{entry.id()}.{skill.id()}",
                    text=skill.upgrade_tree_name
                ))

            # 动画
            for anim in [skill.anim, skill.custom_target_anim, skill.custom_idle_anim_name]:
                if isinstance(anim, Animation):
                    res.append(anim.model_copy(update={
                        "hero_name": entry.id(),
                        "is_fx": False
                    }))
            # 特效
            for fx in [
                skill.fx, skill.targfx, skill.targheadfx, skill.targchestfx,
                skill.misstargfx, skill.misstargheadfx, skill.misstargchestfx
            ]:
                if isinstance(fx, Animation):
                    res.append(fx.model_copy(update={
                        "hero_name": entry.id(),
                        "is_fx": True
                    }))

            # 技能效果
            if isinstance(skill.skill_info, SkillInfo):
                skill_info = [skill.skill_info]
            else:
                skill_info = skill.skill_info
            for info in skill_info:
                if info.damage_heal_base_class_ids is not None:
                    for item in info.damage_heal_base_class_ids:
                        if isinstance(item, Entry):
                            res.append(item)
                if info.effect_ids is not None:
                    for item in info.effect_ids:
                        if isinstance(item, Effect):
                            if isinstance(item.actor_dot, ActorDot):
                                if isinstance(item.actor_dot.fx, Animation):
                                    item.actor_dot.fx.hero_name = entry.id()
                            res.append(item)
                if info.valid_modes_and_effects is not None:
                    for mode_effects in info.valid_modes_and_effects:
                        if mode_effects.effects is not None:
                            for item in mode_effects.effects:
                                if isinstance(item, Effect):
                                    if isinstance(item.actor_dot, ActorDot):
                                        if isinstance(item.actor_dot.fx, Animation):
                                            item.actor_dot.fx.hero_name = entry.id()
                                    res.append(item)

        # 过压修改
        if entry.overstressed_modifier is not None:
            for modify in entry.overstressed_modifier:
                if isinstance(modify.trait_id, Entry):
                    res.append(modify.trait_id)

        # 死门减益
        if entry.deaths_door_buffs is not None:
            for buff in entry.deaths_door_buffs:
                if isinstance(buff, Entry):
                    res.append(buff)
        if entry.recovery_buffs is not None:
            for buff in entry.recovery_buffs:
                if isinstance(buff, Entry):
                    res.append(buff)
        if entry.recovery_heart_attack_buffs is not None:
            for buff in entry.recovery_heart_attack_buffs:
                if isinstance(buff, Entry):
                    res.append(buff)

        # 冲突怪癖
        if entry.quirk_modifier is not None:
            for modify in entry.quirk_modifier:
                if isinstance(modify, Entry):
                    res.append(modify)

        # 额外掉落
        if entry.extra_battle_loot is not None:
            if isinstance(entry.extra_battle_loot.code, Entry):
                res.append(entry.extra_battle_loot.code)
        if entry.extra_curio_loot is not None:
            if isinstance(entry.extra_curio_loot.code, Entry):
                res.append(entry.extra_curio_loot.code)

        if entry.extra_stack_limit is not None:
            for item in entry.extra_stack_limit:
                if isinstance(item.item_id, Entry):
                    res.append(item.item_id)

        # 演出动画
        if entry.actout_display is not None:
            actout = entry.actout_display
            if isinstance(actout.attack_friendly_sfx, Entry):
                res.append(actout.attack_friendly_sfx)

            if actout.attack_friendly_anim is not None:
                if isinstance(actout.attack_friendly_anim, Animation):
                    res.append(actout.attack_friendly_anim.model_copy(update={
                        "hero_name": entry.id(),
                        "is_fx": False
                    }))
            if actout.attack_friendly_fx is not None:
                if isinstance(actout.attack_friendly_fx, Animation):
                    res.append(actout.attack_friendly_fx.model_copy(update={
                        "hero_name": entry.id(),
                        "is_fx": True
                    }))
            if actout.attack_friendly_targchestfx is not None:
                if isinstance(actout.attack_friendly_targchestfx, Animation):
                    res.append(actout.attack_friendly_targchestfx.model_copy(update={
                        "hero_name": entry.id(),
                        "is_fx": True
                    }))

        # 马车生成
        if entry.generation is not None:
            generation = entry.generation
            if isinstance(generation.town_event_dependency, Entry):
                res.append(generation.town_event_dependency)
            if isinstance(generation.reduce_number_of_cards_in_deck_hero_class_id, Entry):
                res.append(generation.reduce_number_of_cards_in_deck_hero_class_id)

        # 翻译
        if entry.hero_localization is not None:
            for item in entry.hero_localization.get_localization_entries(entry.id()):
                res.append(Localization(
                    entry_id=item[0],
                    text=item[1]
                ))

        # 血条颜色
        if entry.health_bar is not None:
            res.extend([
                Colour(entry_id=f"tray_health_bar_{entry.id()}_damage_bottom", rgba=entry.health_bar.damage_bottom),
                Colour(entry_id=f"tray_health_bar_{entry.id()}_damage_top", rgba=entry.health_bar.damage_top),
                Colour(entry_id=f"tray_health_bar_{entry.id()}_heal_bottom", rgba=entry.health_bar.heal_bottom),
                Colour(entry_id=f"tray_health_bar_{entry.id()}_heal_top", rgba=entry.health_bar.heal_top),
                Colour(entry_id=f"tray_health_bar_{entry.id()}_current_bottom", rgba=entry.health_bar.current_bottom),
                Colour(entry_id=f"tray_health_bar_{entry.id()}_current_top", rgba=entry.health_bar.current_top),
            ])

        # 商店自带物品
        if entry.raid_starting_hero_items is not None:
            for hero_item in entry.raid_starting_hero_items:
                if isinstance(hero_item.item_id, Entry):
                    res.append(hero_item.item_id)

        return res

    def _export_one_hero(self, hero: Hero, root_dir: str) -> List[str]:
        hero_dir = os.path.join(root_dir, HERO_SAVE_DIR, hero.id())
        res = []

        # 导出info文件
        file = os.path.join(hero_dir, f'{hero.id()}.info.darkest')
        res.append(write_str_to_file(
            file_path=file,
            content=hero.info()
        ))

        # 导出art文件
        file = os.path.join(hero_dir, f'{hero.id()}.art.darkest')
        res.append(write_str_to_file(
            file_path=file,
            content=hero.art()
        ))

        # 导出升级文件
        file = os.path.join(root_dir, HERO_UPGRADE_SAVE_DIR, f"{hero.id()}{HERO_UPGRADE_FILE_EXTENSION}")
        res.append(write_str_to_file(
            file_path=file,
            content=json.dumps(hero.get_upgrade_dict(), indent=2, ensure_ascii=True)
        ))

        # 导出额外物品上限
        if hero.extra_stack_limit is not None:
            content = []
            for limit in hero.extra_stack_limit:
                content.append(limit.info(hero.id()))
            file = os.path.join(EXTRA_STACK_LIMIT_SAVE_DIR, f"{hero.id()}{EXTRA_STACK_LIMIT_FILE_EXTENSION}")
            res.append(write_str_to_file(
                file_path=file,
                content="\n".join(content)
            ))

        # 导出商店界面自动补给品
        if hero.raid_starting_hero_items is not None:
            tem = []
            for hero_item in hero.raid_starting_hero_items:
                tem.append(hero_item.get_dict())
            tem = {"raid_starting_hero_class_item_lists": [{"hero_class": hero.id(), "item_lists": tem}]}
            file = os.path.join(PROVISION_SAVE_DIR, f"hero_{hero.id()}{PROVISION_FILE_EXTENSION}")
            res.append(write_str_to_file(
                file_path=file,
                content=json.dumps(tem, indent=2, ensure_ascii=True)
            ))

        # 导出weapon和armour图片
        if hero.weapon_images is not None:
            for i in range(len(hero.weapon_images)):
                file = os.path.join(hero_dir, "icons_equip", f"eqp_weapon_{i}.png")
                res.append(resize_image(
                    input_path=hero.weapon_images[i],
                    output_path=file
                ))
        if hero.armour_images is not None:
            for i in range(len(hero.armour_images)):
                file = os.path.join(hero_dir, "icons_equip", f"eqp_armour_{i}.png")
                res.append(resize_image(
                    input_path=hero.armour_images[i],
                    output_path=file
                ))

        # 导出升级背景图
        if hero.guild_header_image_path is not None:
            file = os.path.join(hero_dir, f'{hero.id()}_guild_header.png')
            res.append(resize_image(
                input_path=hero.guild_header_image_path,
                output_path=file,
                size=(715, 630)
            ))

        # 导出头像图片
        if hero.portrait_roster_image_path is not None:
            file = os.path.join(hero_dir, f'{hero.id()}_A', f'{hero.id()}_portrait_roster.png')
            res.append(resize_image(
                input_path=hero.portrait_roster_image_path,
                output_path=file,
                size=(85, 85)
            ))

        # 导出技能图标
        for skill in hero.skills:  # type: Skill
            if skill.icon_image is not None and skill.icon is not None:
                file = os.path.join(hero_dir, f'{hero.id()}.ability.{skill.icon}.png')
                res.append(resize_image(
                    input_path=skill.icon_image,
                    output_path=file,
                    size=(72, 72)
                ))

        return res

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        if root_dir is None:
            root_dir = "./"
        res = []

        for hero in self._entries:  # type: Hero
            res.extend(self._export_one_hero(hero, root_dir))

        return res

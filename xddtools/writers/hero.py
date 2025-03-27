import json
import os
from typing import List, Any, Dict, Optional

from xddtools.base import BaseWriter, Entry, HeroEntry
from xddtools.entries.bank import Bank
from xddtools.entries.animation import Animation
from xddtools.entries.hero import Hero, Mode
from xddtools.entries.localization import Localization
from xddtools.entries.skill import Skill, SkillInfo
from xddtools.enum import BankDir, BankSource
from xddtools.path import HERO_SAVE_DIR, HERO_UPGRADE_FILE_EXTENSION, HERO_UPGRADE_SAVE_DIR, EXTRA_STACK_LIMIT_SAVE_DIR, \
    EXTRA_STACK_LIMIT_FILE_EXTENSION
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
        if len(modes) > 0 and entry.base_mode is not None:
            raise ValueError(f"{entry.id()} has base mode {entry.base_mode.id()} "
                             f"but also has modes {','.join([m.id() for m in modes])}")
        for mode in modes:  # type: Mode
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

                def tem_func(d: Dict[str, Any]) -> dict:
                    tem = {}
                    if len(d) != 2:
                        raise ValueError("defend animation must have 2 animations,defend and death")
                    for k, v in d.items():
                        if k.startswith("defend"):
                            tem[f"defend_{mode.id()}"] = v
                        elif k.startswith("death"):
                            tem[f"death_{mode.id()}"] = v
                    if len(tem) != 2:
                        raise ValueError("defend animation must have 2 animations,defend and death")
                    return tem

                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": mode.id(),
                    "is_fx": False,
                    "anim_name": "defend",
                    "dict_func": tem_func if anim.dict_func is None else anim.dict_func
                }))

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

                def tem_func(d: Dict[str, Any]) -> dict:
                    tem = {}
                    if len(d["animations"]) != 2:
                        raise ValueError("defend animation must have 2 animations,defend and death")
                    for k, v in d["animations"].items():
                        if k.startswith("defend"):
                            tem[f"defend"] = v
                        elif k.startswith("death"):
                            tem[f"death"] = v
                    if len(tem) != 2:
                        raise ValueError("defend animation must have 2 animations,defend and death")
                    d["animations"] = tem
                    return d

                res.append(anim.model_copy(update={
                    "hero_name": entry.id(),
                    "mode_name": None,
                    "is_fx": False,
                    "anim_name": "defend",
                    "dict_func": tem_func if anim.dict_func is None else anim.dict_func
                }))

        # 暴击效果
        for effect in entry.crit_effects:
            if isinstance(effect, Entry):
                res.append(effect)

        # 技能
        for skill in entry.skills:  # type: Skill
            # 音效
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
                        if isinstance(item, Entry):
                            res.append(item)
                if info.valid_modes_and_effects is not None:
                    for mode_effects in info.valid_modes_and_effects:
                        if mode_effects.effect_ids is not None:
                            for item in mode_effects.effect_ids:
                                if isinstance(item, Entry):
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

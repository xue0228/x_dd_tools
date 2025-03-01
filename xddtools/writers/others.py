import json
import os
from typing import Tuple, Optional, Iterable, Dict, List

from xddtools.base import BaseWriter, BaseJsonData, LocalizationWriter
from xddtools.buffs import Buff
from xddtools.camping_skills import CampingSkill
from xddtools.colour import Colour, bleed, stress, heal_hp, blight
from xddtools.effects import Effect
from xddtools.enums import ItemType, CampingSkillEffectType
from xddtools.items import Item
from xddtools.loot import LootTable, LootItemEntry
from xddtools.path import BUFF_SAVE_DIR, BUFF_FILE_EXTENSION, \
    EFFECT_SAVE_DIR, EFFECT_FILE_EXTENSION, COLOUR_SAVE_DIR, COLOUR_FILE_EXTENSION, ITEM_SAVE_DIR, \
    ITEM_FILE_EXTENSION, QUIRK_LIBRARY_FILE_EXTENSION, QUIRK_SAVE_DIR, QUIRK_ACTOUT_FILE_EXTENSION, \
    LOOT_TABLE_SAVE_DIR, LOOT_TABLE_FILE_EXTENSION, CAMPING_SKILL_SAVE_DIR, CAMPING_SKILL_FILE_EXTENSION
from xddtools.quirks import Quirk
from xddtools.utils import make_dirs


class ColourWriter(BaseWriter):
    def __init__(
            self,
            name: str,
            colours: Optional[Iterable[Colour]] = None,
    ):
        super().__init__(
            name=name,
            items=colours,
            relative_save_dir=COLOUR_SAVE_DIR,
            extension=COLOUR_FILE_EXTENSION
        )

    def __str__(self) -> str:
        return "".join([str(colour) for colour in self._items]) + "\n"


class BuffWriter(BaseJsonData, BaseWriter):
    def __init__(
            self,
            name: str,
            buffs: Optional[Iterable[Buff]] = None,
            localization_writer: Optional[LocalizationWriter] = None
    ):
        super().__init__(
            name=name,
            items=buffs,
            relative_save_dir=BUFF_SAVE_DIR,
            extension=BUFF_FILE_EXTENSION,
            localization_writer=localization_writer
        )

    def add_item(
            self,
            item: Buff
    ):
        item_id = super().add_item(item)
        if self._localization_writer is not None:
            self._localization_writer.add_entries(item.buff_rule.entries)
        return item_id

    def dict(self) -> dict:
        return {"buffs": [buff.dict() for buff in self._items]}


class EffectWriter(BaseWriter):
    def __init__(
            self,
            name: str,
            effects: Optional[Iterable[Effect]] = None,
            buff_writer: Optional[BuffWriter] = None
    ):
        self.buff_writer = buff_writer
        super().__init__(
            name=name,
            items=effects,
            relative_save_dir=EFFECT_SAVE_DIR,
            extension=EFFECT_FILE_EXTENSION
        )

    def add_item(
            self,
            item: Effect
    ):
        if self.buff_writer is not None and item.buff_ids is not None:
            for buff in item.buff_ids:
                if isinstance(buff, Buff):
                    self.buff_writer.add_item(buff)
        return super().add_item(item)

    def __str__(self):
        return "".join([str(effect) for effect in self._items]) + "\n"


class ItemWriter(BaseWriter):
    def __init__(
            self,
            name: str,
            items: Optional[Iterable[Item]] = None,
            effect_writer: Optional[EffectWriter] = None,
            localization_writer: Optional[LocalizationWriter] = None
    ):
        self.effect_writer = effect_writer
        super().__init__(
            name=name,
            items=items,
            relative_save_dir=ITEM_SAVE_DIR,
            extension=ITEM_FILE_EXTENSION,
            localization_writer=localization_writer
        )

    def add_item(
            self,
            item: Item
    ):
        if self.effect_writer is not None and item.effect is not None:
            self.effect_writer.add_item(item.effect)
        return super().add_item(item)

    def __str__(self):
        return "".join([str(item) for item in self._items]) + "\n"

    def _classification_dict(self) -> Dict[ItemType, List[Item]]:
        res = {}
        for item in self._items:
            if item.item_type not in res:
                res[item.item_type] = []
            res[item.item_type].append(item)
        return res

    def export(self, root_dir: Optional[str] = None) -> Tuple[str, ...]:
        if root_dir is None:
            root_dir = "./"

        for item in self._items:
            if item.image_path is not None:
                item.export_image(root_dir)

        res = []
        for k, v in self._classification_dict().items():
            file = os.path.join(root_dir, self._relative_save_dir, f"{self.id}.{k.value}{self._extension}")
            make_dirs(os.path.dirname(file))
            with open(file, 'w', encoding='utf-8') as f:
                tem = "".join([str(item) for item in v]) + "\n"
                f.write(tem)
            res.append(os.path.normpath(file))
        return tuple(res)


class QuirkWriter(BaseJsonData, BaseWriter):
    def __init__(
            self,
            name: str,
            quirks: Optional[Iterable[Quirk]] = None,
            buff_writer: Optional[BuffWriter] = None,
            effect_writer: Optional[EffectWriter] = None,
            item_writer: Optional[ItemWriter] = None,
            localization_writer: Optional[LocalizationWriter] = None
    ):
        self.buff_writer = buff_writer
        self.effect_writer = effect_writer
        self.item_writer = item_writer
        super().__init__(
            name=name,
            items=quirks,
            relative_save_dir=QUIRK_SAVE_DIR,
            extension=QUIRK_LIBRARY_FILE_EXTENSION,
            localization_writer=localization_writer
        )

    def add_item(
            self,
            item: Quirk
    ):
        if self.buff_writer is not None and item.buffs is not None:
            for buff in item.buffs:
                if isinstance(buff, Buff):
                    self.buff_writer.add_item(buff)

        if item.use_item_changes is not None:
            for use_item_change in item.use_item_changes:
                if self.item_writer is not None and isinstance(use_item_change.item_id, Item):
                    self.item_writer.add_item(use_item_change.item_id)
                # if isinstance(use_item_change.change_quirk_class_id, Quirk):
                #     self.add_item(use_item_change.change_quirk_class_id)

        if item.use_item_dungeon_effects is not None:
            for use_item_dungeon_effect in item.use_item_dungeon_effects:
                if self.item_writer is not None and isinstance(use_item_dungeon_effect.item_id, Item):
                    self.item_writer.add_item(use_item_dungeon_effect.item_id)
                if self.effect_writer is not None and isinstance(use_item_dungeon_effect.effect, Effect):
                    self.effect_writer.add_item(use_item_dungeon_effect.effect)

        if self.effect_writer is not None and item.combat_start_turn_act_outs is not None:
            for act_out in item.combat_start_turn_act_outs:
                if isinstance(act_out.string_value, Effect):
                    self.effect_writer.add_item(act_out.string_value)
        if self.effect_writer is not None and item.reaction_act_outs is not None:
            for act_out in item.reaction_act_outs:
                if isinstance(act_out.effect, Effect):
                    self.effect_writer.add_item(act_out.effect)

        # if item.incompatible_quirks is not None:
        #     for quirk in item.incompatible_quirks:
        #         if isinstance(quirk, Quirk):
        #             self.add_item(quirk)
        #
        # if item.evolution_class_id is not None and isinstance(item.evolution_class_id, Quirk):
        #     self.add_item(item.evolution_class_id)
        #
        # if item.contagious_class_id is not None and isinstance(item.contagious_class_id, Quirk):
        #     self.add_item(item.contagious_class_id)

        return super().add_item(item)

    def dict(self) -> dict:
        quirks = []
        act_outs = []
        for quirk in self._items:
            quirk = quirk.dict()
            tem = {
                "quirk_id": quirk["id"]
            }
            combat_start_turn_act_out = quirk.pop("combat_start_turn_act_outs", None)
            if combat_start_turn_act_out is not None:
                tem["combat_start_turn_act_outs"] = combat_start_turn_act_out
            reaction_act_out = quirk.pop("reaction_act_outs", None)
            if reaction_act_out is not None:
                tem["reaction_act_outs"] = reaction_act_out
            if len(tem) > 1:
                act_outs.append(tem)
            quirks.append(quirk)

        return {
            "quirks": quirks,
            "quirk_act_outs": act_outs,
        }

    def export(self, root_dir: Optional[str] = None) -> Tuple[str, ...]:
        if root_dir is None:
            root_dir = "./"

        for item in self._items:
            if item.image_path is not None:
                item.export_image(root_dir)

        tem = self.dict()
        quirks = {"quirks": tem["quirks"]}
        act_outs = {"quirk_act_outs": tem["quirk_act_outs"]}

        res = []

        file = os.path.join(root_dir, self._relative_save_dir, f"{self.id}{self._extension}")
        make_dirs(os.path.dirname(file))
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(quirks, f, indent=2, ensure_ascii=True)
        res.append(os.path.normpath(file))

        file = os.path.join(root_dir, self._relative_save_dir, f"{self.id}{QUIRK_ACTOUT_FILE_EXTENSION}")
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(act_outs, f, indent=2, ensure_ascii=True)
        res.append(os.path.normpath(file))

        return tuple(res)


class LootTableWriter(BaseJsonData, BaseWriter):
    def __init__(
            self,
            name: str,
            loot_tables: Optional[Iterable[LootTable]] = None,
            item_writer: Optional[ItemWriter] = None,
    ):
        self.item_writer = item_writer
        super().__init__(
            name=name,
            items=loot_tables,
            relative_save_dir=LOOT_TABLE_SAVE_DIR,
            extension=LOOT_TABLE_FILE_EXTENSION,
        )

    def add_item(
            self,
            item: LootTable
    ):
        if self.item_writer is not None:
            for loot in item.loot_entries:
                if isinstance(loot, LootItemEntry) and isinstance(loot.item_id, Item):
                    self.item_writer.add_item(loot.item_id)
        return super().add_item(item)

    def dict(self) -> dict:
        return {"loot_tables": [table.dict() for table in self._items]}


class CampingSkillWriter(BaseJsonData, BaseWriter):
    def __init__(
            self,
            name: str,
            class_specific_number_of_classes_threshold: int = 4,
            camping_skills: Optional[Iterable[CampingSkill]] = None,
            table_writer: Optional[LootTableWriter] = None,
            localization_writer: Optional[LocalizationWriter] = None,
    ):
        self._class_specific_number_of_classes_threshold = class_specific_number_of_classes_threshold
        self._table_writer = table_writer
        self._localization_writer = localization_writer
        super().__init__(
            name=name,
            items=camping_skills,
            relative_save_dir=CAMPING_SKILL_SAVE_DIR,
            extension=CAMPING_SKILL_FILE_EXTENSION,
            localization_writer=localization_writer,
        )

    def add_item(
            self,
            item: CampingSkill
    ):
        if self._table_writer is not None:
            for effect in item.effects:
                if effect.effect_type == CampingSkillEffectType.LOOT and isinstance(effect.sub_type, LootTable):
                    self._table_writer.add_item(effect.sub_type)
        return super().add_item(item)

    def dict(self) -> dict:
        return {
            "configuration": {
                "class_specific_number_of_classes_threshold": self._class_specific_number_of_classes_threshold
            },
            "skills": [skill.dict() for skill in self._items]
        }

    def export(self, root_dir: Optional[str] = None) -> Tuple[str, ...]:
        res = []
        for item in self._items:
            if item.image_path is not None:
                res.append(
                    item.export_image(root_dir)
                )
        res.append(super().export(root_dir))
        return tuple(res)


def get_base_colour_writer(
        name: str,
        colours: Optional[Iterable[Colour]] = None,
):
    res = ColourWriter(name, colours)
    res.add_items((bleed, blight, stress, heal_hp))
    return res

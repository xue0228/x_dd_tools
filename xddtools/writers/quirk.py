import json
import os.path
from typing import List, Optional

from xddtools.base import JsonData, BaseWriter, Entry, QuirkEntry
from xddtools.entries import Localization
from xddtools.entries.quirk import Quirk, get_quirk_transition_a_to_b_localization_entries
from xddtools.path import QUIRK_SAVE_DIR, QUIRK_LIBRARY_FILE_EXTENSION, QUIRK_IMAGE_SAVE_DIR, \
    QUIRK_ACTOUT_FILE_EXTENSION
from xddtools.utils import resize_image_keep_ratio, write_str_to_file


class QuirkWriter(JsonData, BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=QUIRK_SAVE_DIR,
            extension=QUIRK_LIBRARY_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, QuirkEntry)

    def add_entry(self, entry: Quirk) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)

        res = []

        if isinstance(entry.evolution_class_id, Entry):
            res.append(entry.evolution_class_id)
        if isinstance(entry.contagious_class_id, Entry):
            res.append(entry.contagious_class_id)

        if entry.incompatible_quirks is not None:
            for quirk in entry.incompatible_quirks:
                if isinstance(quirk, Entry):
                    res.append(quirk)
        if entry.buffs is not None:
            for buff in entry.buffs:
                if isinstance(buff, Entry):
                    res.append(buff)
        if entry.combat_start_turn_act_outs is not None:
            for act_out in entry.combat_start_turn_act_outs:
                for entry_id, bark in act_out.get_localization_entries(entry.id()):
                    res.append(Localization(
                        entry_id=entry_id,
                        text=bark
                    ))
                if isinstance(act_out.string_value, Entry):
                    res.append(act_out.string_value)
                if act_out.valid_hero_class_ids is not None:
                    for hero in act_out.valid_hero_class_ids:
                        if isinstance(hero, Entry):
                            res.append(hero)
        if entry.reaction_act_outs is not None:
            for act_out in entry.reaction_act_outs:
                for entry_id, bark in act_out.get_localization_entries(entry.id()):
                    res.append(Localization(
                        entry_id=entry_id,
                        text=bark
                    ))
                if isinstance(act_out.effect, Entry):
                    res.append(act_out.effect)
        if entry.use_item_dungeon_effects is not None:
            for item in entry.use_item_dungeon_effects:
                if isinstance(item.effect, Entry):
                    res.append(item.effect)
                if isinstance(item.item_id, Entry):
                    res.append(item.item_id)

        if entry.use_item_changes is not None:
            for change in entry.use_item_changes:
                if isinstance(change.item_id, Entry):
                    res.append(change.item_id)
                if isinstance(change.change_quirk_class_id, Entry):
                    res.append(change.change_quirk_class_id)
                if change.change_quirk_bark is not None:
                    res.extend(get_quirk_transition_a_to_b_localization_entries(
                        entry.id(),
                        change.change_quirk_class_id,
                        change.change_quirk_bark
                    ))

        if entry.evolution_quirk_bark is not None:
            if entry.evolution_class_id is None:
                raise ValueError("evolution_quirk_bark is not None,but evolution_class_id is None")
            res.extend(get_quirk_transition_a_to_b_localization_entries(
                entry.id(),
                entry.evolution_class_id,
                entry.evolution_quirk_bark
            ))

        if entry.str_quirk_name is not None:
            entry_id = f"str_quirk_name_{entry.id()}"
            res.append(Localization(
                entry_id=entry_id,
                text=entry.str_quirk_name,
            ))
        if entry.str_quirk_description is not None:
            entry_id = f"str_quirk_description_{entry.id()}"
            res.append(Localization(
                entry_id=entry_id,
                text=entry.str_quirk_description,
            ))
        if entry.str_ui_entering is not None:
            entry_id = f"str_ui_entering_{entry.id()}"
            res.append(Localization(
                entry_id=entry_id,
                text=entry.str_ui_entering,
            ))
        if entry.str_trigger_curio is not None:
            if isinstance(entry.str_trigger_curio, str):
                barks = [entry.str_trigger_curio]
            else:
                barks = entry.str_trigger_curio
            for bark in barks:
                entry_id = f"trigger_curio_quirk_{entry.id()}"
                res.append(Localization(
                    entry_id=entry_id,
                    text=bark,
                ))

        return res

    def get_dict(self) -> dict:
        quirks = []
        act_outs = []
        for entry in self._entries:  # type: Quirk
            quirk = entry.get_dict()
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

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        if root_dir is None:
            root_dir = "./"

        res = []
        for quirk in self._entries:  # type: Quirk
            if quirk.tray_quirk_image is not None:
                file = os.path.join(
                    root_dir,
                    QUIRK_IMAGE_SAVE_DIR,
                    f"tray_quirk.{quirk.id()}.png"
                )
                res.append(resize_image_keep_ratio(quirk.tray_quirk_image, file, (24, 24)))

        tem = self.get_dict()
        quirks = {"quirks": tem["quirks"]}
        act_outs = {"quirk_act_outs": tem["quirk_act_outs"]}

        res = []

        file = os.path.join(root_dir, self._relative_save_dir, f"{self.prefix}{self._extension}")
        res.append(write_str_to_file(
            file,
            json.dumps(quirks, indent=2, ensure_ascii=True)
        ))

        file = os.path.join(root_dir, self._relative_save_dir, f"{self.prefix}{QUIRK_ACTOUT_FILE_EXTENSION}")
        res.append(write_str_to_file(
            file,
            json.dumps(act_outs, indent=2, ensure_ascii=True)
        ))

        return res

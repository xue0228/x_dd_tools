from typing import List

from xddtools.base import JsonData, BaseWriter, Entry, TraitEntry
from xddtools.entries import Localization
from xddtools.entries.trait import Trait
from xddtools.path import TRAIT_SAVE_DIR, TRAIT_FILE_EXTENSION


class TraitWriter(JsonData, BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=TRAIT_SAVE_DIR,
            extension=TRAIT_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, TraitEntry)

    def add_entry(self, entry: Trait) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)

        res = []

        if entry.buff_ids is not None:
            for buff in entry.buff_ids:
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

        overstress = "virtue" if entry.is_virtue else "affliction"
        overstress_bark = "virtued" if entry.is_virtue else "afflicted"
        if entry.str_trait_name is not None:
            entry_id = f"str_{overstress}_name_{entry.id()}"
            res.append(Localization(
                entry_id=entry_id,
                text=entry.str_trait_name,
            ))
        if entry.str_trait_description is not None:
            entry_id = f"str_{overstress}_description_{entry.id()}"
            res.append(Localization(
                entry_id=entry_id,
                text=entry.str_trait_description,
            ))
        if entry.str_trait_barks is not None:
            if isinstance(entry.str_trait_barks, str):
                barks = [entry.str_trait_barks]
            else:
                barks = entry.str_trait_barks
            for bark in barks:
                entry_id = f"str_{overstress_bark}_{entry.id()}"
                res.append(Localization(
                    entry_id=entry_id,
                    text=bark,
                ))

        return res

    def get_dict(self) -> dict:
        tem = []
        for trait in self._entries:  # type: Trait
            tem.append(trait.get_dict())
        return {"traits": tem}

from typing import List

from xddtools.base import JsonData, BaseWriter, Entry, PartyNameEntry
from xddtools.entries.localization import Localization
from xddtools.entries.party_name import PartyName
from xddtools.path import PARTY_NAME_FILE_EXTENSION, PARTY_NAME_SAVE_DIR


class PartyNameWriter(JsonData, BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=PARTY_NAME_SAVE_DIR,
            extension=PARTY_NAME_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, PartyNameEntry)

    def add_entry(self, entry: PartyName) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)
        res = []

        for hero in entry.required_hero_class:
            if isinstance(hero, Entry):
                res.append(hero)

        if entry.party_name is not None:
            res.append(Localization(
                entry_id=f"party_name_{entry.id()}",
                text=entry.party_name
            ))

        return res

    def get_dict(self) -> dict:
        tem = []
        for item in self._entries:  # type: PartyName
            tem.append(item.get_dict())
        return {"party_names": tem}

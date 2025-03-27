from typing import List

from xddtools.base import JsonData, BaseWriter, Entry, LootTableEntry
from xddtools.entries.loot import LootTable
from xddtools.path import LOOT_TABLE_SAVE_DIR, LOOT_TABLE_FILE_EXTENSION


class LootTableWriter(JsonData, BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=LOOT_TABLE_SAVE_DIR,
            extension=LOOT_TABLE_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, LootTableEntry)

    def add_entry(self, entry: LootTable) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)

        res = []

        if entry.loot_entries is not None:
            for loot in entry.loot_entries:
                if isinstance(loot.item_id, Entry):
                    res.append(loot.item_id)
                if isinstance(loot.loot_table_id, Entry):
                    res.append(loot.loot_table_id)
                if isinstance(loot.trinket_rarity, Entry):
                    res.append(loot.trinket_rarity)

        return res

    def get_dict(self) -> dict:
        tem = []
        for trait in self._entries:  # type: LootTable
            tem.append(trait.get_dict())
        return {"loot_tables": tem}


def get_common_overrides_loot_table_writer() -> LootTableWriter:
    return LootTableWriter(prefix="common_overrides")

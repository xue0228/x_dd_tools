from typing import Union, Iterable, Optional, Tuple

from xddtools.base import BaseJsonData, BaseID
from xddtools.enums import LootType, ItemType, DungeonID, ItemID
from xddtools.items import Item


class BaseLootEntry(BaseJsonData):
    def __init__(
            self,
            loot_type: LootType,
            chances: int,
            data: dict
    ):
        self._loot_type = loot_type
        self._chances = chances
        self._data = data

    def dict(self) -> dict:
        return {
            "type": self._loot_type.value,
            "chances": self._chances,
            "data": self._data
        }


class LootTable(BaseID, BaseJsonData):
    def __init__(
            self,
            name: str,
            loot_entries: Optional[Iterable[BaseLootEntry]],
            difficulty: int = 0,
            dungeon: Union[DungeonID, str] = ""
    ):
        if difficulty < 0:
            raise ValueError("difficulty must be >= 0,normally should be 1,3,5 or 6")
        super().__init__(name)
        self._difficulty = difficulty
        self._dungeon = dungeon.value if isinstance(dungeon, DungeonID) else dungeon
        self._loot_entries = []
        if loot_entries is not None:
            for loot_entry in loot_entries:
                self._loot_entries.append(loot_entry)

    def add_loot_entry(self, loot_entry: BaseLootEntry):
        self._loot_entries.append(loot_entry)

    @property
    def loot_entries(self):
        return self._loot_entries

    def dict(self) -> dict:
        return {
            "id": self.id,
            "difficulty": self._difficulty,
            "dungeon": self._dungeon,
            "entries": [loot_entry.dict() for loot_entry in self._loot_entries]
        }


class LootNothingEntry(BaseLootEntry):
    def __init__(self, chances: int):
        super().__init__(LootType.NOTHING, chances, {})


class LootItemEntry(BaseLootEntry):
    def __init__(
            self,
            chances: int,
            item_type: ItemType,
            item_id: Union[Item, ItemID, str],
            amount: int
    ):
        if isinstance(item_id, ItemID):
            item_id = item_id.value
        self.item_id = item_id
        super().__init__(
            loot_type=LootType.ITEM,
            chances=chances,
            data={
                "type": item_type.value,
                "id": item_id.id if isinstance(item_id, Item) else item_id,
                "amount": amount
            }
        )


class LootJournalPageEntry(BaseLootEntry):
    def __init__(
            self,
            chances: int,
            min_page_index: int = 1,
            max_page_index: int = 21,
    ):
        super().__init__(
            loot_type=LootType.JOURNAL_PAGE,
            chances=chances,
            data={
                "min_page_index": min_page_index,
                "max_page_index": max_page_index
            }
        )


class LootTableEntry(BaseLootEntry):
    def __init__(
            self,
            chances: int,
            loot_table_id: Union[LootTable, str]
    ):
        loot_table_id = loot_table_id.id if isinstance(loot_table_id, LootTable) else loot_table_id
        super().__init__(
            loot_type=LootType.TABLE,
            chances=chances,
            data={
                "table": loot_table_id
            }
        )


def generate_common_overrides_loot_tables() -> Tuple[LootTable, LootTable, LootTable]:
    return LootTable(
        name="A",
        loot_entries=(
            LootNothingEntry(chances=0),
            LootTableEntry(chances=50, loot_table_id="C"),
            LootTableEntry(chances=38, loot_table_id="G"),
            LootTableEntry(chances=48, loot_table_id="H"),
            LootTableEntry(chances=0, loot_table_id="J"),
            LootTableEntry(chances=0, loot_table_id="P"),
            LootTableEntry(chances=28, loot_table_id="S"),
            LootTableEntry(chances=8, loot_table_id="T"),
            LootJournalPageEntry(chances=2, min_page_index=1, max_page_index=21),
            LootTableEntry(chances=4, loot_table_id="BLOOD_ALWAYS"),
        )
    ), LootTable(
        name="S",
        loot_entries=(
            LootNothingEntry(chances=0),
            LootItemEntry(chances=0, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_FIREWOOD, amount=1),
            LootItemEntry(chances=12, item_type=ItemType.PROVISION, item_id="", amount=2),
            LootItemEntry(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_SHOVEL, amount=1),
            LootItemEntry(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_ANTIVENOM, amount=1),
            LootItemEntry(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_BANDAGE, amount=1),
            LootItemEntry(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_MEDICINAL_HERBS, amount=1),
            LootItemEntry(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_SKELETON_KEY, amount=1),
            LootItemEntry(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_HOLY_WATER, amount=1),
            LootItemEntry(chances=8, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_TORCH, amount=1),
            LootTableEntry(chances=2, loot_table_id="BLOOD_ALWAYS"),
        )
    ), LootTable(
        name="WOOD_LOOT",
        loot_entries=(
            LootNothingEntry(chances=0),
            LootItemEntry(chances=1, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_FIREWOOD, amount=2),
            LootItemEntry(chances=25, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_FIREWOOD, amount=1),
        )
    )

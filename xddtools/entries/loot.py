from typing import Union, Optional, Dict, Any, Sequence, List

from pydantic import BaseModel, ConfigDict, Field, model_validator

from xddtools.enum.trinket import DungeonID
from xddtools.name import AutoName
from xddtools.base import JsonData, ItemEntry, LootTableEntry, get_entry_id, TrinketRarityEntry
from xddtools.enum.buff_rule import ItemID, ItemType
from xddtools.enum.loot import LootType


class Loot(JsonData, BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    chances: int

    item_type: Optional[ItemType] = None
    item_id: Union[ItemEntry, ItemID, str, None] = None
    item_amount: Optional[int] = None

    min_page_index: Optional[int] = None
    max_page_index: Optional[int] = None

    trinket_rarity: Union[TrinketRarityEntry, str, None] = None

    loot_table_id: Union[LootTableEntry, str, None] = None

    loot_type: Optional[LootType] = Field(None, init=False)

    @model_validator(mode="before")
    @classmethod
    def _check_before(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        item_type = values.get("item_type")
        item_id = values.get("item_id")
        item_amount = values.get("item_amount")

        min_page_index = values.get("min_page_index")
        max_page_index = values.get("max_page_index")

        trinket_rarity = values.get("trinket_rarity")

        loot_table_id = values.get("loot_table_id")

        args = [item_type, item_id, item_amount, min_page_index, max_page_index, loot_table_id, trinket_rarity]
        none_num = args.count(None)
        if none_num == 7:
            values["loot_type"] = LootType.NOTHING
        elif none_num == 6:
            if loot_table_id is None and trinket_rarity is None:
                raise ValueError("item_type, item_id, item_amount must be set together,"
                                 "or min_page_index, max_page_index together, "
                                 "or loot_table_id only, or trinket_rarity only")
            values["loot_type"] = LootType.TABLE
        elif none_num == 5:
            if min_page_index is None or max_page_index is None:
                raise ValueError("item_type, item_id, item_amount must be set together,"
                                 "or min_page_index, max_page_index together, "
                                 "or loot_table_id only, or trinket_rarity only")
            values["loot_type"] = LootType.JOURNAL_PAGE
        elif none_num == 4:
            if item_type is None or item_id is None or item_amount is None:
                raise ValueError("item_type, item_id, item_amount must be set together,"
                                 "or min_page_index, max_page_index together, "
                                 "or loot_table_id only, or trinket_rarity only")
            values["loot_type"] = LootType.ITEM
        else:
            raise ValueError("item_type, item_id, item_amount must be set together,"
                             "or min_page_index, max_page_index together, "
                             "or loot_table_id only, or trinket_rarity only")

        return values

    def get_dict(self) -> dict:
        if self.loot_type == LootType.NOTHING:
            data = {}
        elif self.loot_type == LootType.ITEM:
            data = {
                "type": self.item_type.value,
                "id": get_entry_id(self.item_id),
                "amount": self.item_amount
            }
        elif self.loot_type == LootType.JOURNAL_PAGE:
            data = {
                "min_page_index": self.min_page_index,
                "max_page_index": self.max_page_index
            }
        elif self.loot_type == LootType.TABLE:
            data = {
                "table": get_entry_id(self.loot_table_id)
            }
        elif self.loot_type == LootType.TRINKET:
            data = {
                "rarity": get_entry_id(self.trinket_rarity)
            }
        else:
            raise ValueError("Unknown loot_type")
        return {
            "type": self.loot_type.value,
            "chances": self.chances,
            "data": data
        }


class LootTable(JsonData, LootTableEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    loot_entries: Sequence[Loot]
    difficulty: int = 0,
    dungeon: Union[DungeonID, str] = ""

    entry_id: str = Field(default_factory=lambda x: AutoName().new_loot_table(), frozen=True)

    def get_dict(self) -> dict:
        return {
            "id": self.id(),
            "difficulty": self.difficulty,
            "dungeon": get_entry_id(self.dungeon),
            "entries": [loot_entry.get_dict() for loot_entry in self.loot_entries]
        }


def get_common_overrides_loot_tables() -> List[LootTable]:
    return [LootTable(
        entry_id="A",
        loot_entries=[
            Loot(chances=0),
            Loot(chances=50, loot_table_id="C"),
            Loot(chances=38, loot_table_id="G"),
            Loot(chances=48, loot_table_id="H"),
            Loot(chances=0, loot_table_id="J"),
            Loot(chances=0, loot_table_id="P"),
            Loot(chances=28, loot_table_id="S"),
            Loot(chances=8, loot_table_id="T"),
            Loot(chances=2, min_page_index=1, max_page_index=21),
            Loot(chances=4, loot_table_id="BLOOD_ALWAYS"),
        ]
    ), LootTable(
        entry_id="S",
        loot_entries=[
            Loot(chances=0),
            Loot(chances=0, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_FIREWOOD, item_amount=1),
            Loot(chances=12, item_type=ItemType.PROVISION, item_id="", item_amount=2),
            Loot(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_SHOVEL, item_amount=1),
            Loot(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_ANTIVENOM, item_amount=1),
            Loot(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_BANDAGE, item_amount=1),
            Loot(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_MEDICINAL_HERBS, item_amount=1),
            Loot(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_SKELETON_KEY, item_amount=1),
            Loot(chances=4, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_HOLY_WATER, item_amount=1),
            Loot(chances=8, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_TORCH, item_amount=1),
            Loot(chances=2, loot_table_id="BLOOD_ALWAYS"),
        ]
    ), LootTable(
        entry_id="WOOD_LOOT",
        loot_entries=[
            Loot(chances=0),
            Loot(chances=1, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_FIREWOOD, item_amount=2),
            Loot(chances=25, item_type=ItemType.SUPPLY, item_id=ItemID.SUPPLY_FIREWOOD, item_amount=1),
        ]
    )]


if __name__ == '__main__':
    # lot = Loot(chances=2, max_page_index=24, min_page_index=1)
    # lt = LootTable(loot_entries=[lot], difficulty=1, dungeon=DungeonID.COVE)
    # print(lt)
    entries = get_common_overrides_loot_tables()
    for entry in entries:
        print(entry)

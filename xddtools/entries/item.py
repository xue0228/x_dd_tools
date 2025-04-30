from typing import Optional, Sequence

from pydantic import ConfigDict, BaseModel, field_validator, model_validator

from xddtools.base import ItemEntry, EffectEntry, AnimationEntry, BankEntry
from xddtools.enum.buff_rule import ItemType
from xddtools.utils import is_image


class Item(ItemEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    effect: EffectEntry
    item_type: ItemType = ItemType.ESTATE
    base_stack_limit: int = 1
    purchase_gold_value: int = 0
    purchase_shard_value: int = 0
    sell_gold_value: int = 0
    estate_can_be_provision: bool = True
    tutorial_id: Optional[str] = None
    sfx_override: Optional[str] = None

    raid_starting_item_lists: Optional[Sequence[Optional[int]]] = None
    default_store_item_lists: Optional[Sequence[Optional[int]]] = None

    fx: Optional[AnimationEntry] = None
    sfx: Optional[BankEntry] = None
    item_image: Optional[str] = None
    str_inventory_title: Optional[str] = None
    str_inventory_description: Optional[str] = None

    @field_validator("item_image")
    @classmethod
    def _check_item_image(cls, v: str):
        if (v is not None) and (not is_image(v)):
            raise ValueError(f"{v} is not a valid image path")
        return v

    @model_validator(mode="after")
    def _check_after(self):
        if self.raid_starting_item_lists is not None and len(self.raid_starting_item_lists) != 6:
            raise ValueError("raid_starting_item_lists must be a list of 6 integers")
        if self.default_store_item_lists is not None and len(self.default_store_item_lists) != 6:
            raise ValueError("default_store_item_lists must be a list of 6 integers")

        if self.item_type == ItemType.SUPPLY:
            if self.raid_starting_item_lists is None:
                self.raid_starting_item_lists = [None, 0, 0, 0, 0, 0]
            if self.default_store_item_lists is None:
                self.default_store_item_lists = [None, 6, 9, 12, 15, 12]
        return self

    def get_amount_entry(self, num: Optional[int]) -> Optional[dict]:
        if num is None:
            return None
        return {
            "type": self.item_type.value,
            "id": self.id(),
            "amount": num
        }

    def id(self) -> str:
        return self.effect.id()

    def __str__(self):
        res = [
            f'inventory_item: .type "{self.item_type.value}"',
            f'.id "{self.id()}"',
            f'.base_stack_limit {self.base_stack_limit}'
        ]
        if self.purchase_shard_value != 0:
            res.append(f'.purchase_shard_value {self.purchase_shard_value}')
        else:
            res.append(f'.purchase_gold_value {self.purchase_gold_value}')
        res.append(f'.sell_gold_value {self.sell_gold_value}')
        if self.estate_can_be_provision:
            res.append(f'.estate_can_be_provision true')
        if self.tutorial_id is not None:
            res.append(f'.tutorial_id "{self.tutorial_id}"')
        if self.sfx_override is not None:
            res.append(f'.sfx_override "{self.sfx_override}"')

        return " ".join(res)

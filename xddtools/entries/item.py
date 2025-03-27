from typing import Optional

from pydantic import ConfigDict, BaseModel, field_validator

from xddtools.base import ItemEntry, EffectEntry
from xddtools.enum.buff_rule import ItemType
from xddtools.utils import is_image


class Item(ItemEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    effect: EffectEntry
    item_type: ItemType = ItemType.ESTATE
    base_stack_limit: int = 1
    purchase_gold_value: int = 0
    sell_gold_value: int = 0
    estate_can_be_provision: bool = True
    tutorial_id: Optional[str] = None
    sfx_override: Optional[str] = None

    item_image: Optional[str] = None
    str_inventory_title: Optional[str] = None
    str_inventory_description: Optional[str] = None

    @field_validator("item_image")
    @classmethod
    def _check_item_image(cls, v: str):
        if (v is not None) and (not is_image(v)):
            raise ValueError(f"{v} is not a valid image path")
        return v

    def id(self) -> str:
        return self.effect.id()

    def __str__(self):
        res = [
            f'inventory_item: .type "{self.item_type.value}"',
            f'.id "{self.id()}"',
            f'.base_stack_limit {self.base_stack_limit}',
            f'.purchase_gold_value {self.purchase_gold_value}',
            f'.sell_gold_value {self.sell_gold_value}',
        ]
        if self.estate_can_be_provision:
            res.append(f'.estate_can_be_provision true')
        if self.tutorial_id is not None:
            res.append(f'.tutorial_id "{self.tutorial_id}"')
        if self.sfx_override is not None:
            res.append(f'.sfx_override "{self.sfx_override}"')

        return " ".join(res)

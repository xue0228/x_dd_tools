import os
from typing import Tuple, Union, Optional

from xddtools.base import BaseLocalization
from xddtools.effects import Effect
from xddtools.enums import ItemType
from xddtools.path import ITEM_IMAGE_SAVE_DIR
from xddtools.utils import bool_to_lower_str, is_image, resize_image_keep_ratio


class Item(BaseLocalization):
    def __init__(
            self,
            effect: Effect,
            image_path: Optional[str] = None,
            item_type: ItemType = ItemType.ESTATE,
            base_stack_limit: int = 1,
            purchase_gold_value: int = 0,
            sell_gold_value: int = 0,
            estate_can_be_provision: bool = True,
            tutorial_id: Optional[str] = None,
            sfx_override: Optional[str] = None,
            localization: Union[Tuple[str, ...], str, None] = None,
    ):
        """
        crimson_court.estate.inventory.items.darkest

        inventory_item:	.type "estate_currency"	.id "crimson_court_invitation_A"  .base_stack_limit 100	.purchase_gold_value 0  .sell_gold_value 0
        inventory_item:	.type "estate_currency"	.id "crimson_court_invitation_B"  .base_stack_limit 100	.purchase_gold_value 0  .sell_gold_value 0
        inventory_item:	.type "estate_currency"	.id "crimson_court_invitation_C"  .base_stack_limit 100	.purchase_gold_value 0  .sell_gold_value 0
        inventory_item:	.type "estate"	        .id "the_blood"					  .base_stack_limit 6	.purchase_gold_value 0	.sell_gold_value 0 .estate_can_be_provision true .tutorial_id "the_blood"
        inventory_item:	.type "estate"	        .id "the_cure"					  .base_stack_limit 6	.purchase_gold_value 0	.sell_gold_value 0 .estate_can_be_provision true .sfx_override "/general/items/holy_water"
        :param effect:
        :param item_type:
        :param base_stack_limit:
        :param purchase_gold_value:
        :param sell_gold_value:
        :param estate_can_be_provision:
        :param tutorial_id:
        :param sfx_override:
        :param localization:
        """
        if (image_path is not None) and (not is_image(image_path)):
            raise ValueError(f"{image_path} is not a image")
        self.image_path = image_path

        name = effect.id
        self.effect = effect
        self.item_type = item_type
        self.base_stack_limit = base_stack_limit
        self.purchase_gold_value = purchase_gold_value
        self.sell_gold_value = sell_gold_value
        self.estate_can_be_provision = estate_can_be_provision
        self.tutorial_id = tutorial_id
        self.sfx_override = sfx_override
        super().__init__(
            name=name,
            localization=localization,
            entry_id_prefix=("str_inventory_title_", "str_inventory_description_"),
        )

    @property
    def localization_id(self) -> Optional[str]:
        return f"{self.item_type.value}{self.id}"

    def __str__(self):
        res = [
            f'inventory_item: .type "{self.item_type.value}"',
            f'.id "{self.id}"',
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

        return " ".join(res) + "\n"

    def export_image(self, root_dir: Optional[str] = None) -> str:
        if self.image_path is None:
            raise ValueError("image_path is None")
        if root_dir is None:
            root_dir = "./"
        save_dir = os.path.join(root_dir, ITEM_IMAGE_SAVE_DIR, self.item_type.value)
        filename = f"inv_{self.item_type.value}+{self.id}.png"
        file = os.path.join(save_dir, filename)
        return resize_image_keep_ratio(self.image_path, file)

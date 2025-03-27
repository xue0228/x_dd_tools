import os
from typing import List, Optional

from xddtools.base import BaseWriter, Entry, ItemEntry
from xddtools.entries.localization import Localization
from xddtools.entries.item import Item
from xddtools.path import ITEM_SAVE_DIR, ITEM_FILE_EXTENSION, DATA_PATH, ITEM_IMAGE_SAVE_DIR
from xddtools.utils import resize_image_keep_ratio


class ItemWriter(BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=ITEM_SAVE_DIR,
            extension=ITEM_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, ItemEntry)

    def add_entry(self, entry: Item) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)
        res = []
        if isinstance(entry.effect, Entry):
            res.append(entry.effect)

        if entry.str_inventory_title is not None:
            res.append(Localization(
                entry_id=f"str_inventory_title_{entry.item_type.value}{entry.id()}",
                text=entry.str_inventory_title
            ))
        if entry.str_inventory_description is not None:
            res.append(Localization(
                entry_id=f"str_inventory_description_{entry.item_type.value}{entry.id()}",
                text=entry.str_inventory_description
            ))

        return res

    def __str__(self):
        return "\n".join([str(item) for item in self._entries]) + "\n"

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        if root_dir is None:
            root_dir = "./"

        res = []
        for item in self._entries:  # type: Item
            if item.item_image is None:
                image_path = os.path.join(DATA_PATH, "template/item/item_unknown.png")
            else:
                image_path = item.inv_trinket_image
            file = os.path.join(
                root_dir,
                ITEM_IMAGE_SAVE_DIR,
                item.item_type.value,
                f"inv_{item.item_type.value}+{item.id()}.png"
            )
            res.append(resize_image_keep_ratio(image_path, file))

        res.extend(super().export(root_dir))
        return res

import os
from typing import List, Optional

from xddtools.base import BaseWriter, Entry, ItemEntry
from xddtools.entries.bank import Bank
from xddtools.entries.animation import Animation
from xddtools.entries.effect import Effect
from xddtools.entries.localization import Localization
from xddtools.entries.item import Item
from xddtools.enum.bank import BankDir, BankSource
from xddtools.path import ITEM_SAVE_DIR, ITEM_FILE_EXTENSION, DATA_PATH, ITEM_IMAGE_SAVE_DIR
from xddtools.utils import resize_image_keep_ratio, get_rename_skel_dict_func


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
        if isinstance(entry.effect, Effect):
            entry.effect.item = True
            res.append(entry.effect)

        if isinstance(entry.fx, Animation):
            res.append(entry.fx.model_copy(update={
                "is_fx": True,
                "anim_name": entry.id(),
                # "need_rename": False,
                "dict_func": get_rename_skel_dict_func("cure_target")
            }))

        if isinstance(entry.sfx, Bank):
            res.append(entry.sfx.model_copy(update={
                "bank_dir": BankDir.GENERAL_ITEMS,
                "bank_name": entry.id(),
                "guid": entry.sfx.guid,
                "audio": entry.sfx.audio,
                "source": BankSource.GENERAL
            }))

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
                image_path = item.item_image
            file = os.path.join(
                root_dir,
                ITEM_IMAGE_SAVE_DIR,
                item.item_type.value,
                f"inv_{item.item_type.value}+{item.id()}.png"
            )
            res.append(resize_image_keep_ratio(image_path, file))

        res.extend(super().export(root_dir))
        return res

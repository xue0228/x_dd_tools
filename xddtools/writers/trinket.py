import os
from typing import List, Optional

from xddtools.base import JsonData, BaseWriter, Entry, TrinketSetEntry, TrinketRarityEntry, TrinketEntry
from xddtools.entries.localization import Localization
from xddtools.entries.trinket import TrinketSet, TrinketRarity, Trinket
from xddtools.path import TRINKET_SET_FILE_EXTENSION, TRINKET_SAVE_DIR, TRINKET_RARITY_FILE_EXTENSION, DATA_PATH, \
    TRINKET_IMAGE_SAVE_DIR, TRINKET_ENTRY_FILE_EXTENSION
from xddtools.utils import resize_image, resize_image_keep_ratio


class TrinketSetWriter(JsonData, BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=TRINKET_SAVE_DIR,
            extension=TRINKET_SET_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, TrinketSetEntry)

    def add_entry(self, entry: TrinketSet) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)
        res = []
        if entry.buffs is not None:
            for buff in entry.buffs:
                if isinstance(buff, Entry):
                    res.append(buff)

        if entry.str_inventory_set_title is not None:
            res.append(Localization(
                entry_id=f"str_inventory_set_title_{entry.id()}",
                text=entry.str_inventory_set_title,
            ))
        return res

    def get_dict(self) -> dict:
        tem = []
        for item in self._entries:  # type: TrinketSet
            tem.append(item.get_dict())
        return {"sets": tem}


class TrinketRarityWriter(JsonData, BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=TRINKET_SAVE_DIR,
            extension=TRINKET_RARITY_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, TrinketRarityEntry)

    def add_entry(self, entry: TrinketRarity) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)
        res = []
        if isinstance(entry.insert_before, Entry):
            res.append(entry.insert_before)

        if entry.trinket_rarity_title is not None:
            res.append(Localization(
                entry_id=f"trinket_rarity_{entry.id()}",
                text=entry.trinket_rarity_title,
            ))
        return res

    def get_dict(self) -> dict:
        tem = []
        for item in self._entries:  # type: TrinketRarity
            tem.append(item.get_dict())
        return {"rarities": tem}

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        if root_dir is None:
            root_dir = "./"

        res = []
        for item in self._entries:  # type: TrinketRarity
            if item.rarity_image is None:
                image_path = os.path.join(DATA_PATH, "template/trinket/rarity_comet.png")
            else:
                image_path = item.rarity_image
            file = os.path.join(root_dir, TRINKET_IMAGE_SAVE_DIR, f"rarity_{item.id()}.png")
            res.append(resize_image(image_path, file))

        res.extend(super().export(root_dir))
        return res


class TrinketWriter(JsonData, BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=TRINKET_SAVE_DIR,
            extension=TRINKET_ENTRY_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, TrinketEntry)

    def add_entry(self, entry: Trinket) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)
        res = []
        if entry.buffs is not None:
            for buff in entry.buffs:
                if isinstance(buff, Entry):
                    res.append(buff)
        if entry.hero_class_requirements is not None:
            for hero in entry.hero_class_requirements:
                if isinstance(hero, Entry):
                    res.append(hero)
        if isinstance(entry.set_id, Entry):
            res.append(entry.set_id)
        if isinstance(entry.rarity, Entry):
            res.append(entry.rarity)
        if isinstance(entry.visual_rarity, Entry):
            res.append(entry.visual_rarity)
        if entry.special_effects is not None:
            for item in entry.special_effects:
                for effect in item.effects:
                    if isinstance(effect, Entry):
                        res.append(effect)

        if entry.str_inventory_title_trinket is not None:
            res.append(Localization(
                entry_id=f"str_inventory_title_trinket{entry.id()}",
                text=entry.str_inventory_title_trinket
            ))
        return res

    def get_dict(self) -> dict:
        tem = []
        for item in self._entries:  # type: Trinket
            tem.append(item.get_dict())
        return {"entries": tem}

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        if root_dir is None:
            root_dir = "./"

        res = []
        for item in self._entries:  # type: Trinket
            if item.inv_trinket_image is None:
                image_path = os.path.join(DATA_PATH, "template/trinket/trinket_unknown.png")
            else:
                image_path = item.inv_trinket_image
            file = os.path.join(root_dir, TRINKET_IMAGE_SAVE_DIR, f"inv_trinket+{item.id()}.png")
            res.append(resize_image_keep_ratio(image_path, file))

        res.extend(super().export(root_dir))
        return res

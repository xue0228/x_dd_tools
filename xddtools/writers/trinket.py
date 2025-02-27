from typing import Optional, Iterable, Dict, Tuple

from xddtools.base import BaseJsonData, BaseWriter, BaseID, LocalizationWriter
from xddtools.buffs import Buff
from xddtools.effects import Effect
from xddtools.enums import TrinketRarityType
from xddtools.path import TRINKET_SAVE_DIR, TRINKET_SET_FILE_EXTENSION, TRINKET_ENTRY_FILE_EXTENSION, \
    TRINKET_RARITY_FILE_EXTENSION
from xddtools.trinket import TrinketSet, TrinketEntry, TrinketRarity
from xddtools.writers.others import BuffWriter, EffectWriter


class TrinketSetWriter(BaseJsonData, BaseWriter):
    def __init__(
            self,
            name: str,
            sets: Optional[Iterable[TrinketSet]] = None,
            localization_writer: Optional[LocalizationWriter] = None,
    ):
        super().__init__(
            name=name,
            relative_save_dir=TRINKET_SAVE_DIR,
            extension=TRINKET_SET_FILE_EXTENSION,
            items=sets,
            localization_writer=localization_writer,
        )

    def dict(self) -> Dict:
        return {"sets": [item.dict() for item in self._items]}


class TrinketEntryWriter(BaseJsonData, BaseWriter):
    def __init__(
            self,
            name: str,
            entries: Optional[Iterable[TrinketEntry]] = None,
            localization_writer: Optional[LocalizationWriter] = None,
    ):
        super().__init__(
            name=name,
            relative_save_dir=TRINKET_SAVE_DIR,
            extension=TRINKET_ENTRY_FILE_EXTENSION,
            items=entries,
            localization_writer=localization_writer,
        )

    def dict(self) -> Dict:
        return {"entries": [item.dict() for item in self._items]}

    def export(self, root_dir: Optional[str] = None) -> str:
        for item in self._items:
            item.export_image(root_dir)
        return super().export(root_dir)


class TrinketRarityWriter(BaseJsonData, BaseWriter):
    def __init__(
            self,
            name: str,
            rarities: Optional[Iterable[TrinketRarity]] = None,
            localization_writer: Optional[LocalizationWriter] = None,
    ):
        super().__init__(
            name=name,
            relative_save_dir=TRINKET_SAVE_DIR,
            extension=TRINKET_RARITY_FILE_EXTENSION,
            items=rarities,
            localization_writer=localization_writer,
        )

    def dict(self) -> Dict:
        return {"rarities": [item.dict() for item in self._items]}

    def export(self, root_dir: Optional[str] = None) -> str:
        for item in self._items:
            item.export_image(root_dir)
        return super().export(root_dir)


class Trinket(BaseID):
    def __init__(
            self,
            name: str,
            buff_writer: Optional[BuffWriter] = None,
            effect_writer: Optional[EffectWriter] = None,
            localization_writer: Optional[LocalizationWriter] = None,
            is_test: bool = False,
    ):
        self._is_test = is_test
        self._buff_writer = buff_writer
        self._effect_writer = effect_writer
        self._localization_writer = localization_writer
        self._set_writer = TrinketSetWriter(name=name, localization_writer=localization_writer)
        self._entry_writer = TrinketEntryWriter(name=name, localization_writer=localization_writer)
        self._rarity_writer = TrinketRarityWriter(name=name, localization_writer=localization_writer)
        super().__init__(name=name)

    def __len__(self):
        return len(self._set_writer) + len(self._entry_writer) + len(self._rarity_writer)

    def add_item(self, entry: TrinketEntry):
        if entry.buffs is not None:
            for buff in entry.buffs:
                if isinstance(buff, Buff):
                    if self._buff_writer is not None:
                        self._buff_writer.add_item(buff)

        if entry.set_id is not None and isinstance(entry.set_id, TrinketSet):
            if entry.set_id.buffs is not None:
                for buff in entry.set_id.buffs:
                    if isinstance(buff, Buff):
                        if self._buff_writer is not None:
                            self._buff_writer.add_item(buff)

            self._set_writer.add_item(entry.set_id)

        if entry.rarity is not None and isinstance(entry.rarity, TrinketRarity):
            self._rarity_writer.add_item(entry.rarity)

        if entry.special_effects is not None:
            for k, v in entry.special_effects.items():
                for effect in v:
                    if isinstance(effect, Effect):
                        if self._effect_writer is not None:
                            self._effect_writer.add_item(effect)

        if self._is_test:
            entry.rarity = TrinketRarityType.COMET
            entry.price = None
            entry.shard = 0
        self._entry_writer.add_item(entry)

    def add_items(self, entries: Iterable[TrinketEntry]):
        for entry in entries:
            self.add_item(entry)

    def export(
            self,
            root_dir: Optional[str] = None,
            export_other_writers: bool = False
    ) -> Tuple[str, ...]:
        res = []
        if export_other_writers:
            if self._buff_writer is not None:
                res.append(self._buff_writer.export(root_dir))
            if self._effect_writer is not None:
                res.append(self._effect_writer.export(root_dir))
            if self._localization_writer is not None:
                res.append(self._localization_writer.export(root_dir))
        res.append(self._set_writer.export(root_dir))
        res.append(self._entry_writer.export(root_dir))
        res.append(self._rarity_writer.export(root_dir))
        return tuple(res)

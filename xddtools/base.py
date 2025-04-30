import json
import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Iterable, Optional, NoReturn, Union

from loguru import logger

from xddtools.utils import write_str_to_file


class Entry:
    def id(self) -> str:
        return self.entry_id

    def __eq__(self, other):
        if isinstance(other, Entry):
            return self.id() == other.id()
        return False


def get_entry_id(entry: Union[Entry, Enum, str]) -> str:
    if isinstance(entry, Entry):
        return entry.id()
    elif isinstance(entry, Enum):
        return entry.value
    else:
        return entry


class JsonData(ABC):
    @abstractmethod
    def get_dict(self) -> dict:
        pass

    def __str__(self):
        return json.dumps(self.get_dict(), indent=2)


class BuffEntry(Entry):
    pass


class LocalizationEntry(Entry):
    pass


class SkillEntry(Entry):
    pass


class CampingSkillEntry(Entry):
    pass


class QuirkEntry(Entry):
    pass


class ModeEntry(Entry):
    pass


class ItemEntry(Entry):
    pass


class AnimationEntry(Entry):
    def name(self) -> str:
        raise NotImplementedError("please implement name() method")


class EffectEntry(Entry):
    pass


class HeroEntry(Entry):
    pass


class MonsterEntry(Entry):
    pass


class LootMonsterEntry(MonsterEntry):
    pass


class TrinketEntry(Entry):
    pass


class TrinketSetEntry(Entry):
    pass


class TrinketRarityEntry(Entry):
    pass


class ActorDotEntry(Entry):
    pass


class ColourEntry(Entry):
    pass


class ProjectEntry(Entry):
    pass


class TraitEntry(Entry):
    pass


class LootTableEntry(Entry):
    pass


class TownEventEntry(Entry):
    pass


class BankEntry(Entry):
    pass


class BaseWriter(ABC):
    def __init__(self, prefix: str,
                 relative_save_dir: Optional[str] = None,
                 extension: Optional[str] = None):
        self.prefix = prefix
        self._relative_save_dir = relative_save_dir
        self._extension = extension
        self._entries: List[Entry] = []

    @abstractmethod
    def is_valid(self, entry: Entry) -> bool:
        pass

    @abstractmethod
    def add_entry(self, entry: Entry) -> List[Entry]:
        pass

    def add_entries(self, entries: Iterable[Entry]) -> List[Entry]:
        res = []
        for entry in entries:
            res.extend(self.add_entry(entry))
        return res

    def __len__(self):
        return len(self._entries)

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        if self._relative_save_dir is None or self._extension is None:
            raise NotImplementedError("please implement export() method")
        if root_dir is None:
            root_dir = "./"
        file = os.path.join(root_dir, self._relative_save_dir, f"{self.prefix}{self._extension}")
        return [write_str_to_file(file, str(self))]


class ProxyWriter:
    def __init__(self, writers: Optional[Iterable[BaseWriter]] = None):
        self._writers: List[BaseWriter] = []
        self._ids = set()
        self._unsupported = []

        if writers is not None:
            self.add_writers(writers)

    def add_writer(self, writer: BaseWriter) -> NoReturn:
        self._writers.append(writer)
        logger.info(f"add writer: {writer.__class__.__name__}")

    def add_writers(self, writers: Iterable[BaseWriter]) -> NoReturn:
        for writer in writers:
            self.add_writer(writer)

    def _add_entry(self, entry: Entry) -> NoReturn:
        entry_id = entry.id() + f"_{entry.__class__.__name__}"
        logger.info(f"开始处理：{entry_id}")

        if entry_id not in self._ids:
            for writer in self._writers:
                if writer.is_valid(entry):
                    tem = writer.add_entry(entry)
                    if not isinstance(entry, LocalizationEntry):
                        self._ids.add(entry_id)
                    for e in tem:
                        self._add_entry(e)
                    logger.info(f"成功处理：{entry_id}")
                    return
            self._unsupported.append(entry)
            logger.warning(f"未找到合适的writer：{entry_id}")
        else:
            logger.info(f"重复项：{entry_id}")

    def add_entry(self, entry: Entry) -> List[Entry]:
        self._unsupported = []
        self._add_entry(entry)
        return self._unsupported

    def add_entries(self, entries: Iterable[Entry]) -> List[Entry]:
        res = []
        for entry in entries:
            res.extend(self.add_entry(entry))
        return res

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        res = []
        for writer in self._writers:
            if len(writer) > 0:
                tem = writer.export(root_dir)
                res.extend(tem)
                tem = "\n".join(tem)
                logger.info(f"writer {writer.__class__.__name__} 导出成功：\n{tem}")
            else:
                logger.warning(f"writer {writer.__class__.__name__} 没有内容")
        return res


if __name__ == '__main__':
    p = ProxyWriter()
    t = BuffEntry()
    t.entry_id = "xue"
    u = p.add_entry(t)
    print(u)
    p._unsupported = []
    print(u)

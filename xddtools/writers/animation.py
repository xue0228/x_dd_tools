from typing import List

from xddtools.base import BaseWriter, Entry, AnimationEntry, HeroEntry, MonsterEntry
from xddtools.entries.animation import Animation


class AnimationWriter(BaseWriter):
    def __init__(self, prefix: str = ""):
        super().__init__(
            prefix=prefix
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, AnimationEntry)

    def add_entry(self, entry: Animation) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)

        res = []
        if isinstance(entry.hero_name, HeroEntry):
            res.append(entry.hero_name)
        if isinstance(entry.monster_name, MonsterEntry):
            res.append(entry.monster_name)
        return res

    def export(self, root_dir: str = None) -> List[str]:
        if root_dir is None:
            root_dir = "./"
        res = []
        for entry in self._entries:  # type: Animation
            res.extend(entry.copy_and_rename_animation(root_dir))
        return res

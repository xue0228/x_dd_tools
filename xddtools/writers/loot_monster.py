import os.path
from typing import List, Optional

from xddtools.base import BaseWriter, Entry, LootMonsterEntry
from xddtools.entries.bank import Bank
from xddtools.entries.animation import Animation
from xddtools.entries.loot_monster import LootMonster
from xddtools.enum.bank import BankDir, BankSource
from xddtools.path import DATA_PATH, MONSTER_SAVE_DIR
from xddtools.utils import write_str_to_file


class LootMonsterWriter(BaseWriter):
    def __init__(self, prefix: Optional[str] = None):
        super().__init__(
            prefix=prefix
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, LootMonsterEntry)

    def add_entry(self, entry: LootMonster) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)

        res = []

        if isinstance(entry.loot, Entry):
            res.append(entry.loot)
        if entry.spawn_effects is not None:
            for effect in entry.spawn_effects:
                if isinstance(effect, Entry):
                    res.append(effect)

        if isinstance(entry.sfx, Bank):
            res.append(entry.sfx.model_copy(update={
                "bank_dir": BankDir.CHAR_ENEMY,
                "bank_name": f"{entry.id()}_vo_death",
                "guid": entry.sfx.guid,
                "audio": entry.sfx.audio,
                "source": BankSource.EN
            }))

        res.append(Animation(
            anim_name="defend",
            anim_dir=os.path.join(DATA_PATH, "template/fx/loot_monster"),
            monster_name=entry.id(),
            need_rename=False
        ))

        return res

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        if root_dir is None:
            root_dir = "./"

        res = []
        for entry in self._entries:  # type: LootMonster
            monster_dir = os.path.join(root_dir, MONSTER_SAVE_DIR, entry.id(), f"{entry.id()}_A")
            file = os.path.join(monster_dir, f"{entry.id()}_A.info.darkest")
            res.append(write_str_to_file(file, entry.info()))
            file = os.path.join(monster_dir, f"{entry.id()}_A.art.darkest")
            res.append(write_str_to_file(file, entry.art()))

        return res

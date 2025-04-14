from typing import List

from xddtools.base import JsonData, BaseWriter, Entry, ActorDotEntry, get_entry_id
from xddtools.entries.bank import Bank
from xddtools.entries.animation import Animation
from xddtools.entries.actor_dot import ActorDot
from xddtools.enum import BankDir, BankSource
from xddtools.path import ACTOR_DOT_SAVE_DIR, ACTOR_DOT_FILE_EXTENSION


class ActorDotWriter(JsonData, BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=ACTOR_DOT_SAVE_DIR,
            extension=ACTOR_DOT_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, ActorDotEntry)

    def add_entry(self, entry: ActorDot) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)

        res = []

        if isinstance(entry.fx, Animation):
            entry.fx.anim_name = entry.id()
            entry.fx.is_fx = True
            entry.fx.need_rename = False
            res.append(entry.fx)

        if entry.fx is not None:
            if isinstance(entry.fx_onset_sfx, Bank):
                res.append(entry.fx_onset_sfx.model_copy(update={
                    "bank_dir": BankDir.GENERAL_STATUS,
                    "bank_name": f"actor_dot_{get_entry_id(entry.fx)}_onset",
                    "guid": entry.fx_onset_sfx.guid,
                    "audio": entry.fx_onset_sfx.audio,
                    "source": BankSource.GENERAL
                }))

        for element in entry.duration_elements:
            for effect in element.completion_effects:
                if isinstance(effect, Entry):
                    res.append(effect)
            for effect in element.increment_effects:
                if isinstance(effect, Entry):
                    res.append(effect)

        return res

    def get_dict(self) -> dict:
        tem = []
        for trait in self._entries:  # type: ActorDot
            tem.append(trait.get_dict())
        return {"entries": tem}

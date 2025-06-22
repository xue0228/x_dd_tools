import os
from typing import List, Optional

from xddtools.base import JsonData, BaseWriter, Entry, TownEventEntry
from xddtools.entries import Localization
from xddtools.entries.town_event import TownEvent
from xddtools.path import TOWN_EVENT_SAVE_DIR, TOWN_EVENT_FILE_EXTENSION, TOWN_EVENT_IMAGE_SAVE_DIR
from xddtools.utils import resize_image_keep_ratio


class TownEventWriter(JsonData, BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=TOWN_EVENT_SAVE_DIR,
            extension=TOWN_EVENT_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, TownEventEntry)

    def add_entry(self, entry: TownEvent) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)

        res = []

        for data in entry.data:
            if isinstance(data.string_data, Entry):
                res.append(data.string_data)

        if entry.town_event_title is not None:
            res.append(Localization(
                entry_id=f"town_event_title_{entry.id()}",
                text=entry.town_event_title
            ))
        if entry.town_event_description is not None:
            res.append(Localization(
                entry_id=f"town_event_description_{entry.id()}",
                text=entry.town_event_description
            ))

        return res

    def get_dict(self) -> dict:
        res = []
        for entry in self._entries:  # type: TownEvent
            res.append(entry.get_dict())
        return {"events": res}

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        res = super().export(root_dir)

        if root_dir is None:
            root_dir = "./"

        for entry in self._entries:  # type: TownEvent
            if entry.town_event_image is not None:
                file = os.path.join(
                    root_dir,
                    TOWN_EVENT_IMAGE_SAVE_DIR,
                    f"town_event.image_{entry.id()}.png"
                )
                res.append(resize_image_keep_ratio(entry.town_event_image, file, (500, 240)))

        return res


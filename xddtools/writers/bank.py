import json
import os.path
from typing import List, Optional

from xddtools.base import BaseWriter, JsonData, Entry, BankEntry
from xddtools.entries.bank import Bank, AudioProcessor
from xddtools.path import BANK_SAVE_DIR, BANK_OVERRIDE_FILE_EXTENSION, BANK_LOAD_FILE_EXTENSION, AUDIO_SAVE_DIR
from xddtools.utils import write_str_to_file

_audio_processor = AudioProcessor()


class BankWriter(JsonData, BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(prefix=prefix)

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, BankEntry)

    def add_entry(self, entry: Bank) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)

        res = []

        return res

    def get_dict(self) -> dict:
        tem = []
        for bank in self._entries:  # type: Bank
            tem.append(bank.get_dict())
        return {"event_guid_overrides": tem}

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        if root_dir is None:
            root_dir = "./"

        res = []
        sources = set()
        for bank in self._entries:  # type: Bank
            if bank.audio is not None:
                file = os.path.join(
                    root_dir,
                    BANK_SAVE_DIR,
                    f"{bank.source.value}_{self.prefix}",
                    bank.id()[1:] + ".wav"
                )
                _audio_processor.calculate_and_adjust_db(
                    input_path=bank.audio,
                    output_path=file
                )
                res.append(os.path.normpath(file))
                sources.add(bank.source.value)

        file = os.path.join(root_dir, AUDIO_SAVE_DIR, f"{self.prefix}{BANK_OVERRIDE_FILE_EXTENSION}")
        res.append(
            write_str_to_file(file, str(self))
        )

        tem = {
            "load_order": [f"secondary_banks/{source}_{self.prefix}.bank" for source in sources]
        }
        file = os.path.join(root_dir, AUDIO_SAVE_DIR, f"{self.prefix}{BANK_LOAD_FILE_EXTENSION}")
        res.append(
            write_str_to_file(file, json.dumps(tem, indent=2, ensure_ascii=True))
        )

        return res


if __name__ == '__main__':
    w = BankWriter("xue")
    w.add_entries([
        Bank(
            bank_name="test_0",
        ),
        Bank(
            bank_name="test_1",
            audio="test.wav"
        )
    ])
    w.export("tem")

from typing import List

from xddtools.base import BaseWriter, Entry, BuffEntry, JsonData, get_entry_id, ModeEntry
from xddtools.entries.bank import Bank
from xddtools.entries.animation import Animation
from xddtools.entries.buff import Buff
from xddtools.entries.localization import Localization
from xddtools.enum.bank import BankDir, BankSource
from xddtools.path import BUFF_FILE_EXTENSION, BUFF_SAVE_DIR


class BuffWriter(JsonData, BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=BUFF_SAVE_DIR,
            extension=BUFF_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, BuffEntry)

    def add_entry(self, entry: Buff) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)
        res = []
        if isinstance(entry.stat_sub_type, Entry):
            res.append(entry.stat_sub_type)
        if isinstance(entry.buff_rule.rule_data_string, Entry) and \
                not isinstance(entry.buff_rule.rule_data_string, ModeEntry):
            res.append(entry.buff_rule.rule_data_string)
        if isinstance(entry.fx, Animation):
            entry.fx.is_fx = True
            res.append(entry.fx)
        if entry.fx is not None:
            if isinstance(entry.fx_onset_sfx, Bank):
                res.append(entry.fx_onset_sfx.model_copy(update={
                    "bank_dir": BankDir.GENERAL_STATUS,
                    "bank_name": f"buff_fx_{get_entry_id(entry.fx)}_onset",
                    "guid": entry.fx_onset_sfx.guid,
                    "audio": entry.fx_onset_sfx.audio,
                    "source": BankSource.GENERAL
                }))

        if entry.buff_rule.rule_data_string_tooltip is not None and entry.buff_rule.rule_data_string != "":
            entry_id = f"buff_rule_data_tooltip_{get_entry_id(entry.buff_rule.rule_data_string)}"
            res.append(Localization(
                entry_id=entry_id,
                text=entry.buff_rule.rule_data_string_tooltip,
            ))
        if entry.buff_stat_tooltip is not None:
            tem = [entry.stat_type.value]
            if entry.stat_sub_type != "":
                tem.append(get_entry_id(entry.stat_sub_type))
            entry_id = f"buff_stat_tooltip_{'_'.join(tem)}"
            res.append(Localization(
                entry_id=entry_id,
                text=entry.buff_stat_tooltip,
            ))
        return res

    def get_dict(self) -> dict:
        tem = []
        for buff in self._entries:  # type: Buff
            tem.append(buff.get_dict())
        return {"buffs": tem}


if __name__ == '__main__':
    from xddtools.entries.buff import Buff, BuffType
    from xddtools.base import ProxyWriter
    from xddtools.writers.localization import LocalizationWriter

    b = Buff(
        stat_type=BuffType.RIPOSTE,
        stat_sub_type="test",
        buff_stat_tooltip="测试"
    )
    w = BuffWriter("test")
    l = LocalizationWriter("test2")
    p = ProxyWriter([w, l])
    assert w.is_valid(b)
    print(p.add_entry(b))
    print(p.export())

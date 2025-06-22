from typing import List

from xddtools.base import Entry, EffectEntry, BaseWriter
from xddtools.entries import Localization
from xddtools.entries.effect import Effect
from xddtools.path import EFFECT_SAVE_DIR, EFFECT_FILE_EXTENSION
from xddtools.utils import get_bark_list


class EffectWriter(BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=EFFECT_SAVE_DIR,
            extension=EFFECT_FILE_EXTENSION
        )

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, EffectEntry)

    def add_entry(self, entry: Effect) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)
        res = []
        if isinstance(entry.spawn_target_actor_base_class_id, Entry):
            res.append(entry.spawn_target_actor_base_class_id)
        if isinstance(entry.disease, Entry):
            res.append(entry.disease)
        # if isinstance(entry.set_mode, Entry):
        #     res.append(entry.set_mode)
        if isinstance(entry.actor_dot, Entry):
            res.append(entry.actor_dot)
        if isinstance(entry.damage_source_data, Entry):
            res.append(entry.damage_source_data)
        if isinstance(entry.use_item_id, Entry):
            res.append(entry.use_item_id)
        if isinstance(entry.buff_sub_type, Entry):
            res.append(entry.buff_sub_type)
        if entry.buff_ids is not None:
            for buff in entry.buff_ids:
                if isinstance(buff, Entry):
                    res.append(buff)
        if entry.riposte_effect is not None:
            for effect in entry.riposte_effect:
                if isinstance(effect, Entry):
                    res.append(effect)
        if entry.summon_monsters is not None:
            for monster in entry.summon_monsters:
                if isinstance(monster, Entry):
                    res.append(monster)

        for bark in get_bark_list(entry.barks):
            res.append(Localization(
                entry_id=entry.bark_id(),
                text=bark
            ))

        return res

    def __str__(self):
        return "\n".join([str(effect) for effect in self._entries]) + "\n"


if __name__ == '__main__':
    from xddtools.entries.effect import EffectTarget

    e = EffectWriter("test")
    e.add_entry(Effect(target=EffectTarget.PERFORMER))
    e.add_entry(Effect(target=EffectTarget.PERFORMER))
    e.add_entry(Effect(target=EffectTarget.PERFORMER))
    e.add_entry(Effect(target=EffectTarget.PERFORMER))
    e.add_entry(Effect(target=EffectTarget.PERFORMER))
    e.export()

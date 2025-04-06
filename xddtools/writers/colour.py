import importlib.util
import os
from typing import List

from xddtools.base import BaseWriter, Entry, ColourEntry
from xddtools.entries.colour import Colour
from xddtools.path import COLOUR_SAVE_DIR, COLOUR_FILE_EXTENSION


class ColourWriter(BaseWriter):
    def __init__(self, prefix: str):
        super().__init__(
            prefix=prefix,
            relative_save_dir=COLOUR_SAVE_DIR,
            extension=COLOUR_FILE_EXTENSION
        )
        self._ordered = []
        self._ordered_ids = []

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, ColourEntry)

    def add_entry(self, entry: Colour) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)
        res = []
        if isinstance(entry.shared_id, Entry):
            res.append(entry.shared_id)
        return res

    def _put_colour_in_order(self, colour: Colour):
        if colour.id() not in self._ordered_ids:
            if colour.shared_id is not None:
                self._put_colour_in_order(colour.shared_id)
            self._ordered.append(colour)
            self._ordered_ids.append(colour.id())

    def __str__(self):
        self._ordered = []
        self._ordered_ids = []
        for colour in self._entries:  # type: Colour
            self._put_colour_in_order(colour)

        return "\n".join([str(colour) for colour in self._ordered]) + "\n"


def get_colour_writer(
        prefix: str
):
    # from xddtools.entries.colour import bleed, blight, stress, heal_hp, skill_unselectable, debuff
    # res = ColourWriter(prefix)
    # res.add_entries((bleed, blight, stress, heal_hp, skill_unselectable, debuff))
    # return res

    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "entries/colour.py")
    # 获取模块名（去掉 .py 后缀）
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    # 创建模块的 spec 和模块对象
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    # 加载模块
    spec.loader.exec_module(module)

    # 使用 vars() 获取模块的所有属性
    all_attributes = vars(module)

    # 过滤掉内置属性、函数和类
    variables = [
        value for key, value in all_attributes.items()
        if not key.startswith("__") and key.islower() and isinstance(value, Entry)
    ]
    res = ColourWriter(prefix)
    res.add_entries(variables)

    return res


if __name__ == '__main__':
    x = get_colour_writer("test")
    print(x)

    # from xddtools.base import ProxyWriter
    #
    # c1 = Colour(darkness=0.5)
    # c2 = Colour(darkness=0.5, shared_id=c1)
    # c3 = Colour(darkness=0.5, shared_id=c2)
    # c4 = Colour(darkness=0.5, shared_id=c1)
    # c5 = Colour(darkness=0.5)
    # c6 = Colour(darkness=0.5)
    # c7 = Colour(darkness=0.5)
    # c = get_colour_writer("test")
    # p = ProxyWriter([c])
    # p.add_entry(c3)
    # p.add_entry(c4)
    # p.add_entry(c5)
    # p.add_entry(c6)
    # p.add_entry(c7)
    # p.add_entry(c1)
    # p.add_entry(c2)
    #
    # p.export()

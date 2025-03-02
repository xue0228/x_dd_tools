import types


class AutoNameBase:
    def new_buff(self) -> str: ...

    def last_buff(self) -> str: ...

    def index_buff(self, idx: int) -> str: ...

    def new_effect(self) -> str: ...

    def last_effect(self) -> str: ...

    def index_effect(self, idx: int) -> str: ...

    def new_colour(self) -> str: ...

    def last_colour(self) -> str: ...

    def index_colour(self, idx: int) -> str: ...

    def new_skill(self) -> str: ...

    def last_skill(self) -> str: ...

    def index_skill(self, idx: int) -> str: ...

    def new_anim(self) -> str: ...

    def last_anim(self) -> str: ...

    def index_anim(self, idx: int) -> str: ...

    def new_rarity(self) -> str: ...

    def last_rarity(self) -> str: ...

    def index_rarity(self, idx: int) -> str: ...

    def new_trinket(self) -> str: ...

    def last_trinket(self) -> str: ...

    def index_trinket(self, idx: int) -> str: ...

    def new_item(self) -> str: ...

    def last_item(self) -> str: ...

    def index_item(self, idx: int) -> str: ...

    def new_loot(self) -> str: ...

    def last_loot(self) -> str: ...

    def index_loot(self, idx: int) -> str: ...

    def new_quirk(self) -> str: ...

    def last_quirk(self) -> str: ...

    def index_quirk(self, idx: int) -> str: ...

    def new_camping_skill(self) -> str: ...

    def last_camping_skill(self) -> str: ...

    def index_camping_skill(self, idx: int) -> str: ...

    def new_trait(self) -> str: ...

    def last_trait(self) -> str: ...

    def index_trait(self, idx: int) -> str: ...

    def new_(self) -> str: ...

    def last_(self) -> str: ...

    def index_(self, idx: int) -> str: ...


class AutoName(AutoNameBase):
    def __init__(
            self,
            prefix: str,
    ):
        self._prefix = prefix
        self._data = {}
        self._categories = (
            "buff", "effect", "colour", "skill",
            "anim", "rarity", "trinket", "item",
            "loot", "quirk", "camping_skill", "trait"
        )
        for category in self._categories:
            # 动态生成并绑定方法
            setattr(self, f"new_{category}", types.MethodType(self._make_new_method(category), self))
            setattr(self, f"last_{category}", types.MethodType(self._make_last_method(category), self))
            setattr(self, f"index_{category}", types.MethodType(self._make_index_method(category), self))

    @staticmethod
    def _make_new_method(category):
        def new_method(self):
            return self._add_new_name(category)

        return new_method

    @staticmethod
    def _make_last_method(category):
        def last_method(self):
            return self._get_name_by_index(category)

        return last_method

    @staticmethod
    def _make_index_method(category):
        def index_method(self, idx: int):
            return self._get_name_by_index(category, idx)

        return index_method

    def __len__(self):
        res = sum([value for value in self._data.values()])
        return res + len(self._data)

    def _add_new_name(self, category: str):
        if category not in self._data:
            self._data[category] = 0
            return "_".join([self._prefix, category, str(0)])
        self._data[category] += 1
        return "_".join([self._prefix, category, str(self._data[category])])

    def _get_name_by_index(self, category: str, idx: int = -1):
        if category not in self._data:
            raise ValueError("Category not found")
        if idx < 0:
            idx = self._data[category] + 1 + idx
            if idx < 0:
                raise ValueError("Index out of range")
        else:
            if idx > self._data[category]:
                raise ValueError("Index out of range")
        return "_".join([self._prefix, category, str(idx)])


if __name__ == '__main__':
    a = AutoName("xhunter")
    print(a.new_buff())
    print(a.new_buff())
    print(a.new_buff())
    print(a.last_buff())
    print(len(a))

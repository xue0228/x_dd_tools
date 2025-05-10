import os
import types


class AutoName:
    _instances = {}
    _default_prefix = os.getenv('AUTO_NAME_PREFIX', 'default')  # 默认从环境变量中获取前缀

    def __new__(cls, prefix: str = None):
        if prefix is None:
            prefix = cls._default_prefix
        if prefix not in cls._instances:
            instance = super(AutoName, cls).__new__(cls)
            instance._prefix = prefix
            # 初始化数据存储
            instance._data = {category: -1 for category in (
                "buff", "effect", "colour", "skill",
                "anim", "rarity", "trinket", "item",
                "loot_table", "quirk", "camping_skill", "trait",
                "mode", "sub_type", "set", "project",
                "actor_dot", "hero", "loot_monster", "party_name"
            )}

            # 动态生成并绑定方法
            for category in instance._data.keys():
                for operation in ('new', 'last', 'index'):
                    method_name = f"{operation}_{category}"
                    method = cls._make_method(operation, category)
                    bound_method = types.MethodType(method, instance)
                    setattr(instance, method_name, bound_method)
            cls._instances[prefix] = instance
        return cls._instances[prefix]

    @staticmethod
    def _make_method(operation, category):
        def new_method(self, idx=None):
            if operation == 'new':
                self._data[category] += 1
                return f"{self._prefix}_{category}_{self._data[category]}"
            elif operation == 'last':
                if self._data[category] < 0:
                    raise ValueError(f"No items available in category {category}")
                return f"{self._prefix}_{category}_{self._data[category]}"
            elif operation == 'index':
                if idx is None or idx > self._data[category] or idx < 0:
                    raise ValueError(f"Index out of range for category {category}")
                return f"{self._prefix}_{category}_{idx}"

        return new_method

    def __len__(self):
        return sum([v for v in self._data.values() if v > 0])

    @classmethod
    def set_default_prefix(cls, prefix: str):
        instance = cls._instances.get(cls._default_prefix, None)
        if instance is not None and len(instance) > 0:
            raise ValueError("Cannot change default prefix when there are items in the default category")
        cls._default_prefix = prefix

    def __repr__(self):
        return repr(self._data)


if __name__ == '__main__':
    import os

    # 设置环境变量（仅用于演示）
    os.environ['AUTO_NAME_PREFIX'] = 'env_prefix'

    # 创建默认实例
    default_instance = AutoName()
    print(default_instance.new_buff())  # 使用默认前缀
    print(default_instance.new_buff())
    print(default_instance.new_buff())
    print(default_instance.last_buff())

    # 创建具有特定前缀的实例
    specific_instance = AutoName("specific_prefix")
    print(specific_instance.new_buff())  # 使用不同的前缀
    print(specific_instance.new_buff())
    print(specific_instance.new_buff())
    print(specific_instance.last_buff())

    # 更改默认前缀
    AutoName.set_default_prefix("new_default_prefix")
    changed_default_instance = AutoName()
    print(changed_default_instance.new_buff())  # 使用新的默认前缀
    print(changed_default_instance.new_buff())
    print(changed_default_instance.new_buff())
    print(changed_default_instance.last_buff())

    # 验证单个前缀的实例是否相同
    another_default_instance = AutoName()
    print(changed_default_instance is another_default_instance)  # 应该输出 True

    # 验证不同前缀的实例是否不同
    print(default_instance is specific_instance)  # 应该输出 False

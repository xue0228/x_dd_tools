from typing import Union, Iterable, List


class Target:
    def __init__(
            self,
            target: Union[Iterable[int], int, str, None],
            is_group: bool = False,
            is_friend: bool = False,
            is_random: bool = False,
            is_launch: bool = False,
    ):
        self._target = self.init_target(target)
        if is_group and is_random:
            raise ValueError("is_group and is_random cannot be True at the same time")
        if is_launch and (is_friend or is_group or is_random):
            raise ValueError("if is_launch is true,others must all be false")
        self._is_group = is_group
        self._is_friend = is_friend
        self._is_random = is_random
        self._is_launch = is_launch
        self._target = sorted(self._target, reverse=self._is_launch)

    def is_friend(self) -> bool:
        return self._is_friend

    @staticmethod
    def init_target(target: Union[Iterable[int], int, str, None]) -> List[int]:
        if isinstance(target, int):
            if 1 <= target <= 4:
                target = [target]
            else:
                target = str(target)
                tem = []
                for num in target:
                    if not num.isdigit():
                        raise ValueError(f"Invalid target: {target}")
                    tem.append(int(num))
                target = tem

        elif target is None:
            target = []

        elif isinstance(target, str):
            tem = []
            for num in target:
                if not num.isdigit():
                    raise ValueError(f"Invalid target: {target}")
                tem.append(int(num))
            target = tem

        elif isinstance(target, Iterable):
            tem = []
            for num in target:
                if not isinstance(num, int):
                    raise ValueError(f"Invalid target: {target}")
                tem.append(num)
            target = tem

        else:
            raise TypeError(f"Invalid target: {target}")

        return list(set(target))

    def __str__(self):
        if len(self._target) == 0:
            return ""

        res = "".join([str(num) for num in self._target])

        if self._is_launch:
            return res

        if self._is_group:
            res = "~" + res
        elif self._is_random:
            res = "?" + res

        if self._is_friend:
            res = "@" + res

        return res


SELF = Target(None)

ALL_FRIEND = Target("1234", is_group=True, is_friend=True)
ALL_ENEMY = Target("1234", is_group=True, is_friend=False)

ALL_RANDOM_FRIEND = Target("1234", is_random=True, is_friend=True)
ALL_RANDOM_ENEMY = Target("1234", is_random=True, is_friend=False)

ENEMY_GROUP_12 = Target("12", is_group=True)
ENEMY_GROUP_23 = Target("23", is_group=True)
ENEMY_GROUP_34 = Target("34", is_group=True)
ENEMY_GROUP_14 = Target("14", is_group=True)

ENEMY_GROUP_234 = Target("234", is_group=True)
ENEMY_GROUP_134 = Target("134", is_group=True)
ENEMY_GROUP_124 = Target("124", is_group=True)
ENEMY_GROUP_123 = Target("123", is_group=True)

LAUNCH_1 = Target("1", is_launch=True)
LAUNCH_2 = Target("2", is_launch=True)
LAUNCH_3 = Target("3", is_launch=True)
LAUNCH_4 = Target("4", is_launch=True)
LAUNCH_12 = Target("12", is_launch=True)
LAUNCH_13 = Target("13", is_launch=True)
LAUNCH_14 = Target("14", is_launch=True)
LAUNCH_23 = Target("23", is_launch=True)
LAUNCH_24 = Target("24", is_launch=True)
LAUNCH_34 = Target("34", is_launch=True)
LAUNCH_123 = Target("123", is_launch=True)
LAUNCH_124 = Target("124", is_launch=True)
LAUNCH_134 = Target("134", is_launch=True)
LAUNCH_234 = Target("234", is_launch=True)
LAUNCH_ANY = Target("4321", is_launch=True)

if __name__ == '__main__':
    t = Target("122", is_friend=True)
    print(f"{t}")

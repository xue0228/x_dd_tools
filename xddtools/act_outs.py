from typing import Optional, Iterable, Union, Tuple, List, Any, Dict

from xddtools.base import BaseJsonData, BaseLocalization
from xddtools.effects import Effect
from xddtools.enums import CombatStartTurnActOuts, ReactionActOuts


class CombatStartTurn(BaseLocalization, BaseJsonData):
    def __init__(
            self,
            name: CombatStartTurnActOuts,
            chance: int,
            number_value: float = 0.0,
            string_value: Union[Effect, str] = "",
            raid_limit: Optional[int] = None,
            valid_hero_class_ids: Optional[Iterable[str]] = None,
            localization: Union[Tuple[str, ...], str, None] = None
    ):
        self.name = name
        self.chance = chance
        self.number_value = number_value
        self.string_value = string_value
        self.raid_limit = raid_limit
        self.valid_hero_class_ids = valid_hero_class_ids
        super().__init__(
            name="",
            localization=localization,
            entry_id_prefix=f"str_{name.value}_"
        )

    @property
    def entries(self) -> Tuple[Tuple[str, str]]:
        res = list(super().entries)
        if self.name == CombatStartTurnActOuts.CHANGE_POS:
            if self.number_value > 0:
                res = [(item[0].replace("str_change_pos_", "str_change_pos_back_"), item[1]) for item in res]
            elif self.number_value < 0:
                res = [(item[0].replace("str_change_pos_", "str_change_pos_fwd_"), item[1]) for item in res]
            else:
                tem = res
                res = [(item[0].replace("str_change_pos_", "str_change_pos_back_"), item[1]) for item in res]
                res.extend(
                    [(item[0].replace("str_change_pos_", "str_change_pos_fwd_"), item[1]) for item in tem]
                )
        return tuple(res)

    def dict(self) -> Dict:
        res = {
            "id": self.name.value,
            "data": {
                "number_value": self.number_value,
                "string_value": self.string_value.id
                if isinstance(self.string_value, Effect) else self.string_value,
            },
            "chance": self.chance,
        }
        if self.raid_limit is not None:
            res["raid_limit"] = self.raid_limit
        if self.valid_hero_class_ids is not None:
            res["valid_hero_class_ids"] = [hero for hero in self.valid_hero_class_ids]
        return res


class Reaction(BaseLocalization, BaseJsonData):
    def __init__(
            self,
            name: ReactionActOuts,
            chance: float,
            effect: Union[Effect, str],
            localization: Union[Tuple[str, ...], str, None] = None
    ):
        self.name = name
        self.chance = chance
        self.effect = effect
        super().__init__(
            name="",
            localization=localization,
            entry_id_prefix=f"str_{name.value}_"
        )

    def dict(self) -> Dict:
        res = {
            "id": self.name.value,
            "data": {
                "effect": self.effect.id
                if isinstance(self.effect, Effect) else self.effect,
            },
            "chance": self.chance,
        }
        return res


# class CombatStartTurnActOut(BaseJsonData):
#     def __init__(
#             self,
#             quirk_id: Union[Any, str],
#             act_outs: Optional[Iterable[CombatStartTurn]] = None
#     ):
#         self._quirk_id: str = quirk_id.id if not isinstance(quirk_id, str) else quirk_id
#         self._act_outs: List[CombatStartTurn, ...] = []
#         if act_outs is not None:
#             for act_out in act_outs:
#                 self.add_act_out(act_out)
#
#     def add_act_out(self, act_out: CombatStartTurn):
#         self._act_outs.append(act_out)
#
#     @staticmethod
#     def _single_dict(act_out: CombatStartTurn):
#         res = {
#             "id": act_out.id,
#             "_data": {
#                 "number_value": act_out.number_value,
#                 "string_value": act_out.string_value.id
#                 if isinstance(act_out.string_value, Effect) else act_out.string_value,
#             },
#             "chance": act_out.chance,
#         }
#         if act_out.raid_limit is not None:
#             res["raid_limit"] = act_out.raid_limit
#         if act_out.valid_hero_class_ids is not None:
#             res["valid_hero_class_ids"] = [hero for hero in act_out.valid_hero_class_ids]
#         return res
#
#     @property
#     def effects(self):
#         return [act_out.string_value for act_out in self._act_outs if isinstance(act_out.string_value, Effect)]
#
#     def dict(self):
#         res = [self._single_dict(act_out) for act_out in self._act_outs]
#         return {
#             "combat_start_turn_act_outs": res
#         }
#
#     @property
#     def entries(self) -> Tuple[Tuple[str, str]]:
#         res = []
#         for act_out in self._act_outs:
#             tem = [(item[0] + self._quirk_id, item[1]) for item in act_out.entries]
#             res.extend(tem)
#         return tuple(res)
#
#
# class ReactionActOut(BaseJsonData):
#     def __init__(
#             self,
#             quirk_id: Union[Any, str],
#             act_outs: Optional[Iterable[Reaction]] = None
#     ):
#         self._quirk_id: str = quirk_id.id if not isinstance(quirk_id, str) else quirk_id
#         self._act_outs: List[Reaction, ...] = []
#         if act_outs is not None:
#             for act_out in act_outs:
#                 self.add_act_out(act_out)
#
#     def add_act_out(self, act_out: Reaction):
#         self._act_outs.append(act_out)
#
#     @staticmethod
#     def _single_dict(act_out: Reaction):
#         res = {
#             "id": act_out.id,
#             "_data": {
#                 "effect": act_out.effect.id
#                 if isinstance(act_out.effect, Effect) else act_out.effect,
#             },
#             "chance": act_out.chance,
#         }
#         return res
#
#     @property
#     def effects(self):
#         return [act_out.effect for act_out in self._act_outs if isinstance(act_out.effect, Effect)]
#
#     def dict(self):
#         res = [self._single_dict(act_out) for act_out in self._act_outs]
#         return {
#             "reaction_act_outs": res
#         }
#
#     @property
#     def entries(self) -> Tuple[Tuple[str, str]]:
#         res = []
#         for act_out in self._act_outs:
#             tem = [(item[0] + self._quirk_id, item[1]) for item in act_out.entries]
#             res.extend(tem)
#         return tuple(res)

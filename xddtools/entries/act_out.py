from typing import Union, Sequence, Optional, List, Tuple

from pydantic import BaseModel, ConfigDict

from xddtools.base import EffectEntry, JsonData, HeroEntry, get_entry_id, Entry
from xddtools.enum.act_out import CombatStartTurnActOuts, ReactionActOuts


class CombatStartTurn(JsonData, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    name: CombatStartTurnActOuts
    chance: int
    number_value: float = 0.0
    string_value: Union[EffectEntry, str] = ""
    raid_limit: Optional[int] = None
    valid_hero_class_ids: Optional[Sequence[Union[HeroEntry, str]]] = None
    act_out_barks: Union[Sequence[str], str, None] = None

    def get_dict(self) -> dict:
        res = {
            "id": self.name.value,
            "data": {
                "number_value": self.number_value,
                "string_value": get_entry_id(self.string_value),
            },
            "chance": self.chance,
        }
        if self.raid_limit is not None:
            res["raid_limit"] = self.raid_limit
        if self.valid_hero_class_ids is not None:
            res["valid_hero_class_ids"] = [get_entry_id(hero) for hero in self.valid_hero_class_ids]
        return res

    def get_localization_entries(self, entry_id: Union[Entry, str]) -> List[Tuple[str, str]]:
        entry_id = get_entry_id(entry_id)
        res = []
        if self.act_out_barks is None:
            return res
        if isinstance(self.act_out_barks, str):
            barks = [self.act_out_barks]
        else:
            barks = self.act_out_barks
        for bark in barks:
            if self.name == CombatStartTurnActOuts.CHANGE_POS:
                if self.number_value > 0:
                    res.append((f"str_change_pos_back_{entry_id}", bark))
                elif self.number_value < 0:
                    res.append((f"str_change_pos_fwd_{entry_id}", bark))
                else:
                    res.append((f"str_change_pos_back_{entry_id}", bark))
                    res.append((f"str_change_pos_fwd_{entry_id}", bark))
            else:
                res.append((f"str_{self.name.value}_{entry_id}", bark))
        return res


class Reaction(JsonData, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    name: ReactionActOuts
    chance: float
    effect: Union[EffectEntry, str]
    act_out_barks: Union[Sequence[str], str, None] = None

    def get_dict(self) -> dict:
        res = {
            "id": self.name.value,
            "data": {
                "effect": get_entry_id(self.effect)
            },
            "chance": self.chance,
        }
        return res

    def get_localization_entries(self, entry_id: Union[Entry, str]) -> List[Tuple[str, str]]:
        entry_id = get_entry_id(entry_id)
        res = []
        if self.act_out_barks is None:
            return res
        if isinstance(self.act_out_barks, str):
            barks = [self.act_out_barks]
        else:
            barks = self.act_out_barks
        for bark in barks:
            res.append((f"str_{self.name.value}_{entry_id}", bark))
        return res

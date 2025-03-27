from typing import Sequence, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from xddtools.name import AutoName
from xddtools.base import JsonData, QuirkEntry, BuffEntry, get_entry_id
from xddtools.entries.act_out import CombatStartTurn, Reaction
from xddtools.enum.quirk import CurioTag


class Trait(JsonData, QuirkEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    is_generated: bool = False
    is_virtue: bool = True
    curio_tag: CurioTag = CurioTag.NONE
    curio_tag_chance: float = 0.5
    keep_loot: bool = False
    generate_chance_modifier: float = 0.0
    buff_ids: Optional[Sequence[Union[BuffEntry, str]]] = None
    combat_start_turn_act_outs: Optional[Sequence[CombatStartTurn]] = None
    reaction_act_outs: Optional[Sequence[Reaction]] = None

    str_trait_name: Optional[str] = None
    str_trait_description: Optional[str] = None
    str_trait_barks: Union[Sequence[str], str, None] = None
    entry_id: str = Field(default_factory=lambda x: AutoName().new_trait(), frozen=True)

    def get_dict(self) -> dict:
        res = {
            "id": self.id(),
            "is_generated": self.is_generated,
            "overstress_type": "virtue" if self.is_virtue else "affliction",
            "curio_tag": self.curio_tag.value,
            "curio_tag_chance": self.curio_tag_chance,
            "keep_loot": self.keep_loot,
            "generate_chance_modifier": self.generate_chance_modifier,
        }
        if self.buff_ids is not None:
            res["buff_ids"] = [get_entry_id(buff) for buff in self.buff_ids]

        if self.combat_start_turn_act_outs is not None:
            res["combat_start_turn_act_outs"] = [act_out.get_dict() for act_out in self.combat_start_turn_act_outs]
        if self.reaction_act_outs is not None:
            res["reaction_act_outs"] = [act_out.get_dict() for act_out in self.reaction_act_outs]

        return res

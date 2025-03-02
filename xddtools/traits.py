from typing import Optional, Iterable, Union, Tuple

from xddtools.act_outs import Reaction, CombatStartTurn
from xddtools.base import BaseJsonData, BaseLocalization
from xddtools.buffs import Buff
from xddtools.enums import CurioTag


class Trait(BaseJsonData, BaseLocalization):
    def __init__(
            self,
            trait_name: str,
            is_generated: bool = False,
            is_virtue: bool = True,
            curio_tag: CurioTag = CurioTag.NONE,
            curio_tag_chance: float = 0.5,
            keep_loot: bool = False,
            generate_chance_modifier: float = 0.0,
            buff_ids: Optional[Iterable[Union[Buff, str]]] = None,
            combat_start_turn_act_outs: Optional[Iterable[CombatStartTurn]] = None,
            reaction_act_outs: Optional[Iterable[Reaction]] = None,
            localization: Union[Tuple[str, ...], str, None] = None,
    ):
        self.is_generated = is_generated
        self.is_virtue = is_virtue
        self.curio_tag = curio_tag
        self.curio_tag_chance = curio_tag_chance
        self.keep_loot = keep_loot
        self.generate_chance_modifier = generate_chance_modifier
        self.buff_ids = buff_ids
        self.combat_start_turn_act_outs = combat_start_turn_act_outs
        self.reaction_act_outs = reaction_act_outs
        overstress = "virtue" if self.is_virtue else "affliction"
        overstress_bark = "virtued" if self.is_virtue else "afflicted"
        super().__init__(
            name=trait_name,
            localization=localization,
            entry_id_prefix=(
                f"str_{overstress}_name_",
                f"str_{overstress}_description_",
                f"str_{overstress_bark}_",
            ),
        )

    def dict(self) -> dict:
        res = {
            "id": self.id,
            "is_generated": self.is_generated,
            "overstress_type": "virtue" if self.is_virtue else "affliction",
            "curio_tag": self.curio_tag.value,
            "curio_tag_chance": self.curio_tag_chance,
            "keep_loot": self.keep_loot,
            "generate_chance_modifier": self.generate_chance_modifier,
        }
        if self.buff_ids is not None:
            res["buff_ids"] = [buff.id if isinstance(buff, Buff) else buff
                               for buff in self.buff_ids]

        if self.combat_start_turn_act_outs is not None:
            res["combat_start_turn_act_outs"] = [act_out.dict() for act_out in self.combat_start_turn_act_outs]
        if self.reaction_act_outs is not None:
            res["reaction_act_outs"] = [act_out.dict() for act_out in self.reaction_act_outs]

        return res

    @property
    def entries(self) -> Tuple[Tuple[str, str]]:
        entries = list(super().entries)
        if self.combat_start_turn_act_outs is not None:
            for act_out in self.combat_start_turn_act_outs:
                tem = [(item[0] + self.id, item[1]) for item in act_out.entries]
                entries.extend(tem)
        if self.reaction_act_outs is not None:
            for act_out in self.reaction_act_outs:
                tem = [(item[0] + self.id, item[1]) for item in act_out.entries]
                entries.extend(tem)
        return tuple(entries)

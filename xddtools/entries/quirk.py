from typing import Union, Sequence, Optional, List

from pydantic import ConfigDict, BaseModel, Field, field_validator

from xddtools.base import ItemEntry, QuirkEntry, EffectEntry, JsonData, BuffEntry, get_entry_id, LocalizationEntry
from xddtools.entries.act_out import Reaction, CombatStartTurn
from xddtools.entries.localization import Localization
from xddtools.enum.buff_rule import ItemType
from xddtools.enum.quirk import QuirkClassification, CurioTag, QuirkTag
from xddtools.name import AutoName
from xddtools.utils import is_image


class UseItemChange(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    item_type: ItemType
    item_id: Union[ItemEntry, str]
    change_quirk_class_id: Union[QuirkEntry, str]
    change_quirk_bark: Union[Sequence[str], str, None] = None


class UseItemDungeonEffect(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    item_type: ItemType
    item_id: Union[ItemEntry, str]
    effect: Union[EffectEntry, str]


class Quirk(JsonData, QuirkEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    tray_quirk_image: Optional[str] = None
    analytics_enabled: bool = False
    show_explicit_buff_description: bool = False
    show_flavor_description: bool = True
    is_explicit_buff_description_valid_in_character_sheet: bool = True
    is_flavor_description_valid_in_tray_icon: bool = True
    show_explicit_curio_tag_description: bool = False
    random_chance: float = 1
    is_positive: bool = True
    is_disease: bool = False
    classification: QuirkClassification = QuirkClassification.MENTAL
    incompatible_quirks: Optional[Sequence[Union[QuirkEntry, str]]] = None
    curio_tag: Union[str, CurioTag, None] = None
    curio_tag_chance: float = 0.0
    keep_loot: bool = False
    buffs: Optional[Sequence[Union[BuffEntry, str]]] = None
    tags: Optional[Sequence[Union[QuirkTag, str]]] = None
    evolution_duration_min: Optional[int] = None
    evolution_duration_max: Optional[int] = None
    evolution_town_progression_duration_change: Optional[int] = None
    evolution_class_id: Union[QuirkEntry, str, None] = None
    can_modify_in_activity: bool = True
    can_remove_with_camping_skill: bool = True
    can_be_replaced_by_new_quirk: bool = True
    required_plot_quests_to_modify: Optional[Sequence[str]] = None
    required_plot_quests_to_embark: Optional[Sequence[str]] = None
    roster_limit: Optional[int] = None
    slot_size: int = 1
    use_item_changes: Optional[Sequence[UseItemChange]] = None
    use_item_dungeon_effects: Optional[Sequence[UseItemDungeonEffect]] = None
    contagious_class_id: Union[QuirkEntry, str, None] = None
    has_fx: bool = False
    combat_start_turn_act_outs: Optional[Sequence[CombatStartTurn]] = None
    reaction_act_outs: Optional[Sequence[Reaction]] = None

    str_quirk_name: Optional[str] = None
    str_quirk_description: Optional[str] = None
    str_ui_entering: Optional[str] = None
    evolution_quirk_bark: Union[Sequence[str], str, None] = None

    entry_id: str = Field(default_factory=lambda x: AutoName().new_quirk(), frozen=True)

    @field_validator("tray_quirk_image")
    @classmethod
    def _check_tray_quirk_image(cls, v: str):
        if (v is not None) and (not is_image(v)):
            raise ValueError(f"{v} is not a valid image path")
        return v

    def get_dict(self) -> dict:
        res = {
            "id": self.id(),
            "show_explicit_buff_description": self.show_explicit_buff_description,
            "show_flavor_description": self.show_flavor_description,
            "is_explicit_buff_description_valid_in_character_sheet":
                self.is_explicit_buff_description_valid_in_character_sheet,
            "is_flavor_description_valid_in_tray_icon": self.is_flavor_description_valid_in_tray_icon,
            "show_explicit_curio_tag_description": self.show_explicit_curio_tag_description,
        }
        if self.analytics_enabled:
            res["analytics_enabled"] = self.analytics_enabled

        if self.random_chance < 0:
            raise ValueError("random_chance must be >= 0")

        res["random_chance"] = self.random_chance
        res["is_positive"] = self.is_positive
        res["is_disease"] = self.is_disease
        res["classification"] = self.classification.value

        if self.incompatible_quirks is None:
            incompatible_quirks = []
        else:
            incompatible_quirks = [get_entry_id(quirk)
                                   for quirk in self.incompatible_quirks]
        res["incompatible_quirks"] = incompatible_quirks

        if self.curio_tag is None:
            curio_tag = ""
        else:
            curio_tag = get_entry_id(self.curio_tag)
        res["curio_tag"] = curio_tag

        if 0 <= self.curio_tag_chance <= 1:
            res["curio_tag_chance"] = self.curio_tag_chance
        else:
            raise ValueError("curio_tag_chance must be in range [0, 1]")

        res["keep_loot"] = self.keep_loot

        buffs = []
        if self.buffs is not None:
            for buff in self.buffs:
                buffs.append(get_entry_id(buff))
        res["buffs"] = buffs

        tags = []
        if self.tags is not None:
            for tag in self.tags:
                tags.append(get_entry_id(tag))
        res["tags"] = tags

        if self.evolution_duration_min is not None:
            res["evolution_duration_min"] = self.evolution_duration_min
        if self.evolution_duration_max is not None:
            res["evolution_duration_max"] = self.evolution_duration_max
        if self.evolution_town_progression_duration_change is not None:
            res["evolution_town_progression_duration_change"] = self.evolution_town_progression_duration_change
        if self.evolution_class_id is not None:
            res["evolution_class_id"] = get_entry_id(self.evolution_class_id)

        res["can_modify_in_activity"] = self.can_modify_in_activity
        res["can_remove_with_camping_skill"] = self.can_remove_with_camping_skill
        res["can_be_replaced_by_new_quirk"] = self.can_be_replaced_by_new_quirk

        if self.required_plot_quests_to_modify is not None:
            required_plot_quests_to_modify = [item for item in self.required_plot_quests_to_modify]
            res["required_plot_quests_to_modify"] = required_plot_quests_to_modify

        if self.required_plot_quests_to_embark is not None:
            required_plot_quests_to_embark = [item for item in self.required_plot_quests_to_embark]
            res["required_plot_quests_to_embark"] = required_plot_quests_to_embark

        if self.roster_limit is not None:
            res["roster_limit"] = self.roster_limit

        res["slot_size"] = self.slot_size

        if self.use_item_changes is not None:
            use_item_changes = []
            for item in self.use_item_changes:
                use_item_changes.append({
                    "item_type": item.item_type.value,
                    "item_id": get_entry_id(item.item_id),
                    "change_quirk_class_id": get_entry_id(item.change_quirk_class_id)
                })
            res["use_item_changes"] = use_item_changes

        if self.use_item_dungeon_effects is not None:
            use_item_dungeon_effects = []
            for item in self.use_item_dungeon_effects:
                use_item_dungeon_effects.append({
                    "item_type": item.item_type.value,
                    "item_id": get_entry_id(item.item_id),
                    "effect": get_entry_id(item.effect)
                })
            res["use_item_dungeon_effects"] = use_item_dungeon_effects

        if self.contagious_class_id is not None:
            res["contagious_class_id"] = get_entry_id(self.contagious_class_id)

        res["has_fx"] = self.has_fx

        if self.combat_start_turn_act_outs is not None:
            res["combat_start_turn_act_outs"] = [act_out.get_dict() for act_out in self.combat_start_turn_act_outs]
        if self.reaction_act_outs is not None:
            res["reaction_act_outs"] = [act_out.get_dict() for act_out in self.reaction_act_outs]

        return res


def get_quirk_transition_a_to_b_localization_entries(
        a: Union[QuirkEntry, str],
        b: Union[QuirkEntry, str],
        bark_texts: Union[Sequence[str], str]
) -> List[LocalizationEntry]:
    if isinstance(bark_texts, str):
        bark_texts = [bark_texts]
    res = []
    for bark_text in bark_texts:
        res.append(Localization(
            entry_id=f"quirk_transition_{get_entry_id(a)}_to_{get_entry_id(b)}",
            text=bark_text
        ))
    return res

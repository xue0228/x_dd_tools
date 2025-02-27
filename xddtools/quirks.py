import os
from dataclasses import dataclass
from typing import Optional, Iterable, Union, Any, Tuple, Dict

from xddtools.act_outs import CombatStartTurn, Reaction
from xddtools.base import BaseJsonData, BaseLocalization
from xddtools.buffs import Buff
from xddtools.effects import Effect
from xddtools.enums import QuirkClassification, CurioTag, QuirkTag, ItemType
from xddtools.items import Item
from xddtools.path import QUIRK_IMAGE_SAVE_DIR
from xddtools.utils import is_image, resize_image_keep_ratio


@dataclass(frozen=True)
class UseItemChange:
    item_type: ItemType
    item_id: Union[Item, str]
    change_quirk_class_id: Union[Any, str]


@dataclass(frozen=True)
class UseItemDungeonEffect:
    item_type: ItemType
    item_id: Union[Item, str]
    effect: Union[Effect, str]


class Quirk(BaseJsonData, BaseLocalization):
    def __init__(
            self,
            quirk_name: Optional[str] = None,
            image_path: Optional[str] = None,
            analytics_enabled: bool = False,
            show_explicit_buff_description: bool = False,
            show_flavor_description: bool = True,
            is_explicit_buff_description_valid_in_character_sheet: bool = False,
            is_flavor_description_valid_in_tray_icon: bool = False,
            show_explicit_curio_tag_description: bool = False,
            random_chance: float = 1,
            is_positive: bool = True,
            is_disease: bool = False,
            classification: QuirkClassification = QuirkClassification.MENTAL,
            incompatible_quirks: Optional[Iterable[Union[str, Any]]] = None,
            curio_tag: Union[str, CurioTag, None] = None,
            curio_tag_chance: float = 0.0,
            keep_loot: bool = False,
            buffs: Optional[Iterable[Union[Buff, str]]] = None,
            tags: Optional[Iterable[Union[QuirkTag, str]]] = None,
            evolution_duration_min: Optional[int] = None,
            evolution_duration_max: Optional[int] = None,
            evolution_town_progression_duration_change: Optional[int] = None,
            evolution_class_id: Union[str, Any, None] = None,
            can_modify_in_activity: bool = True,
            can_remove_with_camping_skill: bool = True,
            can_be_replaced_by_new_quirk: bool = True,
            required_plot_quests_to_modify: Optional[Iterable[str]] = None,
            required_plot_quests_to_embark: Optional[Iterable[str]] = None,
            roster_limit: Optional[int] = None,
            slot_size: int = 1,
            use_item_changes: Optional[Iterable[UseItemChange]] = None,
            use_item_dungeon_effects: Optional[Iterable[UseItemDungeonEffect]] = None,
            contagious_class_id: Union[str, Any, None] = None,
            has_fx: bool = False,
            combat_start_turn_act_outs: Optional[Iterable[CombatStartTurn]] = None,
            reaction_act_outs: Optional[Iterable[Reaction]] = None,
            localization: Union[Tuple[str, ...], str, None] = None,
    ):
        if (image_path is not None) and (not is_image(image_path)):
            raise ValueError(f"{image_path} is not a image")
        self.image_path = image_path

        self.analytics_enabled = analytics_enabled
        self.show_explicit_buff_description = show_explicit_buff_description
        self.show_flavor_description = show_flavor_description
        self.is_explicit_buff_description_valid_in_character_sheet = \
            is_explicit_buff_description_valid_in_character_sheet
        self.is_flavor_description_valid_in_tray_icon = is_flavor_description_valid_in_tray_icon
        self.show_explicit_curio_tag_description = show_explicit_curio_tag_description
        self.random_chance = random_chance
        self.is_positive = is_positive
        self.is_disease = is_disease
        self.classification = classification
        self.incompatible_quirks = incompatible_quirks
        self.curio_tag = curio_tag
        self.curio_tag_chance = curio_tag_chance
        self.keep_loot = keep_loot
        self.buffs = buffs
        self.tags = tags
        self.evolution_duration_min = evolution_duration_min
        self.evolution_duration_max = evolution_duration_max
        self.evolution_town_progression_duration_change = evolution_town_progression_duration_change
        self.evolution_class_id = evolution_class_id
        self.can_modify_in_activity = can_modify_in_activity
        self.can_remove_with_camping_skill = can_remove_with_camping_skill
        self.can_be_replaced_by_new_quirk = can_be_replaced_by_new_quirk
        self.required_plot_quests_to_modify = required_plot_quests_to_modify
        self.required_plot_quests_to_embark = required_plot_quests_to_embark
        self.roster_limit = roster_limit
        self.slot_size = slot_size
        self.use_item_changes = use_item_changes
        self.use_item_dungeon_effects = use_item_dungeon_effects
        self.contagious_class_id = contagious_class_id
        self.has_fx = has_fx
        self.combat_start_turn_act_outs = combat_start_turn_act_outs
        self.reaction_act_outs = reaction_act_outs
        super().__init__(
            name=quirk_name,
            localization=localization,
            entry_id_prefix=(
                "str_quirk_name_",
                "str_quirk_description_",
                "str_ui_entering_"
            )
        )

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

    def dict(self) -> Dict:
        res = {
            "id": self.id,
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
            incompatible_quirks = [quirk.id if isinstance(quirk, Quirk) else quirk
                                   for quirk in self.incompatible_quirks]
        res["incompatible_quirks"] = incompatible_quirks

        if self.curio_tag is None:
            curio_tag = ""
        else:
            curio_tag = self.curio_tag.value if isinstance(self.curio_tag, CurioTag) else self.curio_tag
        res["curio_tag"] = curio_tag

        if 0 <= self.curio_tag_chance <= 1:
            res["curio_tag_chance"] = self.curio_tag_chance
        else:
            raise ValueError("curio_tag_chance must be in range [0, 1]")

        res["keep_loot"] = self.keep_loot

        buffs = []
        if self.buffs is not None:
            for buff in self.buffs:
                if isinstance(buff, Buff):
                    buffs.append(buff.id)
                else:
                    buffs.append(buff)
        res["buffs"] = buffs

        tags = []
        if self.tags is not None:
            for tag in self.tags:
                if isinstance(tag, QuirkTag):
                    tags.append(tag.value)
                else:
                    tags.append(tag)
        res["tags"] = tags

        if self.evolution_duration_min is not None:
            res["evolution_duration_min"] = self.evolution_duration_min
        if self.evolution_duration_max is not None:
            res["evolution_duration_max"] = self.evolution_duration_max
        if self.evolution_town_progression_duration_change is not None:
            res["evolution_town_progression_duration_change"] = self.evolution_town_progression_duration_change
        if self.evolution_class_id is not None:
            class_id = self.evolution_class_id.id \
                if isinstance(self.evolution_class_id, Quirk) else self.evolution_class_id
            res["evolution_class_id"] = class_id

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
                    "item_id": item.item_id.id if isinstance(item.item_id, Item) else item.item_id,
                    "change_quirk_class_id": item.change_quirk_class_id.id
                    if isinstance(item.change_quirk_class_id, Quirk) else item.change_quirk_class_id
                })
            res["use_item_changes"] = use_item_changes

        if self.use_item_dungeon_effects is not None:
            use_item_dungeon_effects = []
            for item in self.use_item_dungeon_effects:
                use_item_dungeon_effects.append({
                    "item_type": item.item_type.value,
                    "item_id": item.item_id.id if isinstance(item.item_id, Item) else item.item_id,
                    "effect": item.effect.id
                    if isinstance(item.effect, Effect) else item.effect
                })
            res["use_item_dungeon_effects"] = use_item_dungeon_effects

        if self.contagious_class_id is not None:
            contagious_class_id = self.contagious_class_id.id \
                if isinstance(self.contagious_class_id, Quirk) else self.contagious_class_id
            res["contagious_class_id"] = contagious_class_id

        res["has_fx"] = self.has_fx

        if self.combat_start_turn_act_outs is not None:
            res["combat_start_turn_act_outs"] = [act_out.dict() for act_out in self.combat_start_turn_act_outs]
        if self.reaction_act_outs is not None:
            res["reaction_act_outs"] = [act_out.dict() for act_out in self.reaction_act_outs]

        return res

    def export_image(self, root_dir: Optional[str] = None) -> str:
        if self.image_path is None:
            raise ValueError("image_path is None")
        if root_dir is None:
            root_dir = "./"
        save_dir = os.path.join(root_dir, QUIRK_IMAGE_SAVE_DIR)
        filename = f"tray_quirk.{self.id}.png"
        file = os.path.join(save_dir, filename)
        return resize_image_keep_ratio(self.image_path, file, (24, 24))


def quirk_transition_a_to_b_localization_id(
        a: Union[Quirk, str],
        b: Union[Quirk, str],
):
    a = a.id if isinstance(a, Quirk) else a
    b = b.id if isinstance(b, Quirk) else b
    return f"quirk_transition_{a}_to_{b}"


if __name__ == '__main__':
    q = Quirk(
        quirk_name="tough",
    )
    print(q)

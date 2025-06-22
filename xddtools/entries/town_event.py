from typing import Optional, Union, Sequence

from pydantic import BaseModel, ConfigDict, field_validator, Field

from xddtools import AutoName
from xddtools.base import TownEventEntry, Entry, JsonData, get_entry_id
from xddtools.utils import is_image


class TownEventData(JsonData, BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, arbitrary_types_allowed=True)

    type: str = "bonus_recruit"
    string_data: Union[str, Entry] = ""
    number_data: float = 1.0

    def get_dict(self) -> dict:
        return {
            "type": self.type,
            "string_data": get_entry_id(self.string_data),
            "number_data": self.number_data
        }


class TownEvent(JsonData, TownEventEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    entry_id: str = Field(default_factory=lambda x: AutoName().new_town_event(), frozen=True)

    base_chance: float = 20.0
    per_not_rolled_additional_chance: float = 20.0
    cooldown: int = 0
    is_unique: bool = True
    priority: Optional[str] = "higher"
    minimum_week: int = 3
    data: Sequence[TownEventData] = Field(default_factory=list)

    town_event_image: Optional[str] = None
    town_event_title: Optional[str] = None
    town_event_description: Optional[str] = None

    @field_validator("town_event_image")
    @classmethod
    def _check_item_image(cls, v: str):
        if (v is not None) and (not is_image(v)):
            raise ValueError(f"{v} is not a valid image path")
        return v

    def get_dict(self) -> dict:
        res = {
            "id": self.id(),
            "base_chance": self.base_chance,
            "per_not_rolled_additional_chance": self.per_not_rolled_additional_chance,
            "cooldown": self.cooldown,
            "is_unique": self.is_unique,
            "requirements": {
                "minimum_week": self.minimum_week,
                "dead_heroes": 0,
                "hero_level_counts": [],
                "upgrades_purchased": [],
                "trinket_storage_count": 0
            },
            "town_ambience_paramater_ids": [],
            "tone": "neutral",
            "sprite": "",
            "sprite_attachment": "",
            "data": []
        }
        for data in self.data:
            res["data"].append(data.get_dict())
        return res

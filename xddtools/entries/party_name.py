from typing import Sequence, Union, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from xddtools.name import AutoName
from xddtools.base import PartyNameEntry, HeroEntry, JsonData, get_entry_id


class PartyName(JsonData, PartyNameEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    required_hero_class: Sequence[Union[HeroEntry, str]]
    party_name: Optional[str] = None
    entry_id: str = Field(default_factory=lambda x: AutoName().new_party_name(), frozen=True)

    @field_validator("required_hero_class")
    @classmethod
    def _check_required_hero_class(cls, v: Sequence[Union[HeroEntry, str]]):
        if len(v) > 4:
            raise ValueError("Length of required_hero_class must no larger than 4")
        return v

    def get_dict(self) -> dict:
        res = {
            "id": self.id(),
            "required_hero_class": [get_entry_id(hero) for hero in self.required_hero_class]
        }
        return res

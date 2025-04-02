from typing import Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator

from xddtools.base import JsonData, TrinketSetEntry, BuffEntry, get_entry_id, HeroEntry, TrinketRarityEntry, \
    TrinketEntry, EffectEntry
from xddtools.entries.buff_rule import HeroClass
from xddtools.enum.trinket import TrinketAwardCategory, TrinketRarityType, TrinketTriggerType, DungeonID
from xddtools.name import AutoName
from xddtools.utils import is_image


class TrinketSet(JsonData, TrinketSetEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    buffs: Optional[Sequence[Union[BuffEntry, str]]] = None
    str_inventory_set_title: Optional[str] = None
    entry_id: str = Field(default_factory=lambda x: AutoName().new_set(), frozen=True)

    def get_dict(self) -> dict:
        res = {"id": self.id()}
        buffs = [] if self.buffs is None else self.buffs
        res["buffs"] = [get_entry_id(buff) for buff in buffs]
        return res


class TrinketRarity(JsonData, TrinketRarityEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    award_category: TrinketAwardCategory = TrinketAwardCategory.UNIVERSAL
    insert_before: Union[TrinketRarityType, TrinketRarityEntry, str] = TrinketRarityType.CROW
    trinket_rarity_title: Optional[str] = None
    rarity_image: Optional[str] = None
    entry_id: str = Field(default_factory=lambda x: AutoName().new_rarity(), frozen=True)

    @field_validator("rarity_image")
    @classmethod
    def _check_rarity_image(cls, v: str):
        if (v is not None) and (not is_image(v)):
            raise ValueError("rarity_image is not a valid image path")
        return v

    def get_dict(self) -> dict:
        res = {
            "id": self.id(),
            "award_category": self.award_category.value,
            "insert_before": get_entry_id(self.insert_before)
        }
        return res


class TrinketEffect(JsonData, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    trigger: TrinketTriggerType
    effects: Sequence[Union[EffectEntry, str]]

    def get_dict(self) -> dict:
        res = {
            self.trigger.value: [get_entry_id(effect) for effect in self.effects]
        }
        return res


class Trinket(JsonData, TrinketEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    buffs: Optional[Sequence[Union[BuffEntry, str]]] = None
    hero_class_requirements: Optional[Sequence[Union[HeroEntry, HeroClass, str]]] = None
    set_id: Union[TrinketSetEntry, str, None] = None
    rarity: Union[TrinketRarityType, TrinketRarityEntry, str, None] = None
    price: Optional[int] = None
    shard: Optional[int] = None
    limit: Optional[int] = None
    origin_dungeon: Union[DungeonID, str, None] = None
    special_effects: Optional[Sequence[TrinketEffect]] = None
    str_inventory_title_trinket: Optional[str] = None
    inv_trinket_image: Optional[str] = None
    entry_id: str = Field(default_factory=lambda x: AutoName().new_trinket(), frozen=True)

    @field_validator("inv_trinket_image")
    @classmethod
    def _check_inv_trinket_image(cls, v: str):
        if (v is not None) and (not is_image(v)):
            raise ValueError("inv_trinket_image is not a valid image path")
        return v

    def get_dict(self) -> dict:
        res = {"id": self.id()}

        buffs = [] if self.buffs is None else self.buffs
        res["buffs"] = [get_entry_id(buff) for buff in buffs]

        requirements = [] if self.hero_class_requirements is None \
            else self.hero_class_requirements
        res["hero_class_requirements"] = [get_entry_id(requirement) for requirement in requirements]

        if self.set_id is not None:
            res["set_id"] = get_entry_id(self.set_id)

        res["rarity"] = get_entry_id(self.rarity)

        if self.price is not None:
            res["price"] = self.price
        if self.shard is not None:
            res["shard"] = self.shard
        if self.price is None and self.shard is None:
            if self.rarity in [
                TrinketRarityType.COMET,
                TrinketRarityType.MILDRID,
                TrinketRarityType.THING,
            ]:
                res["shard"] = 0
            elif self.rarity in [
                TrinketRarityType.TROPHY,
                TrinketRarityType.COURTIER,
                TrinketRarityType.KICKSTARTER,
            ]:
                res["price"] = 0
            elif self.rarity in [
                TrinketRarityType.DARKEST_DUNGEON,
                TrinketRarityType.CROW,
            ]:
                res["price"] = 1
            elif self.rarity == TrinketRarityType.VERY_COMMON:
                res["price"] = 5000
            elif self.rarity == TrinketRarityType.COMMON:
                res["price"] = 7500
            elif self.rarity == TrinketRarityType.UNCOMMON:
                res["price"] = 10000
            elif self.rarity in [
                TrinketRarityType.COLLECTOR,
                TrinketRarityType.MADMAN,
                TrinketRarityType.RARE,
            ]:
                res["price"] = 15000
            elif self.rarity == TrinketRarityType.VERY_RARE:
                res["price"] = 25000
            elif self.rarity in [
                TrinketRarityType.ANCESTRAL_SHAMBLER,
                TrinketRarityType.ANCESTRAL,
                TrinketRarityType.CRIMSON_COURT,
            ]:
                res["price"] = 50000
            else:
                res["price"] = 50000

        if self.limit is not None:
            res["limit"] = self.limit
        else:
            if self.rarity in [
                TrinketRarityType.VERY_COMMON,
                TrinketRarityType.COMMON,
                TrinketRarityType.UNCOMMON,
                TrinketRarityType.RARE,
                TrinketRarityType.VERY_RARE,
            ]:
                res["limit"] = 0
            else:
                res["limit"] = 1

        if self.origin_dungeon is None:
            if self.rarity == TrinketRarityType.CRIMSON_COURT:
                res["origin_dungeon"] = DungeonID.COURTYARD.value
            else:
                res["origin_dungeon"] = ""
        else:
            res["origin_dungeon"] = get_entry_id(self.origin_dungeon)

        if self.special_effects is not None:
            for effect in self.special_effects:
                if effect.trigger.value in res.keys():
                    res[effect.trigger.value].extend(effect.get_dict()[effect.trigger.value])
                else:
                    res.update(effect.get_dict())
        return res

import os
from typing import Optional, Iterable, Union, Dict

from xddtools.base import BaseLocalization, BaseJsonData
from xddtools.buffs import Buff
from xddtools.effects import Effect
from xddtools.enums import HeroClass, TrinketRarityType, DungeonID, TrinketTriggerType, TrinketAwardCategory
from xddtools.path import TRINKET_IMAGE_SAVE_DIR
from xddtools.utils import is_image, resize_image, resize_image_keep_ratio


class TrinketSet(BaseJsonData, BaseLocalization):
    def __init__(
            self,
            set_name: str,
            buffs: Optional[Iterable[Union[Buff, str]]] = None,
            localization: Optional[str] = None,
    ):
        self.buffs = buffs
        super().__init__(
            name=set_name,
            localization=localization,
            entry_id_prefix="str_inventory_set_title_",
        )

    def dict(self):
        res = {"id": self.id}
        buffs = [] if self.buffs is None else self.buffs
        tem = []
        for buff in buffs:
            if isinstance(buff, Buff):
                tem.append(buff.id)
            else:
                tem.append(buff)
        res["buffs"] = tem
        return res


class TrinketRarity(BaseJsonData, BaseLocalization):
    def __init__(
            self,
            rarity_name: str,
            image_path: str,
            award_category: TrinketAwardCategory = TrinketAwardCategory.UNIVERSAL,
            insert_before: Union[str, TrinketRarityType] = TrinketRarityType.CROW,
            localization: Optional[str] = None,
    ):
        if is_image(image_path):
            self.image_path = image_path
        else:
            raise ValueError(f"{image_path} is not a image")
        self.award_category = award_category
        self.insert_before = insert_before
        super().__init__(
            name=rarity_name,
            localization=localization,
            entry_id_prefix="trinket_rarity_",
        )

    def dict(self) -> Dict:
        res = {
            "id": self.id,
            "award_category": self.award_category.value,
            "insert_before": self.insert_before.value
            if isinstance(self.insert_before, TrinketRarityType) else self.insert_before
        }
        return res

    def export_image(self, root_dir: Optional[str] = None) -> str:
        if root_dir is None:
            root_dir = "./"
        save_dir = os.path.join(root_dir, TRINKET_IMAGE_SAVE_DIR)
        filename = f"rarity_{self.id}.png"
        return resize_image(self.image_path, os.path.join(save_dir, filename))


class TrinketEntry(BaseJsonData, BaseLocalization):
    def __init__(
            self,
            trinket_name: str,
            image_path: str,
            buffs: Optional[Iterable[Union[Buff, str]]] = None,
            hero_class_requirements: Optional[Iterable[Union[str, HeroClass]]] = None,
            set_id: Union[str, TrinketSet, None] = None,
            rarity: Union[str, TrinketRarityType, TrinketRarity, None] = None,
            price: Optional[int] = None,
            shard: Optional[int] = None,
            limit: Optional[int] = None,
            origin_dungeon: Union[str, DungeonID, None] = None,
            special_effects: Optional[Dict[TrinketTriggerType, Iterable[Union[Effect, str]]]] = None,
            localization: Optional[str] = None,
    ):
        if is_image(image_path):
            self.image_path = image_path
        else:
            raise ValueError(f"{image_path} is not a image")
        self.buffs = buffs
        self.hero_class_requirements = hero_class_requirements
        if rarity is None:
            rarity = TrinketRarityType.COMET
        self.set_id = set_id
        self.rarity = rarity
        self.price = price
        self.shard = shard
        self.limit = limit
        self.origin_dungeon = origin_dungeon
        self.special_effects = special_effects
        super().__init__(
            name=trinket_name,
            localization=localization,
            entry_id_prefix="str_inventory_title_trinket",
        )

    def dict(self):
        res = {"id": self.id}

        buffs = [] if self.buffs is None else self.buffs
        tem = []
        for buff in buffs:
            if isinstance(buff, Buff):
                tem.append(buff.id)
            else:
                tem.append(buff)
        res["buffs"] = tem

        requirements = [] if self.hero_class_requirements is None \
            else self.hero_class_requirements
        tem = []
        for requirement in requirements:
            if isinstance(requirement, HeroClass):
                tem.append(requirement.value)
            else:
                tem.append(requirement)
        res["hero_class_requirements"] = tem

        if self.set_id is not None:
            if isinstance(self.set_id, TrinketSet):
                res["set_id"] = self.set_id.id
            else:
                res["set_id"] = self.set_id

        if isinstance(self.rarity, TrinketRarityType):
            rarity = self.rarity.value
        elif isinstance(self.rarity, TrinketRarity):
            rarity = self.rarity.id
        else:
            rarity = self.rarity
        res["rarity"] = rarity

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

        if isinstance(self.origin_dungeon, DungeonID):
            res["origin_dungeon"] = self.origin_dungeon.value
        elif isinstance(self.origin_dungeon, str):
            res["origin_dungeon"] = self.origin_dungeon
        else:
            res["origin_dungeon"] = ""

        if self.special_effects is not None:
            for k, v in self.special_effects.items():
                res[k.value] = [effect.id if isinstance(effect, Effect) else effect for effect in v]

        return res

    def export_image(self, root_dir: Optional[str] = None) -> str:
        if root_dir is None:
            root_dir = "./"
        save_dir = os.path.join(root_dir, TRINKET_IMAGE_SAVE_DIR)
        filename = f"inv_trinket+{self.id}.png"
        return resize_image_keep_ratio(self.image_path, os.path.join(save_dir, filename))

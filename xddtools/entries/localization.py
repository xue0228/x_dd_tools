from typing import List, Union, Sequence, Optional

from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, model_validator

from xddtools.base import LocalizationEntry, HeroEntry, QuirkEntry, get_entry_id, CampingSkillEntry
from xddtools.entries.trait import Trait
from xddtools.enum import CombatStartTurnActOuts, ReactionActOuts
from xddtools.enum.buff_rule import TownActivityType
from xddtools.utils import get_bark_list


class Localization(LocalizationEntry, BaseModel):
    model_config = ConfigDict(
        frozen=True,
        strict=True,
    )

    entry_id: str = Field(..., min_length=1, pattern="^[a-zA-Z0-9_.+]+$")
    text: str

    @model_validator(mode="after")
    def _check_after(self):
        tem = self.text.split("\n")
        if len(tem) > 3:
            logger.warning(f"Localization {self.id()} has {len(tem)} lines.")
        return self


def get_hero_quirk_rejection_localization_entries(
        hero: Union[HeroEntry, str],
        quirk: Union[QuirkEntry, str],
        town_activity: TownActivityType,
        barks: Union[Sequence[str], str]
) -> List[Localization]:
    if isinstance(barks, str):
        barks = [barks]
    res = []
    for bark in barks:
        res.append(Localization(
            entry_id=f"{get_entry_id(hero)}+str_{get_entry_id(quirk)}_{get_entry_id(town_activity)}_rejection",
            text=bark
        ))
    return res


def get_hero_quirk_base_rejection_localization_entries(
        hero: Union[HeroEntry, str],
        alcoholism_gambling: Union[Sequence[str], str, None] = None,
        alcoholism_brothel: Union[Sequence[str], str, None] = None,
        alcoholism_meditation: Union[Sequence[str], str, None] = None,
        alcoholism_prayer: Union[Sequence[str], str, None] = None,
        alcoholism_flagellation: Union[Sequence[str], str, None] = None,
        gambler_bar: Union[Sequence[str], str, None] = None,
        gambler_brothel: Union[Sequence[str], str, None] = None,
        gambler_meditation: Union[Sequence[str], str, None] = None,
        gambler_prayer: Union[Sequence[str], str, None] = None,
        gambler_flagellation: Union[Sequence[str], str, None] = None,
        love_interest_bar: Union[Sequence[str], str, None] = None,
        love_interest_gambling: Union[Sequence[str], str, None] = None,
        love_interest_meditation: Union[Sequence[str], str, None] = None,
        love_interest_prayer: Union[Sequence[str], str, None] = None,
        love_interest_flagellation: Union[Sequence[str], str, None] = None,
        enlightened_bar: Union[Sequence[str], str, None] = None,
        enlightened_gambling: Union[Sequence[str], str, None] = None,
        enlightened_brothel: Union[Sequence[str], str, None] = None,
        enlightened_prayer: Union[Sequence[str], str, None] = None,
        enlightened_flagellation: Union[Sequence[str], str, None] = None,
        god_fearing_bar: Union[Sequence[str], str, None] = None,
        god_fearing_gambling: Union[Sequence[str], str, None] = None,
        god_fearing_brothel: Union[Sequence[str], str, None] = None,
        god_fearing_meditation: Union[Sequence[str], str, None] = None,
        god_fearing_flagellation: Union[Sequence[str], str, None] = None,
        flagellant_bar: Union[Sequence[str], str, None] = None,
        flagellant_gambling: Union[Sequence[str], str, None] = None,
        flagellant_brothel: Union[Sequence[str], str, None] = None,
        flagellant_meditation: Union[Sequence[str], str, None] = None,
        flagellant_prayer: Union[Sequence[str], str, None] = None,
        resolution_bar: Union[Sequence[str], str, None] = None,
        known_cheat_gambling: Union[Sequence[str], str, None] = None,
        deviant_tastes_brothel: Union[Sequence[str], str, None] = None,
        unquiet_mind_meditation: Union[Sequence[str], str, None] = None,
        witness_prayer: Union[Sequence[str], str, None] = None,
        faithless_prayer: Union[Sequence[str], str, None] = None,
        faithless_flagellation: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    res = []

    quirk = "alcoholism"
    if alcoholism_gambling is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.GAMBLING,
            barks=alcoholism_gambling
        ))
    if alcoholism_brothel is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BROTHEL,
            barks=alcoholism_brothel
        ))
    if alcoholism_meditation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.MEDITATION,
            barks=alcoholism_meditation
        ))
    if alcoholism_prayer is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.PRAYER,
            barks=alcoholism_prayer
        ))
    if alcoholism_flagellation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.FLAGELLATION,
            barks=alcoholism_flagellation
        ))

    quirk = "gambler"
    if gambler_bar is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BAR,
            barks=gambler_bar
        ))
    if gambler_brothel is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BROTHEL,
            barks=gambler_brothel
        ))
    if gambler_meditation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.MEDITATION,
            barks=gambler_meditation
        ))
    if gambler_prayer is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.PRAYER,
            barks=gambler_prayer
        ))
    if gambler_flagellation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.FLAGELLATION,
            barks=gambler_flagellation
        ))

    quirk = "love_interest"
    if love_interest_bar is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BAR,
            barks=love_interest_bar
        ))
    if love_interest_gambling is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.GAMBLING,
            barks=love_interest_gambling
        ))
    if love_interest_meditation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.MEDITATION,
            barks=love_interest_meditation
        ))
    if love_interest_prayer is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.PRAYER,
            barks=love_interest_prayer
        ))
    if love_interest_flagellation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.FLAGELLATION,
            barks=love_interest_flagellation
        ))

    quirk = "enlightened"
    if enlightened_bar is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BAR,
            barks=enlightened_bar
        ))
    if enlightened_gambling is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.GAMBLING,
            barks=enlightened_gambling
        ))
    if enlightened_brothel is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BROTHEL,
            barks=enlightened_brothel
        ))
    if enlightened_prayer is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.PRAYER,
            barks=enlightened_prayer
        ))
    if enlightened_flagellation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.FLAGELLATION,
            barks=enlightened_flagellation
        ))

    quirk = "god_fearing"
    if god_fearing_bar is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BAR,
            barks=god_fearing_bar
        ))
    if god_fearing_gambling is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.GAMBLING,
            barks=god_fearing_gambling
        ))
    if god_fearing_brothel is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BROTHEL,
            barks=god_fearing_brothel
        ))
    if god_fearing_meditation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.MEDITATION,
            barks=god_fearing_meditation
        ))
    if god_fearing_flagellation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.FLAGELLATION,
            barks=god_fearing_flagellation
        ))

    quirk = "flagellant"
    if flagellant_bar is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BAR,
            barks=flagellant_bar
        ))
    if flagellant_gambling is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.GAMBLING,
            barks=flagellant_gambling
        ))
    if flagellant_brothel is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BROTHEL,
            barks=flagellant_brothel
        ))
    if flagellant_meditation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.MEDITATION,
            barks=flagellant_meditation
        ))
    if flagellant_prayer is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.PRAYER,
            barks=flagellant_prayer
        ))

    quirk = "resolution"
    if resolution_bar is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BAR,
            barks=resolution_bar
        ))

    quirk = "known_cheat"
    if known_cheat_gambling is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.GAMBLING,
            barks=known_cheat_gambling
        ))

    quirk = "deviant_tastes"
    if deviant_tastes_brothel is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.BROTHEL,
            barks=deviant_tastes_brothel
        ))

    quirk = "unquiet_mind"
    if unquiet_mind_meditation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.MEDITATION,
            barks=unquiet_mind_meditation
        ))

    quirk = "witness"
    if witness_prayer is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.PRAYER,
            barks=witness_prayer
        ))

    quirk = "faithless"
    if faithless_prayer is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.PRAYER,
            barks=faithless_prayer
        ))
    if faithless_flagellation is not None:
        res.extend(get_hero_quirk_rejection_localization_entries(
            hero=hero,
            quirk=quirk,
            town_activity=TownActivityType.FLAGELLATION,
            barks=faithless_flagellation
        ))

    return res


def get_hero_camping_skill_bark_localization_entries(
        hero: Union[HeroEntry, str],
        camping_skill: Union[CampingSkillEntry, str],
        barks: Union[Sequence[str], str]
) -> List[Localization]:
    if isinstance(barks, str):
        barks = [barks]
    res = []
    for bark in barks:
        res.append(Localization(
            entry_id=f"{get_entry_id(hero)}+str_bark_{get_entry_id(camping_skill)}",
            text=bark
        ))
    return res


def get_hero_trait_bark_localization_entries(
        hero: Union[HeroEntry, str],
        trait: Union[Trait, str],
        is_virtue: Optional[bool] = None,
        enter: Union[Sequence[str], str, None] = None,
        bark_stress_camp: Union[Sequence[str], str, None] = None,
        **kwargs: Union[str, Sequence[str]]
) -> List[Localization]:
    check_list = [actout.value for actout in CombatStartTurnActOuts]
    check_list.extend([actout.value for actout in ReactionActOuts])
    check_list.remove("change_pos")
    check_list.extend(["change_pos_back", "change_pos_fwd"])
    res = []

    if enter is not None:
        if is_virtue is None:
            if not isinstance(trait, Trait):
                raise ValueError("is_virtue must be specified when enter is specified.")
            else:
                is_virtue = trait.is_virtue
        res.extend([Localization(
            entry_id=f"{get_entry_id(hero)}+str_{'virtued' if is_virtue else 'afflicted'}_{get_entry_id(trait)}",
            text=bark
        ) for bark in get_bark_list(enter)])

    res.extend([Localization(
        entry_id=f"{get_entry_id(hero)}+str_bark_stress_camp_{get_entry_id(trait)}",
        text=bark
    ) for bark in get_bark_list(bark_stress_camp)])

    for k, v in kwargs.items():
        if k not in check_list:
            raise ValueError(f"Invalid key {k}")
        res.extend([Localization(
            entry_id=f"{get_entry_id(hero)}+str_{k}_{get_entry_id(trait)}",
            text=bark
        ) for bark in get_bark_list(v)])

    return res


def get_hero_trait_fearful_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        bark_stress_camp: Union[Sequence[str], str, None] = None,
        bark_stress: Union[Sequence[str], str, None] = None,
        change_pos_back: Union[Sequence[str], str, None] = None,
        ignore_command: Union[Sequence[str], str, None] = None,
        comment_self_hit: Union[Sequence[str], str, None] = None,
        comment_self_missed: Union[Sequence[str], str, None] = None,
        comment_ally_attack_missed: Union[Sequence[str], str, None] = None,
        comment_ally_hit: Union[Sequence[str], str, None] = None,
        comment_ally_missed: Union[Sequence[str], str, None] = None,
        block_move: Union[Sequence[str], str, None] = None,
        block_camping_skill_performer: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="fearful",
        is_virtue=False,
        enter=enter,
        bark_stress=bark_stress,
        change_pos_back=change_pos_back,
        ignore_command=ignore_command,
        bark_stress_camp=bark_stress_camp,
        comment_self_hit=comment_self_hit,
        comment_self_missed=comment_self_missed,
        comment_ally_attack_missed=comment_ally_attack_missed,
        comment_ally_hit=comment_ally_hit,
        comment_ally_missed=comment_ally_missed,
        block_move=block_move,
        block_camping_skill_performer=block_camping_skill_performer
    )


def get_hero_trait_paranoid_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        bark_stress_camp: Union[Sequence[str], str, None] = None,
        bark_stress: Union[Sequence[str], str, None] = None,
        change_pos_back: Union[Sequence[str], str, None] = None,
        ignore_command: Union[Sequence[str], str, None] = None,
        random_command: Union[Sequence[str], str, None] = None,
        attack_friendly: Union[Sequence[str], str, None] = None,
        block_combat_retreat: Union[Sequence[str], str, None] = None,
        comment_self_hit: Union[Sequence[str], str, None] = None,
        comment_self_missed: Union[Sequence[str], str, None] = None,
        comment_ally_hit: Union[Sequence[str], str, None] = None,
        comment_ally_missed: Union[Sequence[str], str, None] = None,
        block_move: Union[Sequence[str], str, None] = None,
        block_item: Union[Sequence[str], str, None] = None,
        block_heal: Union[Sequence[str], str, None] = None,
        block_buff: Union[Sequence[str], str, None] = None,
        block_camping_skill_performer: Union[Sequence[str], str, None] = None,
        block_camping_skill_target: Union[Sequence[str], str, None] = None,
        block_camping_meal: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="paranoid",
        is_virtue=False,
        enter=enter,
        bark_stress=bark_stress,
        change_pos_back=change_pos_back,
        ignore_command=ignore_command,
        bark_stress_camp=bark_stress_camp,
        random_command=random_command,
        attack_friendly=attack_friendly,
        block_combat_retreat=block_combat_retreat,
        comment_self_hit=comment_self_hit,
        comment_self_missed=comment_self_missed,
        comment_ally_hit=comment_ally_hit,
        comment_ally_missed=comment_ally_missed,
        block_move=block_move,
        block_item=block_item,
        block_heal=block_heal,
        block_buff=block_buff,
        block_camping_skill_performer=block_camping_skill_performer,
        block_camping_skill_target=block_camping_skill_target,
        block_camping_meal=block_camping_meal
    )


def get_hero_trait_abusive_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        bark_stress_camp: Union[Sequence[str], str, None] = None,
        bark_stress: Union[Sequence[str], str, None] = None,
        change_pos_back: Union[Sequence[str], str, None] = None,
        random_command: Union[Sequence[str], str, None] = None,
        attack_friendly: Union[Sequence[str], str, None] = None,
        comment_ally_attack_hit: Union[Sequence[str], str, None] = None,
        comment_ally_attack_missed: Union[Sequence[str], str, None] = None,
        comment_ally_hit: Union[Sequence[str], str, None] = None,
        block_move: Union[Sequence[str], str, None] = None,
        block_camping_skill_performer: Union[Sequence[str], str, None] = None,
        block_camping_skill_target: Union[Sequence[str], str, None] = None,
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="abusive",
        is_virtue=False,
        enter=enter,
        bark_stress_camp=bark_stress_camp,
        bark_stress=bark_stress,
        change_pos_back=change_pos_back,
        random_command=random_command,
        attack_friendly=attack_friendly,
        comment_ally_attack_hit=comment_ally_attack_hit,
        comment_ally_attack_missed=comment_ally_attack_missed,
        comment_ally_hit=comment_ally_hit,
        block_move=block_move,
        block_camping_skill_performer=block_camping_skill_performer,
        block_camping_skill_target=block_camping_skill_target,
    )


def get_hero_trait_masochistic_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        bark_stress_camp: Union[Sequence[str], str, None] = None,
        bark_stress: Union[Sequence[str], str, None] = None,
        change_pos_fwd: Union[Sequence[str], str, None] = None,
        random_command: Union[Sequence[str], str, None] = None,
        mark_self: Union[Sequence[str], str, None] = None,
        attack_self: Union[Sequence[str], str, None] = None,
        block_combat_retreat: Union[Sequence[str], str, None] = None,
        comment_self_hit: Union[Sequence[str], str, None] = None,
        comment_self_missed: Union[Sequence[str], str, None] = None,
        comment_ally_hit: Union[Sequence[str], str, None] = None,
        block_move: Union[Sequence[str], str, None] = None,
        block_item: Union[Sequence[str], str, None] = None,
        block_heal: Union[Sequence[str], str, None] = None,
        block_buff: Union[Sequence[str], str, None] = None,
        block_camping_skill_performer: Union[Sequence[str], str, None] = None,
        block_camping_skill_target: Union[Sequence[str], str, None] = None,
        block_camping_meal: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="masochistic",
        is_virtue=False,
        enter=enter,
        bark_stress_camp=bark_stress_camp,
        bark_stress=bark_stress,
        change_pos_fwd=change_pos_fwd,
        random_command=random_command,
        mark_self=mark_self,
        attack_self=attack_self,
        block_combat_retreat=block_combat_retreat,
        comment_self_hit=comment_self_hit,
        comment_self_missed=comment_self_missed,
        comment_ally_hit=comment_ally_hit,
        block_move=block_move,
        block_item=block_item,
        block_heal=block_heal,
        block_buff=block_buff,
        block_camping_skill_performer=block_camping_skill_performer,
        block_camping_skill_target=block_camping_skill_target,
        block_camping_meal=block_camping_meal
    )


def get_hero_trait_selfish_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        bark_stress_camp: Union[Sequence[str], str, None] = None,
        bark_stress: Union[Sequence[str], str, None] = None,
        change_pos_fwd: Union[Sequence[str], str, None] = None,
        change_pos_back: Union[Sequence[str], str, None] = None,
        ignore_command: Union[Sequence[str], str, None] = None,
        random_command: Union[Sequence[str], str, None] = None,
        comment_self_hit: Union[Sequence[str], str, None] = None,
        comment_ally_attack_hit: Union[Sequence[str], str, None] = None,
        comment_ally_attack_missed: Union[Sequence[str], str, None] = None,
        block_camping_skill_performer: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="selfish",
        is_virtue=False,
        enter=enter,
        bark_stress_camp=bark_stress_camp,
        bark_stress=bark_stress,
        change_pos_fwd=change_pos_fwd,
        change_pos_back=change_pos_back,
        ignore_command=ignore_command,
        random_command=random_command,
        comment_self_hit=comment_self_hit,
        comment_ally_attack_hit=comment_ally_attack_hit,
        comment_ally_attack_missed=comment_ally_attack_missed,
        block_camping_skill_performer=block_camping_skill_performer,
    )


def get_hero_trait_depressed_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        bark_stress_camp: Union[Sequence[str], str, None] = None,
        bark_stress: Union[Sequence[str], str, None] = None,
        change_pos_fwd: Union[Sequence[str], str, None] = None,
        change_pos_back: Union[Sequence[str], str, None] = None,
        ignore_command: Union[Sequence[str], str, None] = None,
        random_command: Union[Sequence[str], str, None] = None,
        mark_self: Union[Sequence[str], str, None] = None,
        attack_self: Union[Sequence[str], str, None] = None,
        block_combat_retreat: Union[Sequence[str], str, None] = None,
        block_item: Union[Sequence[str], str, None] = None,
        block_heal: Union[Sequence[str], str, None] = None,
        block_buff: Union[Sequence[str], str, None] = None,
        block_camping_skill_performer: Union[Sequence[str], str, None] = None,
        block_camping_skill_target: Union[Sequence[str], str, None] = None,
        block_camping_meal: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="depressed",
        is_virtue=False,
        enter=enter,
        bark_stress_camp=bark_stress_camp,
        bark_stress=bark_stress,
        change_pos_fwd=change_pos_fwd,
        change_pos_back=change_pos_back,
        ignore_command=ignore_command,
        random_command=random_command,
        mark_self=mark_self,
        attack_self=attack_self,
        block_combat_retreat=block_combat_retreat,
        block_item=block_item,
        block_heal=block_heal,
        block_buff=block_buff,
        block_camping_skill_performer=block_camping_skill_performer,
        block_camping_skill_target=block_camping_skill_target,
        block_camping_meal=block_camping_meal
    )


def get_hero_trait_irrational_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        bark_stress_camp: Union[Sequence[str], str, None] = None,
        bark_stress: Union[Sequence[str], str, None] = None,
        change_pos_fwd: Union[Sequence[str], str, None] = None,
        change_pos_back: Union[Sequence[str], str, None] = None,
        ignore_command: Union[Sequence[str], str, None] = None,
        random_command: Union[Sequence[str], str, None] = None,
        mark_self: Union[Sequence[str], str, None] = None,
        attack_friendly: Union[Sequence[str], str, None] = None,
        attack_self: Union[Sequence[str], str, None] = None,
        block_combat_retreat: Union[Sequence[str], str, None] = None,
        comment_self_hit: Union[Sequence[str], str, None] = None,
        comment_self_missed: Union[Sequence[str], str, None] = None,
        comment_ally_attack_hit: Union[Sequence[str], str, None] = None,
        comment_ally_attack_missed: Union[Sequence[str], str, None] = None,
        comment_ally_hit: Union[Sequence[str], str, None] = None,
        comment_ally_missed: Union[Sequence[str], str, None] = None,
        block_move: Union[Sequence[str], str, None] = None,
        block_item: Union[Sequence[str], str, None] = None,
        block_heal: Union[Sequence[str], str, None] = None,
        block_buff: Union[Sequence[str], str, None] = None,
        block_camping_skill_performer: Union[Sequence[str], str, None] = None,
        block_camping_meal: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="irrational",
        is_virtue=False,
        enter=enter,
        bark_stress_camp=bark_stress_camp,
        bark_stress=bark_stress,
        change_pos_fwd=change_pos_fwd,
        change_pos_back=change_pos_back,
        ignore_command=ignore_command,
        random_command=random_command,
        mark_self=mark_self,
        attack_friendly=attack_friendly,
        attack_self=attack_self,
        block_combat_retreat=block_combat_retreat,
        comment_self_hit=comment_self_hit,
        comment_self_missed=comment_self_missed,
        comment_ally_attack_hit=comment_ally_attack_hit,
        comment_ally_attack_missed=comment_ally_attack_missed,
        comment_ally_hit=comment_ally_hit,
        comment_ally_missed=comment_ally_missed,
        block_move=block_move,
        block_item=block_item,
        block_heal=block_heal,
        block_buff=block_buff,
        block_camping_skill_performer=block_camping_skill_performer,
        block_camping_meal=block_camping_meal
    )


def get_hero_trait_stalwart_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        stress_heal_self: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="stalwart",
        is_virtue=True,
        enter=enter,
        stress_heal_self=stress_heal_self
    )


def get_hero_trait_courageous_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        stress_heal_party: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="courageous",
        is_virtue=True,
        enter=enter,
        stress_heal_party=stress_heal_party
    )


def get_hero_trait_focused_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        buff_random_party_member: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="focused",
        is_virtue=True,
        enter=enter,
        buff_random_party_member=buff_random_party_member
    )


def get_hero_trait_powerful_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        buff_party: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="powerful",
        is_virtue=True,
        enter=enter,
        buff_party=buff_party
    )


def get_hero_trait_vigorous_localization_entries(
        hero: Union[HeroEntry, str],
        enter: Union[Sequence[str], str, None] = None,
        heal_self: Union[Sequence[str], str, None] = None
) -> List[Localization]:
    return get_hero_trait_bark_localization_entries(
        hero=hero,
        trait="vigorous",
        is_virtue=True,
        enter=enter,
        heal_self=heal_self
    )


if __name__ == '__main__':
    tem = get_hero_trait_stalwart_localization_entries(
        hero="x",
        enter="x",
        stress_heal_self=""
    )
    print(tem)

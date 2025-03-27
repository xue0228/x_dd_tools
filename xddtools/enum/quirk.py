from enum import Enum


class QuirkClassification(Enum):
    PHYSICAL = "physical"
    MENTAL = "mental"


class CurioTag(Enum):
    # 本体
    NONE = "None"
    FOOD = "Food"
    UNHOLY = "Unholy"
    WORSHIP = "Worship"
    TREASURE = "Treasure"
    TORTURE = "Torture"
    ALL = "All"
    FOUNTAIN = "Fountain"
    REFLECTIVE = "Reflective"
    BODY = "Body"
    DRINK = "Drink"
    HAUNTED = "Haunted"
    # CC
    CCRAVE = "CCrave"


class QuirkTag(Enum):
    VAMPIRE = "vampire"
    VAMPIRE_PASSIVE = "vampire_passive"
    SINGLETON = "singleton"
    REMOVE_ON_DEATH = "remove_on_death"
    CANT_LOCK = "cant_lock"
    CONTAGIOUS_IMMUNE = "contagious_immune"

from enum import Enum


class TagID(Enum):
    BOSS = "boss"
    LIGHT = "light"
    HEAVY = "heavy"
    RELIGIOUS = "religious"
    NON_RELIGIOUS = "non-religious"
    HOUSE_OF_THE_YELLOW_HAND = "house_of_the_yellow_hand"
    TRAINING_RING = "training_ring"
    LIBRARY = "library"
    OUTSIDERS_BONFIRE = "outsiders_bonfire"


class DeathFx(Enum):
    DEATH_SMALL = "death_small"
    DEATH_MEDIUM = "death_medium"
    DEATH_LARGE = "death_large"
    DEATH_LARGE_BOSS = "death_large_boss"
    DEATH_CORPSE_MEDIUM = "death_corpse_medium"

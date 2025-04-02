from typing import Union, Sequence, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator

from xddtools import AutoName
from xddtools.base import JsonData, LootTableEntry, ItemEntry, get_entry_id, CampingSkillEntry, HeroEntry, BankEntry, \
    BuffEntry
from xddtools.enum.buff_rule import HeroClass, ItemID, ItemType
from xddtools.enum.camping_skill import CampingSkillBuffSubType, CampingSkillEffectType, CampingSkillSelection, \
    CampingSkillEffectRequirement
from xddtools.utils import int_to_alpha_str, is_image


class CampingSkillEffect(JsonData, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    effect_type: CampingSkillEffectType
    sub_type: Union[ItemEntry, LootTableEntry, CampingSkillBuffSubType, BuffEntry, str] = ""
    amount: float = 0.0
    selection: CampingSkillSelection = CampingSkillSelection.INDIVIDUAL
    requirements: Sequence[CampingSkillEffectRequirement] = Field(default_factory=list)
    chance: float = 1.0
    code_idx: int = 1,
    effect_tooltip: Optional[str] = None  # 目前只看到过 loot 使用

    @model_validator(mode="after")
    def _check_after(self):
        if self.effect_type == CampingSkillEffectType.BUFF:
            if not isinstance(self.sub_type, (CampingSkillBuffSubType, BuffEntry, str)):
                raise ValueError("when effect_type == CampingSkillEffectType.BUFF,"
                                 "sub_type must be CampingSkillBuffSubType,BuffEntry or str")
        elif self.effect_type == CampingSkillEffectType.ITEM:
            if not isinstance(self.sub_type, (ItemEntry, str)):
                raise ValueError("when effect_type == CampingSkillEffectType.ITEM,"
                                 "sub_type must be ItemEntry or str")
        elif self.effect_type == CampingSkillEffectType.LOOT:
            if not isinstance(self.sub_type, (LootTableEntry, str)):
                raise ValueError("when effect_type == CampingSkillEffectType.LOOT,"
                                 "sub_type must be LootTableEntry or str")
        else:
            if self.sub_type != "":
                raise ValueError(f"{self.effect_type.value} no need sub_type")
        return self

    def get_dict(self) -> dict:
        code = int_to_alpha_str(self.code_idx)
        requirements = [r.value for r in self.requirements]
        return {
            "selection": self.selection.value,
            "requirements": requirements,
            "chance": {"code": code, "amount": self.chance},
            "type": self.effect_type.value,
            "sub_type": get_entry_id(self.sub_type),
            "amount": self.amount,
        }


class CampingSkill(JsonData, CampingSkillEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    cost: int
    effects: Sequence[CampingSkillEffect]
    hero_classes: Sequence[Union[HeroEntry, HeroClass, str]] = Field(default_factory=list)
    level: int = 0
    use_limit: int = 1
    currency_cost_type: Union[ItemType, ItemID, str] = "gold"
    currency_cost_amount: int = 1750
    camping_skill_image: Optional[str] = None
    sfx: Union[BankEntry, str, None] = None

    camping_skill_name: Optional[str] = None
    str_camping_skill_barks: Union[Sequence[str], str, None] = None
    entry_id: str = Field(default_factory=lambda x: AutoName().new_camping_skill(), frozen=True)

    @field_validator("camping_skill_image")
    @classmethod
    def _check_camping_skill_image(cls, v: str):
        if (v is not None) and (not is_image(v)):
            raise ValueError(f"{v} is not a valid image path")
        return v

    def get_dict(self) -> dict:
        hero_class = []
        for hc in self.hero_classes:
            hero_class.append(get_entry_id(hc))

        effects = []
        idx = 0
        for effect in self.effects:
            effect.code_idx = idx
            effects.append(effect.get_dict())
            idx += 1

        return {
            "id": self.id(),
            "level": self.level,
            "cost": self.cost,
            "use_limit": self.use_limit,
            "effects": effects,
            "hero_classes": hero_class,
            "upgrade_requirements": [{
                "code": "0",
                "currency_cost": [{
                    "type": get_entry_id(self.currency_cost_type),
                    "amount": self.currency_cost_amount
                }],
                "prerequisite_requirements": []
            }]
        }


UNIVERSAL = ("bounty_hunter", "crusader", "vestal", "occultist",
             "hellion", "grave_robber", "highwayman", "plague_doctor",
             "jester", "leper", "arbalest", "man_at_arms",
             "houndmaster", "abomination", "antiquarian", "musketeer")

# AI 生成，可能存在错误，使用前建议检查
encourage = CampingSkill(
    entry_id="encourage",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=15
        ),
    ),
    hero_classes=UNIVERSAL
)

first_aid = CampingSkill(
    entry_id="first_aid",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.15
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_BLEEDING,
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_POISON,
        ),
    ),
    hero_classes=UNIVERSAL
)

pep_talk = CampingSkill(
    entry_id="pep_talk",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_STRESS_RESIST_BUFF,
            amount=-0.15
        ),
    ),
    hero_classes=UNIVERSAL
)

hobby = CampingSkill(
    entry_id="hobby",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=12,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=()
)

field_dressing = CampingSkill(
    entry_id="field_dressing",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.35,
            chance=0.75
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.50,
            chance=0.25
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_BLEEDING,
        ),
    ),
    hero_classes=("arbalest", "musketeer")
)

marching_plan = CampingSkill(
    entry_id="marching_plan",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SPD_BUFF_PARTY,
            amount=2,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
    ),
    hero_classes=("arbalest", "musketeer")
)

restring_crossbow = CampingSkill(
    entry_id="restring_crossbow",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF_RANGED,
            amount=0.10,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF_RANGED,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF_RANGED,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_CRIT_BUFF_RANGED,
            amount=0.08,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SPD_BUFF_PARTY,
            amount=-2,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("arbalest",)
)

clean_musket = CampingSkill(
    entry_id="clean_musket",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF_RANGED,
            amount=0.10,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF_RANGED,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF_RANGED,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_CRIT_BUFF_RANGED,
            amount=0.08,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SPD_BUFF_PARTY,
            amount=-2,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("musketeer",)
)

triage = CampingSkill(
    entry_id="triage",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.20,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
    ),
    hero_classes=("arbalest", "musketeer")
)

how_its_done = CampingSkill(
    entry_id="how_its_done",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF,
            amount=0.10,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_CRIT_BUFF,
            amount=0.08,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("bounty_hunter",)
)

tracking = CampingSkill(
    entry_id="tracking",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_PARTY_SURPRISE,
            amount=-0.15,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_MONSTERS_SURPRISE,
            amount=0.10,
            selection=CampingSkillSelection.SELF
        )
    ),
    hero_classes=("bounty_hunter",)
)

planned_takedown = CampingSkill(
    entry_id="planned_takedown",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF_LARGE_MONSTERS,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF_LARGE_MONSTERS,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF_LARGE_MONSTERS,
            amount=0.15,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("bounty_hunter",)
)

scout_ahead = CampingSkill(
    entry_id="scout_ahead",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SCOUTING_BUFF,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("bounty_hunter",)
)

unshakeable_leader = CampingSkill(
    entry_id="unshakeable_leader",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_STRESS_RESIST_BUFF,
            amount=-0.25,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("crusader",)
)

stand_tall = CampingSkill(
    entry_id="stand_tall",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=15
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_DEATHS_DOOR_RECOVERY_BUFFS
        ),
    ),
    hero_classes=("crusader",)
)

zealous_speech = CampingSkill(
    entry_id="zealous_speech",
    cost=5,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=15,
            selection=CampingSkillSelection.PARTY
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_STRESS_RESIST_BUFF,
            amount=-0.15,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
    ),
    hero_classes=("crusader",)
)

zealous_vigil = CampingSkill(
    entry_id="zealous_vigil",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=15,
            selection=CampingSkillSelection.SELF,
            requirements=[CampingSkillEffectRequirement.AFFLICTED]
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REDUCE_AMBUSH_CHANCE,
            amount=1.0,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("crusader",)
)

forage = CampingSkill(
    entry_id="forage",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_DISEASE,

            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_DISEASE,

            selection=CampingSkillSelection.INDIVIDUAL
        ),
    ),
    hero_classes=("grave_robber",)
)

gallows_humor = CampingSkill(
    entry_id="gallows_humor",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=20,
            selection=CampingSkillSelection.PARTY_OTHER,
            chance=0.75
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=10,
            selection=CampingSkillSelection.PARTY_OTHER,
            chance=0.25
        ),
    ),
    hero_classes=("grave_robber", "highwayman")
)

night_steps = CampingSkill(
    entry_id="night_steps",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SCOUTING_BUFF,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("grave_robber",)
)

pilfer = CampingSkill(
    entry_id="pilfer",
    cost=1,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.LOOT,
            sub_type="S",
            amount=1,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("grave_robber",)
)

battle_trance = CampingSkill(
    entry_id="battle_trance",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF_FRONT_RANK,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF_FRONT_RANK,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF_NOT_FRONT_RANK,
            amount=-0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF_NOT_FRONT_RANK,
            amount=-0.25,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("hellion",)
)

revel = CampingSkill(
    entry_id="revel",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF,
            amount=-0.05,
            selection=CampingSkillSelection.PARTY
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SPD_BUFF,
            amount=-2,
            selection=CampingSkillSelection.PARTY
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=20,
            selection=CampingSkillSelection.PARTY
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_STRESS_RESIST_BUFF,
            amount=-0.10,
            selection=CampingSkillSelection.PARTY
        ),
    ),
    hero_classes=("hellion",)
)

reject_the_gods = CampingSkill(
    entry_id="reject_the_gods",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=30,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=7,
            selection=CampingSkillSelection.PARTY_OTHER,
            requirements=(CampingSkillEffectRequirement.NOT_RELIGIOUS,)
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=15,
            selection=CampingSkillSelection.PARTY_OTHER,
            requirements=(CampingSkillEffectRequirement.RELIGIOUS,)
        ),
    ),
    hero_classes=("hellion",)
)

sharpen_spear = CampingSkill(
    entry_id="sharpen_spear",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_CRIT_BUFF,
            amount=0.10,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("hellion",)
)

uncatchable = CampingSkill(
    entry_id="uncatchable",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DEF_BUFF,
            amount=0.1,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SPD_BUFF,
            amount=2,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF_MELEE,
            amount=0.2,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF_MELEE,
            amount=0.2,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF_MELEE,
            amount=0.1,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("highwayman",)
)

clean_guns = CampingSkill(
    entry_id="clean_guns",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF_RANGED,
            amount=0.10,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF_RANGED,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF_RANGED,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_CRIT_BUFF_RANGED,
            amount=0.08,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("highwayman",)
)

bandits_sense = CampingSkill(
    entry_id="bandits_sense",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REDUCE_AMBUSH_CHANCE,
            amount=1.0,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_PARTY_SURPRISE,
            amount=-0.20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_MONSTERS_SURPRISE,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("highwayman",)
)

maintain_equipment = CampingSkill(
    entry_id="maintain_equipment",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_PROT_BUFF,
            amount=0.15,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF,
            amount=0.15,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF,
            amount=0.15,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("man_at_arms",)
)

tactics = CampingSkill(
    entry_id="tactics",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DEF_BUFF,
            amount=0.10,
            selection=CampingSkillSelection.PARTY
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_CRIT_BUFF,
            amount=0.05,
            selection=CampingSkillSelection.PARTY
        ),
    ),
    hero_classes=("man_at_arms",)
)

instruction = CampingSkill(
    entry_id="instruction",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF,
            amount=0.10,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SPD_BUFF,
            amount=3,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
    ),
    hero_classes=("man_at_arms",)
)

weapons_practice = CampingSkill(
    entry_id="weapons_practice",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF,
            amount=0.10,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF,
            amount=0.10,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_CRIT_BUFF,
            amount=0.08,
            selection=CampingSkillSelection.PARTY_OTHER,
            chance=0.75
        ),
    ),
    hero_classes=("man_at_arms",)
)

abandon_hope = CampingSkill(
    entry_id="abandon_hope",
    cost=1,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=10,
            selection=CampingSkillSelection.PARTY_OTHER,
            chance=0.5
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=5,
            selection=CampingSkillSelection.PARTY_OTHER,
            chance=0.5
        ),
    ),
    hero_classes=("occultist",)
)

dark_ritual = CampingSkill(
    entry_id="dark_ritual",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.50,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REDUCE_TORCH,
            amount=100,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=15,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_DEATHS_DOOR_RECOVERY_BUFFS,

            selection=CampingSkillSelection.INDIVIDUAL
        ),
    ),
    hero_classes=("occultist",)
)

dark_strength = CampingSkill(
    entry_id="dark_strength",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF,
            amount=0.20,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF,
            amount=0.20,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=15,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("occultist",)
)

unspeakable_commune = CampingSkill(
    entry_id="unspeakable_commune",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=7,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REDUCE_AMBUSH_CHANCE,
            amount=1.0,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("occultist",)
)

experimental_vapours = CampingSkill(
    entry_id="experimental_vapours",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.5,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_HEAL_RECEIVED_BUFF,
            amount=0.33,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
    ),
    hero_classes=("plague_doctor",)
)

leeches = CampingSkill(
    entry_id="leeches",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.15,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_POISON,

            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_DISEASE,

            selection=CampingSkillSelection.INDIVIDUAL
        ),
    ),
    hero_classes=("plague_doctor",)
)

preventative_medicine = CampingSkill(
    entry_id="preventative_medicine",
    cost=1,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_DISEASE,

            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DISEASE_RESIST_BUFF,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("plague_doctor",)
)

self_medicate = CampingSkill(
    entry_id="self_medicate",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=10,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_POISON,

            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_BLEEDING,

            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF,
            amount=0.1,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("plague_doctor",)
)

bless = CampingSkill(
    entry_id="bless",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF,
            amount=0.10,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DEF_BUFF,
            amount=0.10,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
    ),
    hero_classes=("vestal",)
)

chant = CampingSkill(
    entry_id="chant",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_STRESS_RESIST_BUFF,
            amount=-0.20,
            selection=CampingSkillSelection.INDIVIDUAL,
            requirements=(CampingSkillEffectRequirement.RELIGIOUS,)
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_STRESS_RESIST_BUFF,
            amount=-0.10,
            selection=CampingSkillSelection.INDIVIDUAL,
            requirements=(CampingSkillEffectRequirement.NOT_RELIGIOUS,)
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=15,
            selection=CampingSkillSelection.INDIVIDUAL,
            requirements=(CampingSkillEffectRequirement.RELIGIOUS,)
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=5,
            selection=CampingSkillSelection.INDIVIDUAL,
            requirements=(CampingSkillEffectRequirement.NOT_RELIGIOUS,)
        ),
    ),
    hero_classes=("vestal",)
)

pray = CampingSkill(
    entry_id="pray",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=15,
            selection=CampingSkillSelection.PARTY_OTHER,
            requirements=(CampingSkillEffectRequirement.RELIGIOUS,)
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=5,
            selection=CampingSkillSelection.PARTY_OTHER,
            requirements=(CampingSkillEffectRequirement.NOT_RELIGIOUS,)
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_PROT_BUFF,
            amount=0.15,
            selection=CampingSkillSelection.PARTY_OTHER,
            requirements=(CampingSkillEffectRequirement.RELIGIOUS,)
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_PROT_BUFF,
            amount=0.05,
            selection=CampingSkillSelection.PARTY_OTHER,
            requirements=(CampingSkillEffectRequirement.NOT_RELIGIOUS,)
        ),
    ),
    hero_classes=("vestal",)
)

sanctuary = CampingSkill(
    entry_id="sanctuary",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REDUCE_AMBUSH_CHANCE,
            amount=1.0,
            selection=CampingSkillSelection.SELF,
            requirements=(CampingSkillEffectRequirement.RELIGIOUS,)
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.5,
            selection=CampingSkillSelection.PARTY_OTHER,
            requirements=[CampingSkillEffectRequirement.HAS_DEATHS_DOOR_RECOVERY_BUFFS]
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=25,
            selection=CampingSkillSelection.PARTY_OTHER,
            requirements=[CampingSkillEffectRequirement.HAS_DEATHS_DOOR_RECOVERY_BUFFS]
        ),
    ),
    hero_classes=("vestal",)
)

turn_back_time = CampingSkill(
    entry_id="turn_back_time",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=30,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=15,
            selection=CampingSkillSelection.INDIVIDUAL,
            requirements=[CampingSkillEffectRequirement.AFFLICTED]
        ),
    ),
    hero_classes=("jester",)
)

every_rose = CampingSkill(
    entry_id="every_rose",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=15,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_STRESS_RESIST_BUFF,
            amount=-0.15,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
    ),
    hero_classes=("jester",)
)

tigers_eye = CampingSkill(
    entry_id="tigers_eye",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF,
            amount=0.10,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_CRIT_BUFF,
            amount=0.08,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
    ),
    hero_classes=("jester",)
)

mockery = CampingSkill(
    entry_id="mockery",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=20,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=20,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
    ),
    hero_classes=("jester",)
)

let_the_mask_down = CampingSkill(
    entry_id="let_the_mask_down",
    cost=1,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=5,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
    ),
    hero_classes=("leper",)
)

bloody_shroud = CampingSkill(
    entry_id="bloody_shroud",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_BLEED_RESIST_BUFF,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_BLIGHT_RESIST_BUFF,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_MOVE_RESIST_BUFF,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DEBUFF_RESIST_BUFF,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("leper",)
)

reflection = CampingSkill(
    entry_id="reflection",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_ACC_BUFF,
            amount=0.10,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_CRIT_BUFF,
            amount=0.08,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("leper",)
)

quarantine = CampingSkill(
    entry_id="quarantine",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_DAMAGE_MAX_HEALTH_PERCENT,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=20,
            selection=CampingSkillSelection.PARTY_OTHER,
            chance=0.50
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=15,
            selection=CampingSkillSelection.PARTY_OTHER,
            chance=0.50
        ),
    ),
    hero_classes=("leper",)
)

hounds_watch = CampingSkill(
    entry_id="hounds_watch",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_PARTY_SURPRISE,
            amount=-0.20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_MONSTERS_SURPRISE,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REDUCE_AMBUSH_CHANCE,
            amount=1.0,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("houndmaster",)
)

therapy_dog = CampingSkill(
    entry_id="therapy_dog",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=10,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_STRESS_RESIST_BUFF,
            amount=-0.1,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
    ),
    hero_classes=("houndmaster",)
)

pet_the_hound = CampingSkill(
    entry_id="pet_the_hound",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=20,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("houndmaster",)
)

release_the_hound = CampingSkill(
    entry_id="release_the_hound",
    cost=4,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SCOUTING_BUFF,
            amount=0.30,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("houndmaster",)
)

anger_management = CampingSkill(
    entry_id="anger_management",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=20,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=10,
            selection=CampingSkillSelection.PARTY_OTHER
        ),
    ),
    hero_classes=("abomination",)
)

psych_up = CampingSkill(
    entry_id="psych_up",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_LOW_BUFF,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DMG_HIGH_BUFF,
            amount=0.25,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=10,
            selection=CampingSkillSelection.PARTY_OTHER,
            requirements=(CampingSkillEffectRequirement.NOT_RELIGIOUS,)
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=20,
            selection=CampingSkillSelection.PARTY_OTHER,
            requirements=(CampingSkillEffectRequirement.RELIGIOUS,)
        ),
    ),
    hero_classes=("abomination",)
)

the_quickening = CampingSkill(
    entry_id="the_quickening",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SPD_BUFF,
            amount=4,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("abomination",)
)

# eldritch_blood skill
eldritch_blood = CampingSkill(
    entry_id="eldritch_blood",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_BLIGHT_RESIST_BUFF,
            amount=0.40,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_BLEED_RESIST_BUFF,
            amount=0.40,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DISEASE_RESIST_BUFF,
            amount=0.40,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_STRESS_RESIST_BUFF,
            amount=0.20,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("abomination",)
)

# supply skill
supply = CampingSkill(
    entry_id="supply",
    cost=1,
    use_limit=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.LOOT,
            sub_type="S",
            amount=1,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("antiquarian",)
)

# trinket_scrounge skill
trinket_scrounge = CampingSkill(
    entry_id="trinket_scrounge",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.LOOT,
            sub_type="T_ANTIQ_CAMP",
            amount=1,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("antiquarian",)
)

# strange_powders skill
strange_powders = CampingSkill(
    entry_id="strange_powders",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_BLEED_RESIST_BUFF,
            amount=0.20,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_BLIGHT_RESIST_BUFF,
            amount=0.20,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_MOVE_RESIST_BUFF,
            amount=0.20,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DEBUFF_RESIST_BUFF,
            amount=0.20,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_DISEASE_RESIST_BUFF,
            amount=0.20,
            selection=CampingSkillSelection.INDIVIDUAL
        ),
    ),
    hero_classes=("antiquarian",)
)

# curious_incantation skill
curious_incantation = CampingSkill(
    entry_id="curious_incantation",
    cost=1,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_STRESS_RESIST_BUFF,
            amount=-0.50,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("antiquarian",)
)

# CC
# lash_anger skill
lash_anger = CampingSkill(
    entry_id="lash_anger",
    cost=1,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_DAMAGE_AMOUNT,
            amount=40,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("flagellant",)
)

# lash_solace skill
lash_solace = CampingSkill(
    entry_id="lash_solace",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=50,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("flagellant",)
)

# lash_kiss skill
lash_kiss = CampingSkill(
    entry_id="lash_kiss",
    cost=3,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.33,
            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_POISON,

            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_BLEEDING,

            selection=CampingSkillSelection.SELF
        ),
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.BUFF,
            sub_type=CampingSkillBuffSubType.CAMPING_SPD_BUFF,
            amount=3,
            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("flagellant",)
)

# lash_cure skill
lash_cure = CampingSkill(
    entry_id="lash_cure",
    cost=2,
    effects=(
        CampingSkillEffect(
            effect_type=CampingSkillEffectType.REMOVE_DISEASE,

            selection=CampingSkillSelection.SELF
        ),
    ),
    hero_classes=("flagellant",)
)


if __name__ == '__main__':
    import json

    data = json.load(open("default.camping_skills.json", "r", encoding="utf-8"))
    print(data)


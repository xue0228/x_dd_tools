import os
from enum import Enum
from typing import Union, Tuple, Dict, Iterable, Any, Optional

from xddtools.base import BaseLocalization, BaseJsonData, BaseID
from xddtools.enums import CampingSkillSelection, CampingSkillEffectRequirement, CampingSkillEffectType, \
    CampingSkillBuffSubType
from xddtools.path import CAMPING_SKILL_IMAGE_SAVE_DIR
from xddtools.utils import int_to_alpha_str, is_image, resize_image_keep_ratio


class CampingSkillEffect(BaseJsonData):
    def __init__(
            self,
            effect_type: CampingSkillEffectType,
            sub_type: Any = "",
            amount: float = 0.0,
            selection: CampingSkillSelection = CampingSkillSelection.INDIVIDUAL,
            requirements: Optional[Iterable[CampingSkillEffectRequirement]] = None,
            chance: float = 1.0,
            code_idx: int = 0
    ):
        self.effect_type = effect_type
        self.sub_type = sub_type
        self.amount = amount
        self.selection = selection
        self.requirements = requirements or []
        self.chance = chance
        self.code_idx = code_idx

    def dict(self) -> Dict:
        if isinstance(self.sub_type, BaseID):
            sub_type = self.sub_type.id
        elif isinstance(self.sub_type, Enum):
            sub_type = self.sub_type.value
        else:
            sub_type = self.sub_type
        code = int_to_alpha_str(self.code_idx)
        requirements = [r.value for r in self.requirements]
        return {
            "selection": self.selection.value,
            "requirements": requirements,
            "chance": {"code": code, "amount": self.chance},
            "type": self.effect_type.value,
            "sub_type": sub_type,
            "amount": self.amount,
        }


class CampingSkill(BaseJsonData, BaseLocalization):
    def __init__(
            self,
            name: str,
            cost: int,
            effects: Iterable[CampingSkillEffect],
            hero_classes: Iterable[Union[BaseID, Enum, str]],
            level: int = 0,
            use_limit: int = 1,
            currency_cost_type: str = "gold",
            currency_cost_amount: int = 1750,
            image_path: Optional[str] = None,

            localization: Union[Tuple[str, ...], str, None] = None,
    ):
        if (image_path is not None) and (not is_image(image_path)):
            raise ValueError(f"{image_path} is not a image")
        self.image_path = image_path

        self.cost = cost
        self.effects = effects
        self.hero_classes = hero_classes
        self.level = level
        self.use_limit = use_limit
        self.currency_cost_type = currency_cost_type
        self.currency_cost_amount = currency_cost_amount
        super().__init__(
            name=name,
            localization=localization,
            entry_id_prefix=(
                "camping_skill_name_",
                "str_bark_"
            )
        )

    def dict(self) -> Dict:
        hero_class = []
        for hc in self.hero_classes:
            if isinstance(hc, BaseID):
                hero_class.append(hc.id)
            elif isinstance(hc, Enum):
                hero_class.append(hc.value)
            else:
                hero_class.append(hc)

        effects = []
        idx = 0
        for effect in self.effects:
            effect.code_idx = idx
            effects.append(effect.dict())
            idx += 1

        return {
            "id": self.id,
            "level": self.level,
            "cost": self.cost,
            "use_limit": self.use_limit,
            "effects": effects,
            "hero_classes": hero_class,
            "upgrade_requirements": [{
                "code": "0",
                "currency_cost": [{
                    "type": self.currency_cost_type,
                    "amount": self.currency_cost_amount
                }],
                "prerequisite_requirements": []
            }]
        }

    def export_image(self, root_dir: Optional[str] = None) -> str:
        if self.image_path is None:
            raise ValueError("image_path is None")
        if root_dir is None:
            root_dir = "./"
        save_dir = os.path.join(root_dir, CAMPING_SKILL_IMAGE_SAVE_DIR)
        filename = f"camp_skill_{self.id}.png"
        file = os.path.join(save_dir, filename)
        return resize_image_keep_ratio(self.image_path, file, (72, 72))


UNIVERSAL = ("bounty_hunter", "crusader", "vestal", "occultist",
             "hellion", "grave_robber", "highwayman", "plague_doctor",
             "jester", "leper", "arbalest", "man_at_arms",
             "houndmaster", "abomination", "antiquarian", "musketeer")

# AI 生成，可能存在错误，使用前建议检查
encourage = CampingSkill(
    name="encourage",
    cost=2,
    effects=(
        CampingSkillEffect(
            CampingSkillEffectType.STRESS_HEAL_AMOUNT,
            amount=15
        ),
    ),
    hero_classes=UNIVERSAL
)

first_aid = CampingSkill(
    name="first_aid",
    cost=2,
    effects=(
        CampingSkillEffect(
            CampingSkillEffectType.HEALTH_HEAL_MAX_HEALTH_PERCENT,
            amount=0.15
        ),
        CampingSkillEffect(
            CampingSkillEffectType.REMOVE_BLEEDING,
        ),
        CampingSkillEffect(
            CampingSkillEffectType.REMOVE_POISON,
        ),
    ),
    hero_classes=UNIVERSAL
)

pep_talk = CampingSkill(
    name="pep_talk",
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
    name="hobby",
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
    name="field_dressing",
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
    name="marching_plan",
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
    name="restring_crossbow",
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
    name="clean_musket",
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
    name="triage",
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
    name="how_its_done",
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
    name="tracking",
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
    name="planned_takedown",
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
    name="scout_ahead",
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
    name="unshakeable_leader",
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
    name="stand_tall",
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
    name="zealous_speech",
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
    name="zealous_vigil",
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
    name="forage",
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
    name="gallows_humor",
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
    name="night_steps",
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
    name="pilfer",
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
    name="battle_trance",
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
    name="revel",
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
    name="reject_the_gods",
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
    name="sharpen_spear",
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
    name="uncatchable",
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
    name="clean_guns",
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
    name="bandits_sense",
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
    name="maintain_equipment",
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
    name="tactics",
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
    name="instruction",
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
    name="weapons_practice",
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
    name="abandon_hope",
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
    name="dark_ritual",
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
    name="dark_strength",
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
    name="unspeakable_commune",
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
    name="experimental_vapours",
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
    name="leeches",
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
    name="preventative_medicine",
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
    name="self_medicate",
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
    name="bless",
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
    name="chant",
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
    name="pray",
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
    name="sanctuary",
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
    name="turn_back_time",
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
    name="every_rose",
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
    name="tigers_eye",
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
    name="mockery",
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
    name="let_the_mask_down",
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
    name="bloody_shroud",
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
    name="reflection",
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
    name="quarantine",
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
    name="hounds_watch",
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
    name="therapy_dog",
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
    name="pet_the_hound",
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
    name="release_the_hound",
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
    name="anger_management",
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
    name="psych_up",
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
    name="the_quickening",
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
    name="eldritch_blood",
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
    name="supply",
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
    name="trinket_scrounge",
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
    name="strange_powders",
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
    name="curious_incantation",
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
    name="lash_anger",
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
    name="lash_solace",
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
    name="lash_kiss",
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
    name="lash_cure",
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
    print(restring_crossbow.json())

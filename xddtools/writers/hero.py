from dataclasses import dataclass
from typing import Tuple, Union

from xddtools.base import BaseJsonData, BaseWriter
from xddtools.path import HERO_UPGRADE_SAVE_DIR, HERO_UPGRADE_FILE_EXTENSION


@dataclass(frozen=True)
class CurrencyCost:
    amount: int
    type: str = "gold"


@dataclass(frozen=True)
class PrerequisiteRequirement:
    tree_id: str
    requirement_code: str


class HeroUpgradeWriter(BaseJsonData, BaseWriter):
    def __init__(
            self,
            hero_name: str,
            combat_skills: Tuple[str, ...],
            combat_skill_golds: Tuple[Tuple[int, int, int, int, int], ...] = (
                    (1000, 250, 750, 1250, 2500),
            ),
            weapon_golds: Tuple[int, int, int, int] = (750, 1750, 3000, 6000),
            armour_golds: Tuple[int, int, int, int] = (750, 1750, 3000, 6000),
    ):
        if len(combat_skill_golds) != 1 and len(combat_skills) != len(combat_skill_golds):
            raise ValueError("combat_skills and combat_skill_golds must have the same length")
        self.combat_skills = combat_skills
        self.combat_skill_golds = combat_skill_golds
        self.weapon_golds = weapon_golds
        self.armour_golds = armour_golds
        super().__init__(
            name=hero_name,
            items=None,
            relative_save_dir=HERO_UPGRADE_SAVE_DIR,
            extension=HERO_UPGRADE_FILE_EXTENSION
        )

    @staticmethod
    def get_requirement_dict(
            code: int,
            currency_cost: Union[CurrencyCost, Tuple[CurrencyCost, ...]] = (),
            prerequisite_requirements: Union[PrerequisiteRequirement, Tuple[PrerequisiteRequirement, ...]] = (),
            prerequisite_resolve_level: int = 0
    ):
        if isinstance(currency_cost, CurrencyCost):
            currency_cost = [{"type": currency_cost.type, "amount": currency_cost.amount}]
        else:
            currency_cost = [
                {"type": currency_cost.type, "amount": currency_cost.amount}
                for currency_cost in currency_cost
            ]

        if isinstance(prerequisite_requirements, PrerequisiteRequirement):
            prerequisite_requirements = [{
                "tree_id": prerequisite_requirements.tree_id,
                "requirement_code": prerequisite_requirements.requirement_code
            }]
        else:
            prerequisite_requirements = [
                {
                    "tree_id": prerequisite_requirements.tree_id,
                    "requirement_code": prerequisite_requirements.requirement_code
                }
                for prerequisite_requirements in prerequisite_requirements
            ]

        return {
            "code": str(code),
            "currency_cost": currency_cost,
            "prerequisite_requirements": prerequisite_requirements,
            "prerequisite_resolve_level": prerequisite_resolve_level
        }

    def get_equipment_dict(
            self,
            equipment_type: str,
            golds: Tuple[int, int, int, int] = (750, 1750, 3000, 6000)
    ):
        codes = ["a", "b", "c", "d"]
        levels = [1, 2, 3, 5]
        requirements = []
        for i in range(4):
            if i != 0:
                tem = [PrerequisiteRequirement(
                    tree_id=f"{self.id}.{equipment_type}",
                    requirement_code=str(i - 1)
                )]
            else:
                tem = []
            tem.append(PrerequisiteRequirement(
                tree_id=f"blacksmith.{equipment_type}",
                requirement_code=codes[i]
            ))
            requirements.append(self.get_requirement_dict(
                code=i,
                currency_cost=CurrencyCost(amount=golds[i], type="gold"),
                prerequisite_requirements=tuple(tem),
                prerequisite_resolve_level=levels[i]
            ))
        return {
            "id": f"{self.id}.{equipment_type}",
            "is_instanced": True,
            "tags": [equipment_type, "first_level_not_upgrade"],
            "requirements": requirements
        }

    def get_combat_skill_dict(
            self,
            skill_name: str,
            golds: Tuple[int, int, int, int, int] = (1000, 250, 750, 1250, 2500)
    ):
        codes = ["a", "b", "c", "d"]
        levels = [0, 1, 2, 3, 5]
        requirements = []
        for i in range(5):
            if i != 0:
                tem = [
                    PrerequisiteRequirement(
                        tree_id=f"{self.id}.{skill_name}",
                        requirement_code=str(i - 1)
                    ),
                    PrerequisiteRequirement(
                        tree_id="guild.skill_levels",
                        requirement_code=codes[i - 1]
                    )
                ]
            else:
                tem = []
            requirements.append(self.get_requirement_dict(
                code=i,
                currency_cost=CurrencyCost(amount=golds[i], type="gold"),
                prerequisite_requirements=tuple(tem),
                prerequisite_resolve_level=levels[i]
            ))
        return {
            "id": f"{self.id}.{skill_name}",
            "is_instanced": True,
            "tags": ["combat_skill"],
            "requirements": requirements
        }

    def dict(self) -> dict:
        res = [
            self.get_equipment_dict("weapon", self.weapon_golds),
            self.get_equipment_dict("armour", self.armour_golds)
        ]
        if len(self.combat_skill_golds) == 1:
            for skill in self.combat_skills:
                res.append(self.get_combat_skill_dict(skill, self.combat_skill_golds[0]))
        else:
            for skill, gold in zip(self.combat_skills, self.combat_skill_golds):
                res.append(self.get_combat_skill_dict(skill, gold))
        return {"trees": res}

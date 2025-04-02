import os.path
from typing import List, Optional

from xddtools.base import JsonData, BaseWriter, Entry, CampingSkillEntry, get_entry_id
from xddtools.entries import Localization, Bank
from xddtools.entries.camping_skill import CampingSkill
from xddtools.enum import BankDir, BankSource
from xddtools.path import CAMPING_SKILL_SAVE_DIR, CAMPING_SKILL_FILE_EXTENSION, DATA_PATH, CAMPING_SKILL_IMAGE_SAVE_DIR
from xddtools.utils import resize_image_keep_ratio


class CampingSkillWriter(JsonData, BaseWriter):
    def __init__(
            self,
            prefix: str,
            class_specific_number_of_classes_threshold: int = 4
    ):
        super().__init__(
            prefix=prefix,
            relative_save_dir=CAMPING_SKILL_SAVE_DIR,
            extension=CAMPING_SKILL_FILE_EXTENSION
        )
        self._class_specific_number_of_classes_threshold = class_specific_number_of_classes_threshold

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, CampingSkillEntry)

    def add_entry(self, entry: CampingSkill) -> List[Entry]:
        if entry in self._entries:
            return []

        self._entries.append(entry)

        res = []

        if isinstance(entry.sfx, str):
            res.append(Bank(
                bank_dir=BankDir.CAMP_SKILL,
                bank_name=entry.id(),
                audio=entry.sfx,
                source=BankSource.HERO
            ))
        elif isinstance(entry.sfx, Bank):
            res.append(entry.sfx.model_copy(update={
                "bank_dir": BankDir.CAMP_SKILL,
                "bank_name": entry.id(),
                "guid": entry.sfx.guid,
                "audio": entry.sfx.audio,
                "source": BankSource.HERO
            }))

        for hero in entry.hero_classes:
            if isinstance(hero, Entry):
                res.append(hero)
        if entry.effects is not None:
            for effect in entry.effects:
                if isinstance(effect.sub_type, Entry):
                    res.append(effect.sub_type)
                if effect.effect_tooltip is not None:
                    res.append(Localization(
                        entry_id=f"camping_skill_effect_{effect.effect_type.value}_{get_entry_id(effect.sub_type)}",
                        text=effect.effect_tooltip,
                    ))

        if entry.camping_skill_name is not None:
            entry_id = f"camping_skill_name_{entry.id()}"
            res.append(Localization(
                entry_id=entry_id,
                text=entry.camping_skill_name,
            ))
        if entry.str_camping_skill_barks is not None:
            if isinstance(entry.str_camping_skill_barks, str):
                str_camping_skill_barks = [entry.str_camping_skill_barks]
            else:
                str_camping_skill_barks = entry.str_camping_skill_barks
            for bark in str_camping_skill_barks:
                entry_id = f"str_bark_{entry.id()}"
                res.append(Localization(
                    entry_id=entry_id,
                    text=bark
                ))

        return res

    def get_dict(self) -> dict:
        tem = []
        for trait in self._entries:  # type: CampingSkill
            tem.append(trait.get_dict())
        return {
            "configuration": {
                "class_specific_number_of_classes_threshold": self._class_specific_number_of_classes_threshold
            },
            "skills": tem
        }

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        if root_dir is None:
            root_dir = "./"

        res = []

        inner_skills = ['encourage',
                        'first_aid',
                        'pep_talk',
                        'hobby',
                        'field_dressing',
                        'marching_plan',
                        'restring_crossbow',
                        'clean_musket',
                        'triage',
                        'how_its_done',
                        'tracking',
                        'planned_takedown',
                        'scout_ahead',
                        'unshakeable_leader',
                        'stand_tall',
                        'zealous_speech',
                        'zealous_vigil',
                        'forage',
                        'gallows_humor',
                        'night_steps',
                        'pilfer',
                        'battle_trance',
                        'revel',
                        'reject_the_gods',
                        'sharpen_spear',
                        'uncatchable',
                        'clean_guns',
                        'bandits_sense',
                        'maintain_equipment',
                        'tactics',
                        'instruction',
                        'weapons_practice',
                        'abandon_hope',
                        'dark_ritual',
                        'dark_strength',
                        'unspeakable_commune',
                        'experimental_vapours',
                        'leeches',
                        'preventative_medicine',
                        'self_medicate',
                        'bless',
                        'chant',
                        'pray',
                        'sanctuary',
                        'turn_back_time',
                        'every_rose',
                        'tigers_eye',
                        'mockery',
                        'let_the_mask_down',
                        'bloody_shroud',
                        'reflection',
                        'quarantine',
                        'hounds_watch',
                        'therapy_dog',
                        'pet_the_hound',
                        'release_the_hound',
                        'anger_management',
                        'psych_up',
                        'the_quickening',
                        'eldritch_blood',
                        'supply',
                        'trinket_scrounge',
                        'strange_powders',
                        'curious_incantation']

        for entry in self._entries:  # type: CampingSkill
            if entry.camping_skill_image is None and entry.id() not in inner_skills:
                image = os.path.join(DATA_PATH, r"template/hero/unknown_camping_skill.png")
            else:
                image = entry.camping_skill_image
            if image is not None:
                file = os.path.join(root_dir, CAMPING_SKILL_IMAGE_SAVE_DIR, f"camp_skill_{entry.id()}.png")
                res.append(resize_image_keep_ratio(image, file, (72, 72)))

        res.extend(super().export(root_dir))

        return res

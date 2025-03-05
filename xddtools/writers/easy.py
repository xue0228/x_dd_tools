from typing import Any, Iterable, Optional, Tuple, Union

from xddtools.base import get_base_localization_writer, LocalizationWriter
from xddtools.buffs import Buff
from xddtools.camping_skills import CampingSkill
from xddtools.colour import Colour
from xddtools.effects import Effect
from xddtools.enums import LocalizationLanguage, ProjectVisibility, ProjectUploadMode, ProjectTag
from xddtools.items import Item
from xddtools.loot import LootTable
from xddtools.quirks import Quirk
from xddtools.traits import Trait
from xddtools.trinket import TrinketEntry
from xddtools.writers.mod import ProjectWriter
from xddtools.writers.others import BuffWriter, EffectWriter, ItemWriter, QuirkWriter, LootTableWriter, \
    get_base_colour_writer, CampingSkillWriter, TraitWriter, ColourWriter
from xddtools.writers.trinket import Trinket


class DDWriter:
    def __init__(
            self,
            name: str,
            language: LocalizationLanguage = LocalizationLanguage.SCHINESE,
            title: Optional[str] = None,
            preview_icon_file: Optional[str] = None,
            mod_data_path: str = "",
            update_details: str = "",
            visibility: ProjectVisibility = ProjectVisibility.PRIVATE,
            upload_mode: ProjectUploadMode = ProjectUploadMode.DIRECT_UPLOAD,
            version_major: int = 0,
            version_minor: int = 0,
            target_build: int = 0,
            tags: Optional[Iterable[Union[ProjectTag, str]]] = None,
            item_description: str = "",
            item_description_short: str = ""
    ):
        if title is None:
            title = name
        self._project_writer = ProjectWriter(
            title=title,
            preview_icon_file=preview_icon_file,
            mod_data_path=mod_data_path,
            language=language,
            update_details=update_details,
            visibility=visibility,
            upload_mode=upload_mode,
            version_major=version_major,
            version_minor=version_minor,
            target_build=target_build,
            tags=tags,
            item_description=item_description,
            item_description_short=item_description_short
        )

        localization_writer = get_base_localization_writer(name=name, language=language)
        colour_writer = get_base_colour_writer(name=name)
        buff_writer = BuffWriter(name=name, localization_writer=localization_writer)
        effect_writer = EffectWriter(name=name, buff_writer=buff_writer)
        item_writer = ItemWriter(
            name=name,
            effect_writer=effect_writer,
            localization_writer=localization_writer
        )
        quirk_writer = QuirkWriter(
            name=name,
            buff_writer=buff_writer,
            effect_writer=effect_writer,
            item_writer=item_writer,
            localization_writer=localization_writer
        )
        loot_writer = LootTableWriter(name=name, item_writer=item_writer)
        trinket_writer = Trinket(
            name=name,
            buff_writer=buff_writer,
            effect_writer=effect_writer,
            localization_writer=localization_writer,
            is_test=False
        )
        camping_skill_writer = CampingSkillWriter(
            name=name,
            table_writer=loot_writer,
            localization_writer=localization_writer
        )
        trait_writer = TraitWriter(
            name=name,
            buff_writer=buff_writer,
            effect_writer=effect_writer,
            localization_writer=localization_writer
        )

        self._writers = {
            Colour: colour_writer,
            Buff: buff_writer,
            Effect: effect_writer,
            Item: item_writer,
            Quirk: quirk_writer,
            LootTable: loot_writer,
            TrinketEntry: trinket_writer,
            CampingSkill: camping_skill_writer,
            Trait: trait_writer
        }
        self._localization_writer = localization_writer

    @property
    def colour_writer(self) -> ColourWriter:
        return self._writers[Colour]

    @property
    def buff_writer(self) -> BuffWriter:
        return self._writers[Buff]

    @property
    def effect_writer(self) -> EffectWriter:
        return self._writers[Effect]

    @property
    def item_writer(self) -> ItemWriter:
        return self._writers[Item]

    @property
    def quirk_writer(self) -> QuirkWriter:
        return self._writers[Quirk]

    @property
    def loot_writer(self) -> LootTableWriter:
        return self._writers[LootTable]

    @property
    def trinket_writer(self) -> Trinket:
        return self._writers[TrinketEntry]

    @property
    def camping_skill_writer(self) -> CampingSkillWriter:
        return self._writers[CampingSkill]

    @property
    def trait_writer(self) -> TraitWriter:
        return self._writers[Trait]

    @property
    def localization_writer(self) -> LocalizationWriter:
        return self._localization_writer

    @property
    def project_writer(self) -> ProjectWriter:
        return self._project_writer

    def add_item(self, item: Any):
        if type(item) in self._writers:
            self._writers[type(item)].add_item(item)
        else:
            if isinstance(item, tuple) and len(item) == 2:
                self._localization_writer.add_entry(item[0], item[1])
            else:
                raise TypeError(f"{type(item)} is not supported.")

    def add_items(self, items: Iterable[Any]):
        for item in items:
            self.add_item(item)

    def export(self, root_dir: Optional[str] = None) -> Tuple[str, ...]:
        tem = self._project_writer.export(root_dir)
        res = list(tem)
        for _, writer in self._writers.items():
            if len(writer) > 0:
                tem = writer.export(root_dir)
                if isinstance(tem, tuple):
                    res.extend(list(tem))
                else:
                    res.append(tem)

        if len(self._localization_writer) > 0:
            res.append(self._localization_writer.export(root_dir))
        return tuple(res)

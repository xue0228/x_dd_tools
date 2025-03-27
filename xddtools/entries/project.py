import xml.etree.ElementTree as ET
from typing import Optional, Sequence, Union
from xml.dom import minidom

from pydantic import BaseModel, ConfigDict, Field, field_validator

from xddtools.base import ProjectEntry, get_entry_id
from xddtools.enum.localization import LocalizationLanguage
from xddtools.enum.project import ProjectVisibility, ProjectUploadMode, ProjectTag
from xddtools.name import AutoName
from xddtools.utils import is_image


class Project(ProjectEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    title: str
    preview_icon_image: Optional[str] = None
    mod_data_path: str = ""
    language: LocalizationLanguage = LocalizationLanguage.SCHINESE
    update_details: str = ""
    visibility: ProjectVisibility = ProjectVisibility.PRIVATE
    upload_mode: ProjectUploadMode = ProjectUploadMode.DIRECT_UPLOAD
    version_major: int = 0
    version_minor: int = 0
    target_build: int = 0
    tags: Sequence[Union[ProjectTag, str]] = Field(default_factory=list)
    item_description: str = Field("", max_length=8000)
    item_description_short: str = Field("", max_length=512)

    entry_id: str = Field(default_factory=lambda x: AutoName().new_project(), frozen=True)

    @field_validator("preview_icon_image")
    @classmethod
    def _check_preview_icon_image(cls, v: str):
        if (v is not None) and (not is_image(v)):
            raise ValueError(f"{v} is not a valid image path")
        return v

    def __str__(self):
        # 创建根元素
        project = ET.Element('project')

        # 添加子元素
        ET.SubElement(project, 'ItemDescriptionShort').text = self.item_description_short
        ET.SubElement(project, 'ModDataPath').text = self.mod_data_path
        ET.SubElement(project, 'Title').text = self.title
        ET.SubElement(project, 'Language').text = self.language.value
        ET.SubElement(project, 'UpdateDetails').text = self.update_details
        ET.SubElement(project, 'Visibility').text = self.visibility.value
        ET.SubElement(project, 'UploadMode').text = self.upload_mode.value
        ET.SubElement(project, 'VersionMajor').text = str(self.version_major)
        ET.SubElement(project, 'VersionMinor').text = str(self.version_minor)
        ET.SubElement(project, 'TargetBuild').text = str(self.target_build)

        # 创建'Tags'节点并添加其子节点
        tags = ET.SubElement(project, 'Tags')
        for tag in self.tags:
            ET.SubElement(tags, 'Tags').text = get_entry_id(tag)

        # 添加最后一个子元素
        ET.SubElement(project, 'ItemDescription').text = self.item_description

        # 将ElementTree对象转换为字符串
        rough_string = ET.tostring(project, encoding='unicode')

        # 使用minidom解析字符串，并进行美化
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ", newl="\n", encoding="utf-8")

        return pretty_xml.decode()


if __name__ == '__main__':
    p = Project(title="猎人饰品", tags=[ProjectTag.TRINKETS, ProjectTag.OVERHAULS, "test"])
    print(p)

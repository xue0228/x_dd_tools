import os.path
import xml.etree.ElementTree as ET
from typing import Optional, Iterable, Union, Tuple
from xml.dom import minidom

from xddtools.enums import LocalizationLanguage, ProjectVisibility, ProjectUploadMode, ProjectTag
from xddtools.path import DATA_PATH
from xddtools.utils import is_image, make_dirs, resize_image_keep_ratio


class ProjectWriter:
    def __init__(
            self,
            title: str,
            preview_icon_file: Optional[str] = None,
            mod_data_path: str = "",
            language: LocalizationLanguage = LocalizationLanguage.SCHINESE,
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
        if len(item_description_short) > 512:
            raise ValueError("item_description_short must be less than or equal to 512 characters")
        if len(item_description) > 8000:
            raise ValueError("item_description must be less than or equal to 8000 characters")

        if preview_icon_file is None:
            preview_icon_file = os.path.join(DATA_PATH, "template/project/preview_icon.png")
        if not is_image(preview_icon_file):
            raise ValueError(f"{preview_icon_file} is not a image")

        self._title = title
        self._preview_icon_file = preview_icon_file
        self._mod_data_path = mod_data_path
        self._language = language
        self._update_details = update_details
        self._visibility = visibility
        self._upload_mode = upload_mode
        self._version_major = version_major
        self._version_minor = version_minor
        self._target_build = target_build
        self._tags = tags or []
        self._item_description = item_description
        self._item_description_short = item_description_short

    def __str__(self):
        # 创建根元素
        project = ET.Element('project')

        # 添加子元素
        ET.SubElement(project, 'ItemDescriptionShort').text = self._item_description_short
        ET.SubElement(project, 'ModDataPath').text = self._mod_data_path
        ET.SubElement(project, 'Title').text = self._title
        ET.SubElement(project, 'Language').text = self._language.value
        ET.SubElement(project, 'UpdateDetails').text = self._update_details
        ET.SubElement(project, 'Visibility').text = self._visibility.value
        ET.SubElement(project, 'UploadMode').text = self._upload_mode.value
        ET.SubElement(project, 'VersionMajor').text = str(self._version_major)
        ET.SubElement(project, 'VersionMinor').text = str(self._version_minor)
        ET.SubElement(project, 'TargetBuild').text = str(self._target_build)

        # 创建'Tags'节点并添加其子节点
        tags = ET.SubElement(project, 'Tags')
        for tag in self._tags:
            ET.SubElement(tags, 'Tags').text = tag

        # 添加最后一个子元素
        ET.SubElement(project, 'ItemDescription').text = self._item_description

        # 将ElementTree对象转换为字符串
        rough_string = ET.tostring(project, encoding='unicode')

        # 使用minidom解析字符串，并进行美化
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ", newl="\n", encoding="utf-8")

        return pretty_xml.decode()

    def export(self, root_dir: Optional[str] = None) -> Tuple[str, ...]:
        if root_dir is None:
            root_dir = "./"
        file = os.path.join(root_dir, "project.xml")
        make_dirs(os.path.dirname(file))
        with open(file, 'w', encoding='utf-8') as f:
            f.write(str(self))
        file2 = os.path.join(root_dir, "preview_icon.png")
        resize_image_keep_ratio(self._preview_icon_file, file2, (512, 512))
        return os.path.normpath(file), os.path.normpath(file2)


if __name__ == '__main__':
    p = ProjectWriter("test")
    p.export("t")

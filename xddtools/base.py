import abc
import html
import json
import os
import subprocess
from typing import Optional, Tuple, Dict, Union, List
from xml.dom import minidom

from xddtools.enums import LocalizationLanguage
from xddtools.path import LOCALIZATION_FILE_EXTENSION, LOCALIZATION_SAVE_DIR, LOCALIZE_PATH
from xddtools.utils import make_dirs


class BaseID:
    def __init__(
            self,
            name: str,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        if len(name) > 64:
            raise ValueError(f"{name} is too long,max is 64")
        self._name = name

    @property
    def id(self) -> str:
        return self._name


class BaseLocalization(BaseID):
    def __init__(
            self,
            name: str,
            localization: Union[Tuple[str, ...], str, None],
            entry_id_prefix: Union[Tuple[str, ...], str, None],
            *args, **kwargs
    ):
        if not isinstance(localization, (Tuple, List)):
            localization = (localization,)
        if not isinstance(entry_id_prefix, (Tuple, List)):
            entry_id_prefix = (entry_id_prefix,)

        self._localization = localization
        self._entry_id_prefix = entry_id_prefix
        super().__init__(name, *args, **kwargs)  # 如果有更多超类，继续调用

    @property
    def localization_id(self) -> Optional[str]:
        return self.id

    @property
    def entries(self) -> Tuple[Tuple[str, str]]:
        res = []
        entry_id_prefixs = []
        len_loc = len(self._localization)
        len_ent = len(self._entry_id_prefix)
        if len_loc > len_ent:
            for i in range(len_loc):
                if i < len_ent:
                    entry_id_prefixs.append(self._entry_id_prefix[i])
                else:
                    entry_id_prefixs.append(self._entry_id_prefix[-1])
        else:
            entry_id_prefixs = self._entry_id_prefix

        for localization, entry_id_prefix in zip(self._localization, entry_id_prefixs):
            if entry_id_prefix is not None and localization is not None and self.localization_id is not None:
                res.append((f"{entry_id_prefix}{self.localization_id}", localization))
        return tuple(res)


class BaseJsonData(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def dict(self) -> Dict:
        pass

    def json(self) -> str:
        return json.dumps(self.dict(), ensure_ascii=True, indent=2)

    def __str__(self):
        return self.json() + "\n"


class LocalizationWriter(BaseID):
    def __init__(
            self,
            name: str,
            language: LocalizationLanguage = LocalizationLanguage.SCHINESE,
    ):
        self.language = language
        self.entries = []
        super().__init__(name=name)

    def add_entry(self, entry_id: str, entry_text: str):
        tem = (entry_id, entry_text)
        if tem not in self.entries:
            self.entries.append(tem)

    def add_entries(self, entries: Tuple[Tuple[str, str]]):
        for entry_id, entry_text in entries:
            self.add_entry(entry_id, entry_text)

    def __len__(self):
        return len(self.entries)

    def export(self, root_dir: Optional[str] = None) -> str:
        if root_dir is None:
            root_dir = "./"

        doc = minidom.Document()
        # 创建根元素
        root = doc.createElement("root")
        doc.appendChild(root)
        # 创建子元素 - language
        if self.language != LocalizationLanguage.ENGLISH:
            english = doc.createElement("language")
            english.setAttribute("id", LocalizationLanguage.ENGLISH.value)
            root.appendChild(english)
        language = doc.createElement("language")
        language.setAttribute("id", self.language.value)
        root.appendChild(language)

        for entry_id, entry_text in self.entries:
            entry = doc.createElement("entry")
            entry.setAttribute("id", entry_id)
            # 手动构建CDATA部分并设置为元素的文本内容
            entry_text = entry_text.replace("}\n", "} \n")
            entry_text_with_cdata = f"<![CDATA[{entry_text}]]>"
            text_node = doc.createTextNode(entry_text_with_cdata)
            entry.appendChild(text_node)
            language.appendChild(entry)

        # 将DOM树转换为字符串
        rough_string = doc.toprettyxml(indent="  ", encoding="utf-8")
        # 解码HTML实体
        decoded_string = html.unescape(rough_string.decode("utf-8"))
        # 写入文件
        file_name = f"{self.id}_{self.language.value}{LOCALIZATION_FILE_EXTENSION}"
        output_path = os.path.join(root_dir, LOCALIZATION_SAVE_DIR, file_name)
        make_dirs(os.path.dirname(output_path))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(decoded_string)
        self.xml_to_loc2(output_path)
        return os.path.normpath(output_path)

    @staticmethod
    def xml_to_loc2(xml_path):
        process = subprocess.Popen(
            [LOCALIZE_PATH],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(xml_path)
        )
        err = process.stderr.read()
        if err != "":
            raise RuntimeError(f"{err}")
        info = process.stdout.read()
        if "SUCCESS!" not in info:
            raise RuntimeError(f"{info}")
        for file in os.listdir(os.path.dirname(xml_path)):
            if file.endswith(".loc2"):
                name = os.path.split(xml_path)[1]
                name = name.split(".")[0].split("_")[:-1]
                name.append(file)
                name = "_".join(name)
                os.rename(
                    os.path.join(os.path.dirname(xml_path), file),
                    os.path.join(os.path.dirname(xml_path), name)
                )


class BaseWriter(BaseID, metaclass=abc.ABCMeta):
    def __init__(
            self,
            name: str,
            items: Optional[Tuple[BaseID, ...]],
            relative_save_dir: str,
            extension: str,
            localization_writer: Optional[LocalizationWriter] = None,
            *args, **kwargs
    ):
        super().__init__(name, *args, **kwargs)

        self._relative_save_dir = relative_save_dir
        self._extension = extension
        self._items = []
        self._localization_writer = localization_writer

        if items is None:
            items = []
        self.add_items(items)

    def add_item(
            self,
            item: BaseID
    ):
        if item in self._items:
            return item.id
        self._items.append(item)
        if self._localization_writer is not None and isinstance(item, BaseLocalization):
            self._localization_writer.add_entries(item.entries)
        return item.id

    def add_items(
            self,
            items: Tuple[BaseID, ...]
    ):
        for item in items:
            self.add_item(item)

    def __len__(self):
        return len(self._items)

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    def export(self, root_dir: Optional[str] = None) -> str:
        if root_dir is None:
            root_dir = "./"
        file = os.path.join(root_dir, self._relative_save_dir, f"{self.id}{self._extension}")
        make_dirs(os.path.dirname(file))
        with open(file, 'w', encoding='utf-8') as f:
            f.write(str(self))
        return os.path.normpath(file)


def get_base_localization_writer(
        name: str,
        language: LocalizationLanguage = LocalizationLanguage.SCHINESE,
) -> LocalizationWriter:
    from xddtools.colour import bleed, blight, stress, heal_hp
    localization_writer = LocalizationWriter(name, language)
    base_entries = {
        "buff_stat_tooltip_ambush_chance": f"%+d%%被怪物夜袭概率",

        "buff_stat_tooltip_disable_combat_skill_attribute_heal": "禁用治疗技能",
        "buff_stat_tooltip_disable_combat_skill_attribute_buff": "禁用增益技能",
        "buff_stat_tooltip_disable_combat_skill_attribute_debuff": "禁用减益技能",
        "buff_stat_tooltip_disable_combat_skill_attribute_bleed": "禁用流血技能",
        "buff_stat_tooltip_disable_combat_skill_attribute_poison": "禁用腐蚀技能",
        "buff_stat_tooltip_disable_combat_skill_attribute_stun": "禁用眩晕技能",
        "buff_stat_tooltip_disable_combat_skill_attribute_tag": "禁用标记技能",
        "buff_stat_tooltip_disable_combat_skill_attribute_stress": "禁用压力技能",
        "buff_stat_tooltip_disable_combat_skill_attribute_move": "禁用位移技能",
        "buff_stat_tooltip_disable_combat_skill_attribute_disease": "禁用疾病技能",
        "buff_stat_tooltip_disable_combat_skill_attribute_guard": "禁用守护技能",
        "buff_stat_tooltip_disable_combat_skill_attribute_daze": "禁用迷乱技能",

        "buff_stat_tooltip_hp_dot_bleed_amount_percent": f"%+d%%施加的{bleed('流血')}量",
        "buff_stat_tooltip_hp_dot_poison_amount_percent": f"%+d%%施加的{blight('腐蚀')}量",
        "buff_stat_tooltip_stress_dot_amount_percent": f"%+d%%施加的{stress('恐惧')}量",
        "buff_stat_tooltip_hp_heal_dot_amount_percent": f"%+d%%施加的{heal_hp('愈合')}量",

        "buff_stat_tooltip_hp_dot_bleed_amount_received_percent": f"%+d%%所受的{bleed('流血')}量",
        "buff_stat_tooltip_hp_dot_poison_amount_received_percent": f"%+d%%所受的{blight('腐蚀')}量",
        "buff_stat_tooltip_stress_dot_amount_received_percent": f"%+d%%所受的{stress('恐惧')}量",
        "buff_stat_tooltip_hp_heal_dot_amount_received_percent": f"%+d%%所受的{heal_hp('愈合')}量",

        "buff_stat_tooltip_hp_dot_bleed_duration_percent": f"%+d%%施加的{bleed('流血')}时间",
        "buff_stat_tooltip_hp_dot_poison_duration_percent": f"%+d%%施加的{blight('腐蚀')}时间",
        "buff_stat_tooltip_stress_dot_duration_percent": f"%+d%%施加的{stress('恐惧')}时间",
        "buff_stat_tooltip_hp_heal_dot_duration_percent": f"%+d%%施加的{heal_hp('愈合')}时间",

        "buff_stat_tooltip_hp_dot_bleed_duration_received_percent": f"%+d%%所受的{bleed('流血')}时间",
        "buff_stat_tooltip_hp_dot_poison_duration_received_percent": f"%+d%%所受的{blight('腐蚀')}时间",
        "buff_stat_tooltip_stress_dot_duration_received_percent": f"%+d%%所受的{stress('恐惧')}时间",
        "buff_stat_tooltip_hp_heal_dot_duration_received_percent": f"%+d%%所受的{heal_hp('愈合')}时间",
    }
    for k, v in base_entries.items():
        localization_writer.add_entry(k, v)
    return localization_writer


if __name__ == '__main__':
    bl = BaseLocalization(
        name="category",
        prefix="p",
        localization=(
            "test",
            "test2",
        ),
        entry_id_prefix="pre",
    )
    print(bl.entries)

import html
import os.path
from typing import List, Optional
from xml.dom import minidom

from xddtools.base import BaseWriter, Entry, LocalizationEntry
from xddtools.entries.localization import Localization
from xddtools.enum.localization import LocalizationLanguage
from xddtools.path import LOCALIZATION_SAVE_DIR, LOCALIZATION_FILE_EXTENSION, LOCALIZE_PATH
from xddtools.utils import process_exe, write_str_to_file


class LocalizationWriter(BaseWriter):
    def __init__(
            self,
            prefix: str,
            language: LocalizationLanguage = LocalizationLanguage.SCHINESE
    ):
        super().__init__(
            prefix=prefix,
            relative_save_dir=LOCALIZATION_SAVE_DIR,
            extension=LOCALIZATION_FILE_EXTENSION
        )
        self.language = language

    def is_valid(self, entry: Entry) -> bool:
        return isinstance(entry, LocalizationEntry)

    def add_entry(self, entry: Localization) -> List[Entry]:
        self._entries.append(entry)
        return []

    def __str__(self):
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

        for localization_entry in self._entries:  # type: Localization
            entry_id, entry_text = localization_entry.id(), localization_entry.text
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

        return decoded_string

    @staticmethod
    def _xml_to_loc2(xml_path: str) -> List[str]:
        info, err = process_exe(
            exe_path=LOCALIZE_PATH,
            args=[xml_path],
            cwd=os.path.dirname(xml_path)
        )

        # dd 自带的汉化程序在运行后会莫名其妙生成一个空的 data 文件夹，这里手动删除
        tem_data_dir = os.path.dirname(os.path.abspath(xml_path))
        tem_data_dir = os.path.dirname(tem_data_dir)
        tem_data_dir = os.path.dirname(tem_data_dir)
        tem_data_dir = os.path.dirname(tem_data_dir)
        tem_data_dir = os.path.dirname(tem_data_dir)
        tem_data_dir = os.path.join(tem_data_dir, "data")
        if os.path.isdir(tem_data_dir) and not os.listdir(tem_data_dir):
            os.rmdir(tem_data_dir)

        if err != "":
            raise RuntimeError(f"{err}")
        if "SUCCESS!" not in info:
            raise RuntimeError(f"{info}")

        res = []
        for file in os.listdir(os.path.dirname(xml_path)):
            if file.endswith(".loc2") and file[:-5] in [item.value for item in LocalizationLanguage]:
                name = os.path.split(xml_path)[1]
                name = name.split(".")[0].split("_")[:-1]
                name.append(file)
                name = "_".join(name)
                src = os.path.join(os.path.dirname(xml_path), file)
                dst = os.path.join(os.path.dirname(xml_path), name)
                if os.path.exists(dst):
                    os.remove(dst)
                os.rename(src, dst)
                res.append(os.path.normpath(dst))
        return res

    def export(self, root_dir: Optional[str] = None) -> List[str]:
        if root_dir is None:
            root_dir = "./"
        file = os.path.join(root_dir, self._relative_save_dir, f"{self.prefix}_{self.language.value}{self._extension}")
        res = [write_str_to_file(file, str(self))]
        res.extend(self._xml_to_loc2(res[-1]))
        return res


def get_localization_writer(
        prefix: str,
        language: LocalizationLanguage = LocalizationLanguage.SCHINESE,
) -> LocalizationWriter:
    from xddtools.entries.colour import bleed, blight, stress, heal_hp
    localization_writer = LocalizationWriter(prefix, language)
    base_entries = {
        "buff_rule_tooltip_target_hpabove": f"%s如果目标生命值高于%d%%",

        "str_ui_actor_dot_complete": "",  # 所有actor_dot完成时共用的文本显示，此处这样设置会使女伯爵的egg破裂时没有文本提示

        "buff_stat_tooltip_ambush_chance": f"%+d%%被怪物夜袭概率",

        "buff_stat_tooltip_hp_heal_received_percent_damage_heal": f"%+d%%偷取的{heal_hp('治疗')}量",

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
        localization_writer.add_entry(Localization(
            entry_id=k,
            text=v,
        ))
    return localization_writer

import glob
import json
import os
import shutil
from typing import Optional, List, Dict

import numpy as np
from pydantic import BaseModel, ConfigDict, field_validator
from pydub import AudioSegment

from xddtools.base import BankEntry, JsonData
from xddtools.enum.bank import BankDir, BankSource
from xddtools.path import BANK_PATH
from xddtools.utils import process_exe, make_dirs


class AudioProcessor:
    @staticmethod
    def is_audio(file_path: str) -> bool:
        """
        判断目标文件是否为支持的音频文件。
        :param file_path: 文件路径
        :return: 如果是支持的音频文件，返回 True；否则返回 False
        """
        if not os.path.isfile(file_path):
            return False

        try:
            # 尝试加载音频文件以验证其有效性
            audio = AudioSegment.from_file(file_path)
            if audio:
                return True
        except:
            return False

    @staticmethod
    def calculate_and_adjust_db(
            input_path: str,
            output_path: str,
            target_db: Optional[float] = -1,
            adjust_type: str = "max",
            target_ar: int = 44100
    ) -> float:
        """
        计算并调整音频文件的分贝值。
        :param input_path: 音频文件路径
        :param output_path:
        :param target_db: 目标分贝值（如果为 None，则仅计算而不调整）
        :param adjust_type: 调整类型，可选 "average"（平均分贝）或 "max"（最高分贝）
        :param target_ar:
        :return: 调整后的分贝值
        """
        # 加载音频文件
        audio = AudioSegment.from_file(input_path)

        # 将音频数据转换为 numpy 数组
        samples = np.array(audio.get_array_of_samples())
        if audio.channels > 1:  # 如果是多声道，取平均值
            samples = samples.reshape((-1, audio.channels)).mean(axis=1)

        if adjust_type == "average":
            sample = np.mean(samples)
        elif adjust_type == "max":
            sample = np.max(samples)
        else:
            raise ValueError("无效的调整类型")

        # 计算当前分贝值（RMS 转换为 dBFS）
        current_db = 20 * np.log10(sample / (2 ** (audio.sample_width * 8 - 1)))

        if target_db is None:
            adjusted_audio = audio
        else:
            # 计算需要调整的增益值
            gain_db = target_db - current_db
            # 应用增益
            adjusted_audio = audio + gain_db
            current_db = target_db
        # 保存调整后的音频文件
        make_dirs(os.path.dirname(output_path))
        adjusted_audio.export(
            output_path,
            format=os.path.splitext(input_path)[1][1:],
            parameters=["-ar", str(target_ar)]
        )

        # 返回调整后的分贝值
        return current_db


class BankExtractor:
    def __init__(self):
        self._quick_bms = os.path.join(BANK_PATH, "quickbms.exe")
        self._fsb_aud_extractor = os.path.join(BANK_PATH, "fsb_aud_extr.exe")
        self._script_bms = os.path.join(BANK_PATH, "Script.bms")
        self._tem_dir = os.path.join(BANK_PATH, "tem")

    def extract(self, bank_path: str, output_dir: Optional[str] = None) -> List[str]:
        if output_dir is None:
            output_dir = self._tem_dir
        process_exe(self._quick_bms, ["-Y", "-o", self._script_bms, bank_path, output_dir])
        fsb_file = "00000000.fsb"
        info, err = process_exe(self._fsb_aud_extractor, [fsb_file], cwd=output_dir)
        if err != "":
            raise RuntimeError(err)

        res = glob.glob(os.path.join(output_dir, "*.wav"))
        res = [os.path.split(x)[-1] for x in res]

        if output_dir == self._tem_dir:
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)

        return res


_audio_processor = AudioProcessor()
_bank_extractor = BankExtractor()


class Bank(JsonData, BankEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    bank_dir: BankDir = BankDir.CHAR_ALLY
    bank_name: str = ""
    guid: str = ""
    audio: Optional[str] = None,
    source: BankSource = BankSource.HERO

    @field_validator("audio")
    @classmethod
    def _check_audio(cls, v: str):
        if (v is not None) and (not _audio_processor.is_audio(v)):
            raise ValueError(f"{v} is not a valid audio path")
        return v

    def id(self) -> str:
        return f"{self.bank_dir.value}/{self.bank_name}"

    def get_dict(self) -> dict:
        return {
            "event_id": f"event:{self.id()}",
            "guid_override": self.guid,
        }


def fill_guid_overrides(
        bank_path: str,
        json_path: str
) -> Dict:
    search_map = {}
    tem = _bank_extractor.extract(bank_path)
    for item in tem:
        tem2 = item.split(" ")
        value = tem2[-1].rstrip(".wav")
        key = " ".join(tem2[:-1])
        search_map[key] = value

    with open(json_path, 'r', encoding='utf-8') as f:
        d = json.load(f)

    res = []
    for item in d["event_guid_overrides"]:
        key = item["event_id"].split("/")[-1]
        if key in search_map:
            value = search_map[key]
        else:
            value = ""
        res.append({"event_id": item["event_id"], "guid_override": value})
    res = {"event_guid_overrides": res}
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    return res


if __name__ == '__main__':
    print(fill_guid_overrides(
        r"D:\Users\Desktop\x_dd_tools\examples\xjiangshi\xjiangshi\audio\secondary_banks\xjiangshi.bank",
        r"D:\Users\Desktop\x_dd_tools\examples\xjiangshi\xjiangshi\audio\xjiangshi.campaign.guid_overrides.json"
    ))


    # bank = r"D:\Users\Desktop\x_dd_tools\examples\xjiangshi\audio\hero_jiangshi.bank"
    # output = r"D:\Users\Desktop\x_dd_tools\examples\xjiangshi\audio"
    #
    # extractor = BankExtractor()
    # result = extractor.extract(bank, output)
    # print(result)

    # processor = AudioProcessor()
    #
    # # 测试音频文件
    # file_path = "test.wav"
    #
    # # 判断是否为音频文件
    # if processor.is_audio(file_path):
    #     print("这是一个有效的音频文件！")
    #
    #     # 计算并调整分贝值
    #     adjusted_db = processor.calculate_and_adjust_db(file_path, "test_2.mp3", target_ar=44100)
    #     print(f"调整后的分贝值: {adjusted_db} dB")

import json
import os
import re
import shutil
import subprocess
from typing import Callable, Optional

from xddtools.base import BaseID
from xddtools.path import CONVERTER_PATH
from xddtools.utils import make_dirs


class Animation(BaseID):
    def __init__(
            self,
            anim_dir: str,
            anim_name: str,
    ):
        self.anim_dir = anim_dir
        self.skel_path, self.atlas_path, self.png_path, self.json_path = self.get_filepaths()
        if self.json_path is None:
            self.json_path = self.skel_to_json(self.skel_path)
        super().__init__(name=anim_name)

    def get_filepaths(self):
        skel = []
        atlas = []
        png = []
        json_list = []
        for file in os.listdir(self.anim_dir):
            if file.endswith(".skel"):
                skel.append(file)
            elif file.endswith(".atlas"):
                atlas.append(file)
            elif file.endswith(".png"):
                png.append(file)
            elif file.endswith(".json"):
                json_list.append(file)

        if len(skel) != 1:
            raise ValueError(f"Expected 1 .skel file, but now get {skel}")
        if len(atlas) != 1:
            raise ValueError(f"Expected 1 .atlas file, but now get {atlas}")
        if len(png) != 1:
            raise ValueError(f"Expected 1 .png file, but now get {png}")
        if len(json_list) > 1:
            raise ValueError(f"Expected 0 or 1 .json file, but now get {json_list}")
        if skel[0][:-5] != atlas[0][:-6]:
            raise ValueError(f"File names are not equal: {skel[0]}, {atlas[0]}")

        return (
            os.path.join(self.anim_dir, skel[0]),
            os.path.join(self.anim_dir, atlas[0]),
            os.path.join(self.anim_dir, png[0]),
            None if len(json_list) == 0 else os.path.join(self.anim_dir, json_list[0])
        )

    @property
    def animations(self):
        return tuple([key for key in self.load_json(self.json_path)["animations"].keys()])

    @staticmethod
    def skel_to_json(skel_path):
        process = subprocess.Popen(
            [CONVERTER_PATH, skel_path],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        err = process.stderr.read()
        if err != "":
            raise RuntimeError(f"{err}")
        return os.path.normpath(os.path.splitext(skel_path)[0] + ".json")

    @staticmethod
    def json_to_skel(json_path):
        process = subprocess.Popen(
            [CONVERTER_PATH, json_path],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        err = process.stderr.read()
        if err != "":
            raise RuntimeError(f"{err}")
        return os.path.normpath(os.path.splitext(json_path)[0] + ".skel")

    @staticmethod
    def load_json(json_path: str):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_json(data, json_path: str):
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=True, indent=2)

    def copy_and_rename_atlas(self, dir_path: str, new_name: str):
        make_dirs(dir_path)
        new_path = os.path.join(dir_path, new_name + ".atlas")
        shutil.copy2(self.atlas_path, new_path)
        with open(new_path, 'r', encoding='utf-8') as f:
            data = f.read()
        pattern = r'^(.*?)\.png$'
        result = re.sub(pattern, new_name + ".png", data, count=1, flags=re.MULTILINE)
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(result)
        return os.path.normpath(new_path)

    def copy_and_rename_png(self, dir_path: str, new_name: str):
        make_dirs(dir_path)
        new_path = os.path.join(dir_path, new_name + ".png")
        shutil.copy2(self.png_path, new_path)
        return os.path.normpath(new_path)

    def copy_and_rename_skel(self, dir_path: str, new_name: str, dict_func: Optional[Callable[[dict], dict]] = None):
        d = self.load_json(self.json_path)
        if dict_func is not None:
            d = dict_func(d)
        make_dirs(dir_path)
        new_path = os.path.join(dir_path, new_name + ".json")
        self.save_json(d, new_path)
        self.json_to_skel(new_path)
        os.remove(new_path)
        return os.path.normpath(new_path)

    def copy_and_rename_animation(
            self,
            root_dir: str,
            anim_name: Optional[str] = None,
            dict_func: Optional[Callable[[dict], dict]] = None,
            is_fx: bool = True,
            is_global: bool = False,
            hero_name: Optional[str] = None,
            hero_sub_type: Optional[str] = None,
            monster_name: Optional[str] = None,
    ):
        if anim_name is None:
            anim_name = self.id
        if anim_name is None:
            raise ValueError("anim_name is None")
        if is_global and not is_fx:
            raise ValueError("no global anim,is_fx must be True when is_global is True")

        res = []
        if is_global:
            dir_path = os.path.join(root_dir, "fx", anim_name)
            new_name = f"{anim_name}.sprite"
            res.append(self.copy_and_rename_skel(dir_path, new_name, dict_func))
            res.append(self.copy_and_rename_atlas(dir_path, new_name))
            res.append(self.copy_and_rename_png(dir_path, new_name))
            return tuple(res)

        if hero_name is not None:
            new_name = f"{hero_name}.sprite.{anim_name}"
            dir_path = os.path.join(root_dir, "heroes", hero_name)
            if is_fx:
                dir_path = os.path.join(dir_path, "fx")
                res.append(self.copy_and_rename_skel(dir_path, new_name, dict_func))
                res.append(self.copy_and_rename_atlas(dir_path, new_name))
                res.append(self.copy_and_rename_png(dir_path, new_name))
                return tuple(res)

            anim_dir_path = os.path.join(dir_path, "anim")
            res.append(self.copy_and_rename_skel(anim_dir_path, new_name, dict_func))
            res.append(self.copy_and_rename_atlas(anim_dir_path, new_name))

            if hero_sub_type is None:
                png_dir_path = [os.path.join(dir_path, f"{hero_name}_{item}", "anim") for item in [
                    "A",
                    # "B", "C", "D"
                ]]
            else:
                png_dir_path = [os.path.join(dir_path, f"{hero_name}_{hero_sub_type.upper()}", "anim")]
            for item in png_dir_path:
                res.append(self.copy_and_rename_png(item, new_name))
            return tuple(res)

        if monster_name is not None:
            new_name = f"{monster_name}.sprite.{anim_name}"
            if is_fx:
                dir_path = os.path.join(root_dir, "monsters", monster_name, "fx")
            else:
                dir_path = os.path.join(root_dir, "monsters", monster_name, "anim")
            res.append(self.copy_and_rename_skel(dir_path, new_name, dict_func))
            res.append(self.copy_and_rename_atlas(dir_path, new_name))
            res.append(self.copy_and_rename_png(dir_path, new_name))
            return tuple(res)

        raise ValueError("is_global,hero_name and monster_name cannot be False or None at the same time")


if __name__ == '__main__':
    # pass
    # print(CONVERTER_PATH)
    #
    from xddtools.path import DATA_PATH

    name = "riposte_2"

    def func(d: dict) -> dict:
        keys = list(d["animations"].keys())
        d["animations"][name] = d["animations"]["riposte_remi_blood_moon"]
        for key in keys:
            del d["animations"][key]
        return d

    a = Animation(
        r"D:\Users\Desktop\x_dd_tools\xddtools\data\template\skill\enemy_2\targheadfx",
        name
    )
    print(a.animations)
    # a.copy_and_rename_animation(
    #     os.path.join(DATA_PATH, "template", "anim"),
    #     name,
    #     is_global=True,
    #     dict_func=func
    # )
    # b = Animation(
    #     os.path.join(r"D:\Users\Desktop\x_dd_tools\xddtools\data\template\anim\fx", name),
    #     name
    # )
    # print(b.animations)

    # a.copy_and_rename_animation(os.path.join(DATA_PATH, "mod_test"), "combat", is_fx=True, hero_name="yiwei")

    # a.copy_and_rename_animation(os.path.join(DATA_PATH, "mod_test"), "yiwei", is_global=True)

    # a.copy_and_rename_atlas(os.path.join(DATA_PATH, "xue"), "yiwei")

    # x = a.json()
    # x["animations"]["walk"] = x["animations"]["walk_remi_c_moon"]
    # del x["animations"]["walk_remi_c_moon"]
    # del x["animations"]["walk_remi_tooltip"]
    # a.save_json(x)
    # print(a)

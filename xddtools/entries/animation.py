import os
import re
import shutil
from typing import Optional, Union, Callable, List, Sequence

from pydantic import BaseModel, ConfigDict, Field, model_validator

from xddtools.base import AnimationEntry, ModeEntry, HeroEntry, MonsterEntry, get_entry_id
from xddtools.name import AutoName
from xddtools.path import CONVERTER_PATH, HERO_SAVE_DIR, MONSTER_SAVE_DIR
from xddtools.utils import process_exe, make_dirs, get_rename_skel_dict_func, save_json, load_json


class Animation(AnimationEntry, BaseModel):
    model_config = ConfigDict(frozen=False, strict=True, arbitrary_types_allowed=True)

    anim_dir: str
    anim_name: Optional[str] = None
    mode_name: Union[ModeEntry, str, None] = None
    includes: Optional[Sequence[str]] = None
    need_rename: bool = True
    dict_func: Optional[Callable[[dict], dict]] = None
    is_fx: bool = False
    hero_name: Union[HeroEntry, str, None] = None
    hero_sub_type: Optional[str] = None
    monster_name: Union[MonsterEntry, str, None] = None

    skel_path: str = Field("", init=False)
    atlas_path: str = Field("", init=False)
    png_path: str = Field("", init=False)
    json_path: str = Field("", init=False)

    entry_id: str = Field(default_factory=lambda x: AutoName().new_anim(), frozen=True)

    def _get_filepaths(self):
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

        if len(json_list) > 1:
            raise ValueError(f"Expected 0 or 1 .json file, but now get {json_list}")
        if len(skel) == 0:
            skel.append(
                os.path.split(
                    self.json_to_skel(os.path.join(self.anim_dir, json_list[0]))
                )[1]
            )
        if len(skel) != 1:
            raise ValueError(f"Expected 1 .skel file, but now get {skel}")
        if len(atlas) != 1:
            raise ValueError(f"Expected 1 .atlas file, but now get {atlas}")
        if len(png) != 1:
            raise ValueError(f"Expected 1 .png file, but now get {png}")
        if skel[0][:-5] != atlas[0][:-6]:
            raise ValueError(f"File names are not equal: {skel[0]}, {atlas[0]}")

        return (
            os.path.join(self.anim_dir, skel[0]),
            os.path.join(self.anim_dir, atlas[0]),
            os.path.join(self.anim_dir, png[0]),
            None if len(json_list) == 0 else os.path.join(self.anim_dir, json_list[0])
        )

    @model_validator(mode="after")
    def _check_after(self):
        self.skel_path, self.atlas_path, self.png_path, self.json_path = self._get_filepaths()
        if self.json_path is None:
            self.json_path = self.skel_to_json(self.skel_path)
        return self

    @property
    def animations(self) -> List[str]:
        return [key for key in load_json(self.json_path)["animations"].keys()]

    @staticmethod
    def skel_to_json(skel_path) -> str:
        _, err = process_exe(CONVERTER_PATH, [skel_path], None)
        if err != "":
            raise RuntimeError(f"{err}")
        return os.path.normpath(os.path.splitext(skel_path)[0] + ".json")

    @staticmethod
    def json_to_skel(json_path) -> str:
        _, err = process_exe(CONVERTER_PATH, [json_path], None)
        if err != "":
            raise RuntimeError(f"{err}")
        return os.path.normpath(os.path.splitext(json_path)[0] + ".skel")

    def copy_and_rename_atlas(self, dir_path: str, new_name: str) -> str:
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

    def copy_and_rename_png(self, dir_path: str, new_name: str) -> str:
        make_dirs(dir_path)
        new_path = os.path.join(dir_path, new_name + ".png")
        shutil.copy2(self.png_path, new_path)
        return os.path.normpath(new_path)

    def copy_and_rename_skel(
            self,
            dir_path: str,
            new_name: str,
            dict_func: Optional[Callable[[dict], dict]] = None
    ) -> str:
        d = load_json(self.json_path)
        if dict_func is not None:
            d = dict_func(d)
        make_dirs(dir_path)
        new_path = os.path.join(dir_path, new_name + ".json")
        save_json(d, new_path)
        self.json_to_skel(new_path)
        os.remove(new_path)
        return os.path.normpath(new_path)

    def name(self) -> str:
        anim_name = self.id() if self.anim_name is None else self.anim_name
        if self.mode_name is not None and self.mode_name != "":
            anim_name = f"{anim_name}_{get_entry_id(self.mode_name)}"
        return anim_name

    def copy_and_rename_animation(self, root_dir: str) -> List[str]:
        if self.hero_name is not None and self.monster_name is not None:
            raise ValueError("Cannot set both hero_name and monster_name")

        anim_name = self.name()

        if self.need_rename:
            dict_func = get_rename_skel_dict_func(anim_name)
        else:
            dict_func = None
        if self.dict_func is not None:
            dict_func = self.dict_func

        if self.includes is not None:
            items = self.animations
            for item in self.includes:
                if item not in items:
                    raise ValueError(f"{item} is not in {items}")

            def tem_func(d: dict) -> dict:
                tem = {}
                for item in self.includes:
                    tem[item] = d[item]
                if dict_func is None:
                    return tem
                return dict_func(tem)

            dict_func = tem_func

        res = []

        if self.hero_name is not None:
            hero_name = get_entry_id(self.hero_name)
            new_name = f"{hero_name}.sprite.{anim_name}"
            dir_path = os.path.join(root_dir, HERO_SAVE_DIR, hero_name)
            if self.is_fx:
                dir_path = os.path.join(dir_path, "fx")
                res.append(self.copy_and_rename_skel(dir_path, new_name, dict_func))
                res.append(self.copy_and_rename_atlas(dir_path, new_name))
                res.append(self.copy_and_rename_png(dir_path, new_name))
                return res

            anim_dir_path = os.path.join(dir_path, "anim")
            res.append(self.copy_and_rename_skel(anim_dir_path, new_name, dict_func))
            res.append(self.copy_and_rename_atlas(anim_dir_path, new_name))

            if self.hero_sub_type is None:
                png_dir_path = [os.path.join(dir_path, f"{hero_name}_{item}", "anim") for item in [
                    "A",
                    # "B", "C", "D"
                ]]
            else:
                png_dir_path = [os.path.join(dir_path, f"{hero_name}_{self.hero_sub_type.upper()}", "anim")]
            for item in png_dir_path:
                res.append(self.copy_and_rename_png(item, new_name))
            return res

        if self.monster_name is not None:
            monster_name = get_entry_id(self.monster_name)
            new_name = f"{monster_name}.sprite.{anim_name}"
            if self.is_fx:
                dir_path = os.path.join(root_dir, MONSTER_SAVE_DIR, monster_name, "fx")
            else:
                dir_path = os.path.join(root_dir, MONSTER_SAVE_DIR, monster_name, "anim")
            res.append(self.copy_and_rename_skel(dir_path, new_name, dict_func))
            res.append(self.copy_and_rename_atlas(dir_path, new_name))
            res.append(self.copy_and_rename_png(dir_path, new_name))
            return res

        if not self.is_fx:
            raise ValueError("no global anim,fx only")
        dir_path = os.path.join(root_dir, "fx", anim_name)
        new_name = f"{anim_name}.sprite"
        res.append(self.copy_and_rename_skel(dir_path, new_name, dict_func))
        res.append(self.copy_and_rename_atlas(dir_path, new_name))
        res.append(self.copy_and_rename_png(dir_path, new_name))
        return res


if __name__ == '__main__':
    a = Animation(
        anim_dir=r"D:\Users\Desktop\x_dd_tools\xddtools\data\template\mode\camp",
        mode_name="human",
        hero_name="xue"
    )
    print(a.animations)
    a.copy_and_rename_animation("test")

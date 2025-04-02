import json
import os
import subprocess
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Tuple, Sequence, Callable, List, Any, Union

from PIL import Image
from PIL.Image import Resampling


def get_bark_list(bark: Union[Sequence[str], str, None]) -> List[str]:
    if isinstance(bark, str):
        return [bark]
    elif isinstance(bark, Sequence):
        return list(bark)
    else:
        return []


def make_dirs(dir_path: str):
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)


def write_str_to_file(file_path: str, content: str):
    make_dirs(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return os.path.normpath(file_path)


def process_exe(
        exe_path: str,
        args: Optional[Sequence[str]],
        cwd: Optional[str] = None
) -> Tuple[str, str]:
    if args is None:
        args = []
    process = subprocess.Popen(
        [exe_path, *args],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=cwd
    )
    info = process.stdout.read()
    err = process.stderr.read()
    return info, err


def float_to_percent_int(value: float) -> int:
    return round(value * 100)


def float_to_percent_str(value: float) -> str:
    value = value * 100
    decimal_value = Decimal(str(value))
    if decimal_value == decimal_value.to_integral():
        return str(int(decimal_value))
    else:
        return str(decimal_value.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).rstrip(".0")


def bool_to_lower_str(value: bool) -> str:
    return str(value).lower()


def int_to_alpha_str(n: int) -> str:
    result = ''
    while n >= 0:
        n, remainder = divmod(n, 26)
        result = chr(65 + remainder) + result
        if n == 0:
            break
        elif n == 1:
            # 特殊处理n=1的情况，因为下一个循环会使得n变为0并跳出循环
            result = 'A' + result
            break
        n -= 1
    return result.lower()


def is_image(file_path: str) -> bool:
    # 检查文件是否存在
    if not os.path.isfile(file_path):
        return False

    try:
        # 尝试打开图像文件
        with Image.open(file_path):
            return True
    except IOError:
        # 如果文件无法作为图像打开，则不是可编辑的图片
        print("File cannot be opened as an image.")
        return False


def resize_image(input_path: str, output_path: str, size: Tuple[int, int] = (72, 144)):
    # 打开图像文件
    img = Image.open(input_path).convert("RGBA")  # 确保图像为RGBA模式以保留透明度
    # 调整大小，忽略原始比例
    resized_img = img.resize(size, Resampling.LANCZOS)
    # 保存结果图像
    make_dirs(os.path.dirname(output_path))
    resized_img.save(output_path, "PNG")
    return os.path.normpath(output_path)


def resize_image_keep_ratio(input_path: str, output_path: str, size: Tuple[int, int] = (72, 144)):
    target_width, target_height = size
    # 打开原始图片
    img = Image.open(input_path).convert("RGBA")
    original_width, original_height = img.size
    # 计算新尺寸
    ratio = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    # 调整大小
    resized_img = img.resize((new_width, new_height), Resampling.LANCZOS)
    # 创建一个新的透明背景图像
    final_image = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
    position = ((target_width - new_width) // 2, (target_height - new_height) // 2)
    final_image.paste(resized_img, position)
    # 保存结果
    make_dirs(os.path.dirname(output_path))
    final_image.save(output_path, "PNG")
    return os.path.normpath(output_path)


def overlay_images(
        background_path: str,
        overlay_path: str,
        output_path: str,
        size: Tuple[int, int] = (72, 144)
):
    # 打开背景图片和覆盖图片
    background = Image.open(background_path).convert("RGBA")
    overlay = Image.open(overlay_path).convert("RGBA")
    # 强制调整背景图片大小到指定尺寸，不保持宽高比
    background_resized = background.resize(size, Resampling.LANCZOS)
    # 计算覆盖图片的新尺寸，保持宽高比
    original_width, original_height = overlay.size
    target_width, target_height = size
    ratio = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    # 调整覆盖图片大小，使用LANCZOS重采样方法
    overlay_resized = overlay.resize((new_width, new_height), Resampling.LANCZOS)
    # 创建一个新的图像，用于保存结果
    combined = Image.new("RGBA", size)
    # 将背景图片粘贴到新图像上
    combined.paste(background_resized, (0, 0))
    # 计算覆盖图片的位置，使其居中
    position = ((target_width - new_width) // 2, (target_height - new_height) // 2)
    # 将覆盖图片粘贴到背景图片上，使用透明度混合
    combined.paste(overlay_resized, position, overlay_resized)
    # 保存结果图像
    make_dirs(os.path.dirname(output_path))
    combined.save(output_path, "PNG")
    return os.path.normpath(output_path)


def get_rename_skel_dict_func(new_name: str) -> Callable[[dict], dict]:
    def rename_skel_dict(skel_dict: dict) -> dict:
        if len(skel_dict["animations"]) > 1:
            raise ValueError("Only one animation is allowed in the skel dict.")
        if new_name in skel_dict["animations"].keys():
            return skel_dict
        target = list(skel_dict["animations"].keys())[0]
        skel_dict["animations"][new_name] = skel_dict["animations"][target]
        del skel_dict["animations"][target]
        return skel_dict

    return rename_skel_dict


def load_json(json_path: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, json_path: str):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True, indent=2)


def is_zero(number, epsilon=1e-10) -> bool:
    return abs(number) < epsilon


def split_list(big_list: List, chunk_size: int = 8) -> List[List[Any]]:
    # 使用列表推导式来生成分割后的子列表
    return [big_list[i:i + chunk_size] for i in range(0, len(big_list), chunk_size)]

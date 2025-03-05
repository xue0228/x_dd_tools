import hashlib
import os
import shutil
import time
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Tuple, List, Any, Callable

from PIL import Image
from PIL.Image import Resampling


def float_to_percent_str(value: float) -> str:
    value = value * 100
    decimal_value = Decimal(str(value))
    if decimal_value == decimal_value.to_integral():
        return str(int(decimal_value))
    else:
        return str(decimal_value.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)).rstrip(".0")


def float_to_percent_int(value: float) -> int:
    return round(value * 100)


def bool_to_lower_str(value: bool) -> str:
    return str(value).lower()


def bool_to_short_form_str(value: bool) -> str:
    return "t" if value else "f"


def str_or_none_to_short_form_str(value: Optional[str]) -> str:
    if value is None:
        return "category"
    words = value.strip("_").split("_")
    res = ""
    for word in words:
        if word == "":
            continue
        res += word[0]
        if len(words) <= 2:
            res += word[-1]
    if res == "":
        res = "nl"
    return res


def float_to_legal_str(value: float) -> str:
    return str(value).replace(".", "d").replace("-", "category")


def int_or_none_to_str(value: Optional[int]) -> str:
    if value is None:
        return "category"
    else:
        return str(value)


def clamp_string(value: str, length: int = 64) -> str:
    if len(value) > length:
        return value[:length]
    else:
        return value


def get_md5_of_instance(instance):
    """
    获取某个类实例的所有属性值拼接成的字符串的32位MD5值。

    :param instance: 类的实例
    :return: 32位的MD5值字符串
    """
    # 初始化一个时间戳字符串，用于拼接所有属性值
    attributes_values = f"{time.time()}"

    # 遍历实例的所有可访问属性
    for attr_name in dir(instance):
        # 忽略以双下划线开头的私有属性和方法
        if attr_name.startswith('__'):
            continue

        # 获取属性值
        try:
            value = getattr(instance, attr_name)
        except AttributeError:
            # 如果尝试获取@property装饰的属性时抛出AttributeError，则跳过该属性
            continue

        # 如果是可迭代对象且不是字符串，则展开
        if hasattr(value, '__iter__') and not isinstance(value, str):
            value = ''.join(str(v) for v in value)

        # 检查是否是属性而非方法，同时忽略@property属性
        if not callable(value) and not isinstance(getattr(type(instance), attr_name, None), property):
            attributes_values += str(value)

    # 计算拼接后字符串的MD5值
    md5_hash = hashlib.md5(attributes_values.encode()).hexdigest()

    return md5_hash


def is_zero(number, epsilon=1e-10) -> bool:
    return abs(number) < epsilon


def copy_dir(src_dir: str, dst_dir: str) -> Optional[Tuple[str]]:
    """
    将src_dir目录下所有文件拷贝到dst_dir
    :param src_dir:
    :param dst_dir:
    :return:
    """
    if not os.path.exists(src_dir):
        return None
    res = os.listdir(src_dir)
    if len(res) == 0:
        return None
    make_dirs(dst_dir)
    for file in res:
        shutil.copy2(os.path.join(src_dir, file), os.path.join(dst_dir, file))
    return tuple(res)


def dd_id(name: str, prefix: Optional[str] = None) -> str:
    if prefix is not None:
        res = f"{prefix}_{name}"
    else:
        res = name
    return clamp_string(res)


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


def make_dirs(dir_path: str):
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)


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


def int_to_alpha_str(n):
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


def split_list(big_list: List, chunk_size: int=8) -> List[List[Any]]:
    # 使用列表推导式来生成分割后的子列表
    return [big_list[i:i + chunk_size] for i in range(0, len(big_list), chunk_size)]


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


if __name__ == '__main__':
    print(int_to_alpha_str(0))
    print(int_to_alpha_str(1))
    print(int_to_alpha_str(10))
    print(int_to_alpha_str(27))
    print(int_to_alpha_str(100))

    # resize_image("test.png", "test1.png")
    # resize_image_keep_ratio("test.png", "test2.png")
    # overlay_images("test.png", "test.png", "test3.png")

    # print(str_or_none_to_short_form_str("riposte_on_hit_chance_"))
    # print(str_or_none_to_short_form_str("_"))
    # print(float_to_legal_str(0.75))
    # # print(int_to_zero_fill_str_by_length(1, 100))
    #
    # # 示例类
    # class Example:
    #     def __init__(self, name, age):
    #         self.name = name
    #         self.age = age
    #
    # # 创建示例对象
    # example = Example("张三", 30)
    #
    # # 调用函数获取16位MD5值
    # print(get_md5_of_instance(example))

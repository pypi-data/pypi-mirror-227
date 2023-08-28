from enum import Enum


class log_level_enum(Enum):
    """
    log级别枚举
    """
    Error = 1
    Warning = 2
    Normal = 3
    Pigeonhole = 4


class log_color_enum(Enum):
    DEFAULT = ""
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"


def convert_print_color(*args):
    """
    函数返回带有指定颜色的字符串。

    :param args: 可变数量的参数，每个参数可以是字符串或一个包含字符串和log_color_enum的元组。
    :return: 拼接好的带有颜色代码的字符串
    """
    result = []

    for arg in args:
        if isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[1], log_color_enum):
            # 元组包含字符串和颜色枚举
            result.append(f"{arg[1].value}{arg[0]}\033[0m")
        else:
            # 只有字符串
            result.append(arg)

    return ''.join(result)


def log(str, log_level: log_level_enum = log_level_enum.Normal):
    """
    打印log
    :param str: log内容
    :param log_level: log级别，使用枚举
    :param log_color: log颜色，使用枚举
    :return: 无返回
    """
    print(f"[{log_level.name}] {str}\n")  # Using \033[0m to reset the color after printing

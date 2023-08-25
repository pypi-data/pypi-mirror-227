# -*- coding:UTF-8 -*-
"""
@author: dyy
@contact: douyaoyuan@126.com
@time: 2023/8/8 9:57
@file: DebugInfo.py
@desc: 提供字符打印相关的操作方法，例如彩色文字，字符对齐，表格整理和输出，光标控制，语义日期 等
"""

# region 导入依赖项
import os as _os
import re as _re
from datetime import timedelta as _timedelta
from datetime import datetime as _datetime
import time as _time
from enum import Enum as _Enum
from enum import unique as _unique
from typing import Callable as _Callable
from functools import wraps as _wraps
from copy import copy as _copy
from copy import deepcopy as _deepcopy

try:
    # 需要安装 wcwidth 模块
    from wcwidth import wcwidth as _wcwidth
except ImportError as impErr:
    _wcwidth = None
    print("尝试导入 wcwidth 依赖时检测到异常：", impErr)
    print("尝试安装 wcwidth 模块：")
    try:
        _os.system("pip install wcwidth")
        print("尝试安装 wcwidth 成功,请重新运行代码")
    except OSError as osErr:
        print("尝试安装模块 wcwidth 时检测到异常：", osErr)
        exit(0)
    else:
        from wcwidth import wcwidth as _wcwidth

try:
    # 需要安装 colorama 模块

    # -----------------colorama模块的一些常量---------------------------
    # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Style: DIM, NORMAL, BRIGHT, RESET_ALL
    #
    from colorama import init as _init
    from colorama import Fore as _Fore
    from colorama import Back as _Back
    from colorama import Style as _Style

    _init(autoreset=True)
except ImportError as impErr:
    _init = None
    _Fore = None
    _Back = None
    _Style = None
    
    print("尝试导入 colorama 依赖时检测到异常：", impErr)
    print("尝试安装 colorama 模块：")
    try:
        _os.system("pip install colorama")
        print("尝试安装 colorama 模块成功,请重新运行代码")
    except OSError as osErr:
        print("尝试安装模块 colorama 时检测到异常：", osErr)
        exit(0)
    else:
        from colorama import init as _init
        from colorama import Fore as _Fore
        from colorama import Back as _Back
        from colorama import Style as _Style

        _init(autoreset=True)

# endregion


@_unique
class 对齐方式(_Enum):
    """
    这是一个 Enum， -1: 左对齐; 0: 居中对齐；1: 右对齐
    """
    左对齐: int = -1
    居中对齐: int = 0
    右对齐: int = 1


# region 公共方法
def 显示宽度(内容: str, 特殊字符宽度字典: dict[str, int] = None) -> int:
    """
    去除颜色控制字符，根据库 wcwidth 判断每个字符的模式，判断其占用的空格数量
    :param 内容: 需要计算显示宽度的字符串
    :param 特殊字符宽度字典: 如果有特殊字符宽度计算不准确,可以明确指定其宽度
    :return: 给定内容的显示宽度值，即等效的英文空格的数量
    """
    if not 内容:
        return 0
    颜色控制字匹配模式: str = r'\033\[\d+m'
    内容整理: str = _re.sub(颜色控制字匹配模式, '', str(内容))
    总显示宽度: int = 0

    if not 特殊字符宽度字典:
        特殊字符宽度字典 = {}
    if 内容整理:
        for 字 in 内容整理:
            if 字 in 特殊字符宽度字典:
                总显示宽度 += 特殊字符宽度字典[字]
            else:
                总显示宽度 += _wcwidth(字)

        return 总显示宽度
    else:
        return 0


# region terminal 文本色彩控制
def __字体上色(字体颜色, *values) -> str:
    合成临时字符串: str = (' '.join(str(itm) for itm in values)).strip()

    def 检查字符串首是否有字体控制字(字符串: str) -> bool:
        检查结果: bool = False

        # 匹配字符串首部的连续的所有字符控制字
        颜色控制字匹配模式: str = r'^(?:\033\[\d+m)+'
        匹配字符串 = _re.match(颜色控制字匹配模式, 字符串)
        if 匹配字符串:
            if r'[3' in 匹配字符串.string:
                检查结果 = True

        return 检查结果

    if 合成临时字符串:
        # 如果字符串首部尚不存在字体颜色控制字,则在字符串首部补充一个字体颜色控制字
        if not 检查字符串首是否有字体控制字(合成临时字符串):
            合成临时字符串 = '{}{}'.format(字体颜色, 合成临时字符串)

        # 检查原字符串尾部结束符
        if 合成临时字符串.endswith(_Fore.RESET + _Back.RESET):
            合成临时字符串 = 合成临时字符串[:-len(_Back.RESET + _Fore.RESET)] + _Back.RESET
        elif 合成临时字符串.endswith(_Fore.RESET):
            合成临时字符串 = 合成临时字符串[:-len(_Fore.RESET)]

        # 将 _Fore.RESET 部位替换成要求的字体颜色, 并在末尾补充一个Fore.RESET
        合成临时字符串 = 合成临时字符串.replace(_Fore.RESET, 字体颜色) + _Fore.RESET
    else:
        合成临时字符串 = ''
    return 合成临时字符串


def __背景上色(背景颜色, *values) -> str:
    合成临时字符串: str = (' '.join(str(itm) for itm in values)).strip()

    def 检查字符串首是否有背景控制字(字符串: str) -> bool:
        检查结果: bool = False

        # 匹配字符串首部的连续的所有字符控制字
        颜色控制字匹配模式: str = r'^(?:\033\[\d+m)+'
        匹配字符串 = _re.match(颜色控制字匹配模式, 字符串)
        if 匹配字符串:
            if r'[4' in 匹配字符串.string:
                检查结果 = True

        return 检查结果

    if 合成临时字符串:
        # 如果字符串首部尚不存在背景颜色控制字,则在字符串首部补充一个背景颜色控制字
        if not 检查字符串首是否有背景控制字(合成临时字符串):
            合成临时字符串 = '{}{}'.format(背景颜色, 合成临时字符串)

        # 检查原字符串尾部结束符
        if 合成临时字符串.endswith(_Back.RESET + _Fore.RESET):
            合成临时字符串 = 合成临时字符串[:-len(_Back.RESET + _Fore.RESET)] + _Fore.RESET
        elif 合成临时字符串.endswith(_Back.RESET):
            合成临时字符串 = 合成临时字符串[:-len(_Back.RESET)]

        # 将 _Back.RESET 部位替换成要求的背景颜色, 并在末尾补充一个Back.RESET
        合成临时字符串 = 合成临时字符串.replace(_Back.RESET, 背景颜色) + _Back.RESET
    else:
        合成临时字符串 = ''

    return 合成临时字符串


def 红字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[31m' + 字符串 + '\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.RED, *values)


def 红底(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[41m' + 字符串 + '\033[49m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __背景上色(_Back.RED, *values)


def 红底白字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[37m\033[41' + 字符串 + '\033[49m\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.WHITE, __背景上色(_Back.RED, *values))


def 红底黑字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[41m' + 字符串 + '\033[49m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.BLACK, __背景上色(_Back.RED, *values))


def 红底黄字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[33m\033\[41m' + 字符串 + '\033[49m\033[39' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.YELLOW, __背景上色(_Back.RED, *values))


def 绿字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[32m' + 字符串 + '\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.GREEN, *values)


def 绿底(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[42m' + 字符串 + '\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __背景上色(_Back.GREEN, *values)


def 黄字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[33m' + 字符串 + '\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.YELLOW, *values)


def 黄底(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[43m' + 字符串 + '\033[49m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __背景上色(_Back.YELLOW, *values)


def 蓝字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[34m' + 字符串 + '\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.BLUE, *values)


def 蓝底(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[44m' + 字符串 + '\033[49m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __背景上色(_Back.BLUE, *values)


def 洋红字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[35m' + 字符串 + '\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.MAGENTA, *values)


def 洋红底(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[45m' + 字符串 + '\033[49m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __背景上色(_Back.MAGENTA, *values)


def 青字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[36m' + 字符串 + '\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.CYAN, *values)


def 青底(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[46m' + 字符串 + '\033[49m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __背景上色(_Back.CYAN, *values)


def 白字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[37m' + 字符串 + '\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.WHITE, *values)


def 白底黑字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[30m\033\[47m' + 字符串 + '\033[49m\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.BLACK, __背景上色(_Back.WHITE, *values))


def 黑字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[30m' + 字符串 + '\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.BLACK, *values)


def 黑底(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[40m' + 字符串 + '\033[49m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __背景上色(_Back.BLACK, *values)


def 绿底白字(*values) -> str:
    r"""
    将指定的字符串，修饰成 ’\033\[37m\033\[42m' + 字符串 + '\033[49m\033[39m' 的格式
    :param values: 待修饰的字符串
    :return: 修饰后的字符串
    """
    return __字体上色(_Fore.WHITE, __背景上色(_Back.GREEN, *values))


# endregion


# region terminal 光标控制
def 光标上移(行数: int = 0) -> None:
    r"""
    print('\033[{}A'.format(行数 + 1))
    """
    if 行数 > 0:
        print('\033[{}A'.format(行数 + 1))


def 光标下移(行数: int = 0) -> None:
    r"""
    print('\033[{}B'.format(行数))
    """
    if 行数 > 0:
        print('\033[{}B'.format(行数))


def 光标右移(列数: int = 0) -> None:
    r"""
    print('\033[{}C'.format(列数))
    """
    if 列数 > 0:
        print('\033[{}C'.format(列数))


def 清屏() -> None:
    r"""
    print('\033[{}J'.format(2))
    """
    print('\033[{}J'.format(2))


def 设置光标位置(行号: int, 列号: int) -> None:
    r"""
    print('\033[{};{}H'.format(行号, 列号))
    """
    if 行号 >= 0 and 列号 >= 0:
        print('\033[{};{}H'.format(行号, 列号))


def 保存光标位置() -> None:
    r"""
    print('\033[s')
    """
    print('\033[s')


def 恢复光标位置() -> None:
    r"""
    print('\033[u')
    """
    print('\033[u')


def 隐藏光标() -> None:
    r"""
    print('\033[?25l')
    """
    print('\033[?25l')


def 显示光标() -> None:
    r"""
    print('\033[?25h')
    """
    print('\033[?25h')


# endregion
# endregion


class 分隔线模板:
    """
    用于生成分隔线，您可以通过 分隔线模板.帮助文档() 来打印相关的帮助信息
    """
    __符号: str = '-'
    __提示内容: str = None
    __总长度: int = 50
    __提示对齐: 对齐方式 = 对齐方式.居中对齐
    __修饰方法: _Callable[[str], str] or list[_Callable[[str], str]] = None
    __打印方法: callable = None
    __特殊字符宽度字典: dict[str, int] = None

    def __init__(self,
                 符号: str = '-',
                 提示内容: str = None,
                 总长度: int = 50,
                 提示对齐: 对齐方式 = 对齐方式.居中对齐,
                 特殊字符宽度字典: dict[str, int] = None,
                 修饰方法: _Callable[[str], str] or list[_Callable[[str], str]] = None,
                 打印方法: callable = print):
        if 符号 is not None:
            self.__符号 = str(符号)
        if 提示内容 is not None:
            self.__提示内容 = 提示内容
        if str(总长度).isdigit():
            总长度 = int(总长度)
            if 总长度 > 0:
                self.__总长度 = 总长度
        if isinstance(提示对齐, 对齐方式):
            self.__提示对齐 = 提示对齐

        if 特殊字符宽度字典:
            self.__特殊字符宽度字典 = _copy(特殊字符宽度字典)
        else:
            self.__特殊字符宽度字典 = {}

        self.修饰方法 = 修饰方法

        if callable(打印方法):
            self.__打印方法 = 打印方法

    # region 访问器
    @property
    def 修饰方法(self) -> list[callable]:
        if callable(self.__修饰方法):
            return [self.__修饰方法]
        elif isinstance(self.__修饰方法, list):
            return _copy(self.__修饰方法)
        else:
            return []

    @修饰方法.setter
    def 修饰方法(self, 方法: _Callable[[str], str] or list[_Callable[[str], str]]):
        if callable(方法):
            self.__修饰方法 = 方法
        elif isinstance(方法, list):
            可修饰: bool = True
            for 方子 in 方法:
                if not callable(方子):
                    可修饰 = False
                    break
            if 可修饰:
                self.__修饰方法 = _copy(方法)
            elif len(方法) < 1:
                self.__修饰方法 = None

    @property
    def 副本(self):
        """
        生成一个新的 分隔线模板 对象， 并将复制当前对像内的必要成员信息
        :return: 一个新的 分隔线模板 对象
        """
        副本: 分隔线模板 = 分隔线模板()

        副本._分隔线模板__符号 = self.__符号
        副本._分隔线模板__提示内容 = self.__提示内容
        副本._分隔线模板__总长度 = self.__总长度
        副本._分隔线模板__提示对齐 = self.__提示对齐
        副本.修饰方法 = self.__修饰方法
        副本._分隔线模板__打印方法 = self.__打印方法

        副本._分隔线模板__特殊字符宽度字典 = _copy(self.__特殊字符宽度字典)

        return 副本

    # endregion

    def 符号(self, 符号: str = None):
        """
        设置分隔线的组成符号
        :param 符号: -, ~, * 都是常用的分隔线符号
        :return: self
        """
        if 符号 is None:
            self.__符号 = '-'
        else:
            self.__符号 = str(符号)
        return self

    def 提示内容(self, 提示: str = None):
        """
        设置分隔线的提示内容
        :param 提示: 提示内容
        :return: self
        """
        if 提示 is None:
            self.__提示内容 = ''
        else:
            self.__提示内容 = str(提示)
        return self

    def 总长度(self, 长度: int = 50):
        """
        设置分隔线的总长度，这个长度小于提示内容字符长度时，会显示提示内容，否则填充分隔线符号到指定长度
        :param 长度: 默认是 50
        :return: self
        """
        if not str(长度).isdigit():
            self.__总长度 = 50
        else:
            长度 = int(长度)
            if 长度 > 0:
                self.__总长度 = 长度
            else:
                self.__总长度 = 50
        return self

    def 文本对齐(self, 方式: int = 对齐方式.居中对齐):
        """
        分隔线提示内容的位置，支持左对齐，居中对齐，右对齐
        :param 方式: 对齐方式.左对齐， 对齐方式.居中对齐， 对齐方式.右对齐
        :return: self
        """
        if isinstance(方式, 对齐方式):
            self.__提示对齐 = 方式
        return self

    def 修饰(self, 方法: _Callable[[str], str] or list[_Callable[[str], str]]):
        """
        传入一个方法，或者方法list，依次对分隔线进行修饰，例如颜色修饰方法，或者 toUpper， toLower 之类的方法
        :param 方法: 接收一个字符串入参，返回一个字符传结果
        :return:self
        """
        self.修饰方法 = 方法
        return self

    def 指定特殊字符宽度字典(self, 特殊字符宽度字典: dict[str, int] = None):
        """
        指定一个 dict[str, int] 对象,用于定义特殊字符的显示宽度, 即等效的英文空格数量
        :param 特殊字符宽度字典: dict[str, int] 对象
        :return: self
        """
        self.__特殊字符宽度字典 = {}
        if 特殊字符宽度字典:
            self.__特殊字符宽度字典 = _copy(特殊字符宽度字典)
        return self

    def 展示(self, 打印方法: _Callable[[str], None] = None):
        """
        以指定的打印方法打印分隔符字符串，如果不指定打印方法，则使用内容打印方法，默认为 print 方法
        :param 打印方法: 接收 str 参数，不关心返回值
        :return: None
        """
        if callable(打印方法):
            self.__打印方法 = 打印方法
        if callable(self.__打印方法):
            self.__打印方法(self.__str__())
        else:
            print(self.__str__())

    @staticmethod
    def 帮助文档(打印方法: _Callable[[str], None] = None) -> None:
        白板: 调试模板 = 调试模板()

        if not callable(打印方法):
            白板.添加一行('分隔线模板用于生成分隔线', '|')
            白板.添加一行('符号: 分隔线中除提示内容外的填充符号, -, ~, * 都是常用的符号', '|')
            白板.添加一行('提示内容: 分隔线中用于提供参数信息的文本,可以为空', '|')
            白板.添加一行('下面是参考线的结构示例:', '|')
            白板.添加一行(青字('┌---分隔线符号----|<-这是提示内容->|<--分隔线符号----┐'), '|')
            白板.添加一行(红字('-' * 18 + '这是一个分隔线示例' + '-*-' * 6), '|')
            白板.添加一行(红字('~ ' * 9 + '这是一个分隔线示例' + ' *' * 9), '|')
            白板.添加一行('分隔线可以控制 【总长度】， 【提示内容】，【修饰方法】，【打印方法】，以支持个性化定制', '|')
            白板.添加一行('模板已经重定义 __str__ 方法，生成分隔线字符串', '|')

            白板.分隔线.符号('=').提示内容('╗').文本对齐(对齐方式.右对齐).总长度(白板.表格宽度()).修饰(黄字).展示()
            白板.展示表格()
            白板.分隔线.符号('=').提示内容('╝').文本对齐(对齐方式.右对齐).总长度(白板.表格宽度()).展示()
        else:
            白板.添加一行('分隔线模板用于生成分隔线')
            白板.添加一行('符号: 分隔线中除提示内容外的填充符号, -, ~, * 都是常用的符号')
            白板.添加一行('提示内容: 分隔线中用于提供参数信息的文本,可以为空')
            白板.添加一行('下面是参考线的结构示例:')
            白板.添加一行(青字('┌---分隔线符号----|<-这是提示内容->|<--分隔线符号----┐'))
            白板.添加一行(红字('-' * 18 + '这是一个分隔线示例' + '-*-' * 6))
            白板.添加一行(红字('~ ' * 9 + '这是一个分隔线示例' + ' *' * 9))
            白板.添加一行('分隔线可以控制 【总长度】， 【提示内容】，【修饰方法】，【打印方法】，以支持个性化定制')
            白板.添加一行('模板已经重定义 __str__ 方法，生成分隔线字符串')

            白板.展示表格(打印方法=打印方法)

    def __str__(self) -> str:
        分隔线字符串: str = ''
        if not self.__符号 or 显示宽度(self.__符号, self.__特殊字符宽度字典) < 1:
            self.__符号 = '-'

        提示文本: str = ''
        if self.__提示内容:
            提示文本 = str(self.__提示内容).strip()

        修饰符重复次数: int = ((self.__总长度 - 显示宽度(提示文本, self.__特殊字符宽度字典)) / 显示宽度(self.__符号, self.__特殊字符宽度字典)).__ceil__()
        if self.__提示对齐 == 对齐方式.左对齐:
            if 修饰符重复次数 > 0:
                分隔线字符串 = '{}{}'.format(提示文本, self.__符号 * 修饰符重复次数)
        elif self.__提示对齐 == 对齐方式.右对齐:
            if 修饰符重复次数 > 0:
                分隔线字符串 = '{}{}'.format(self.__符号 * 修饰符重复次数, 提示文本)
        else:
            修饰符重复次数: int = (
                        ((self.__总长度 - 显示宽度(提示文本, self.__特殊字符宽度字典)) * 0.5) / 显示宽度(self.__符号, self.__特殊字符宽度字典)).__floor__()
            if 修饰符重复次数 > 0:
                左边修饰符: str = ''
                右边修饰符: str = ''
                if 修饰符重复次数 > 0:
                    左边修饰符 = self.__符号 * (修饰符重复次数 + 1)
                    右边修饰符 = self.__符号 * (修饰符重复次数 + 1)

                右边修饰符修正: list[str] = []
                if 右边修饰符:
                    # 右边修饰符需要做方向转换, 例如 > 转为 <
                    右边修饰符 = ''.join(reversed(右边修饰符))

                    def 镜像字符(字: str) -> str:
                        镜像字典: dict = {None: None, '<': '>', '>': '<', '/': '\\', '\\': '/',
                                          '[': ']', ']': '[',
                                          '(': ')', ')': '(',
                                          '《': '》', '》': '《', '«': '»', '»': '«',
                                          '〈': '〉', '‹': '›', '⟨': '⟩', '〉': '〈',
                                          '›': '‹', '⟩': '⟨', '（': '）', '）': '（',
                                          '↗': '↖', '↖': '↗', '↙': '↘', '↘': '↙', 'd': 'b',
                                          'b': 'd',
                                          '⇐': '⇒', '⇒': '⇐'}

                        if 字 and 字 in 镜像字典:
                            return 镜像字典[字]
                        else:
                            return 字

                    for 字符 in 右边修饰符:
                        右边修饰符修正.append(镜像字符(字符))

                if 左边修饰符 and 右边修饰符修正:
                    分隔线字符串 = '{}{}{}'.format(左边修饰符, 提示文本, ''.join(右边修饰符修正))

        if not 分隔线字符串:
            分隔线字符串 = 提示文本

        截取长度: int = 显示宽度(分隔线字符串, self.__特殊字符宽度字典) - self.__总长度
        if 截取长度 > 0:
            if self.__提示对齐 == 对齐方式.左对齐:
                分隔线字符串 = 分隔线字符串[:len(分隔线字符串) - 截取长度]
            elif self.__提示对齐 == 对齐方式.右对齐:
                分隔线字符串 = 分隔线字符串[len(分隔线字符串) - 截取长度:]
            else:
                左边截取长度: int = (截取长度 * 0.5).__floor__()
                if 左边截取长度 > 0:
                    分隔线字符串 = 分隔线字符串[左边截取长度:]

                右边截取长度: int = 显示宽度(分隔线字符串, self.__特殊字符宽度字典) - self.__总长度
                if 右边截取长度 > 0:
                    分隔线字符串 = 分隔线字符串[:len(分隔线字符串) - 右边截取长度]

        # 生成修饰方法表
        修饰方法表: list[_Callable[[str], str]] = []
        if callable(self.__修饰方法):
            修饰方法表 = [self.__修饰方法]
        elif isinstance(self.__修饰方法, list):
            修饰方法表 = self.__修饰方法

        if 修饰方法表:
            for 方法 in 修饰方法表:
                分隔线字符串 = 方法(分隔线字符串)

        return 分隔线字符串


class 语义日期模板:
    """
    用于生成语义日期，您可以通过 主义日期模板.帮助文档() 来打印相关的帮助信息
    """
    __目标日期: _datetime = None
    __打印方法: callable = None

    def __init__(self,
                 目标日期: _datetime = _datetime.now(),
                 打印方法: callable = print):
        if 目标日期:
            self.__目标日期 = 目标日期
        else:
            self.__目标日期 = _datetime.now()
        if callable(打印方法):
            self.__打印方法 = 打印方法
        else:
            self.__打印方法 = print

    # region 访问器
    @property
    def 偏离天数(self) -> int:
        """
        目标日期距离 today() 的天数
        :return: 天数
        """
        return (self.__目标日期.date() - _datetime.now().date()).days

    @property
    def 偏离周数(self) -> int:
        """
        目标日期距离 today() 的周数
        :return: 周数
        """
        目标日期对齐到周一: _datetime = self.__目标日期 + _timedelta(days=1 - self.__目标日期.isoweekday())
        基准日期对齐到周一: _datetime = _datetime.now() + _timedelta(days=1 - _datetime.now().isoweekday())
        对齐到周一的日期偏离天数: int = (目标日期对齐到周一.date() - 基准日期对齐到周一.date()).days
        return (对齐到周一的日期偏离天数 / 7).__floor__()

    @property
    def 偏离月数(self) -> int:
        """
        目标日期距离 today() 的月数
        :return: 月数
        """
        return (self.__目标日期.year - _datetime.now().year) * 12 + self.__目标日期.month - _datetime.now().month

    @property
    def 偏离年数(self) -> int:
        """
        目标日期距离 today() 的年
        :return:
        """
        return self.__目标日期.year - _datetime.now().year

    @property
    def 语义(self) -> str:
        return self.__str__()

    @property
    def 副本(self):
        副本: 语义日期模板 = 语义日期模板()

        副本._语义日期模板__目标日期 = self.__目标日期
        副本._语义日期模板__打印方法 = self.__打印方法

        return 副本

    # endregion

    def 目标日期(self, 日期: _datetime = _datetime.now()):
        """
        设置语义日期的目标日期
        :param 日期: 目标日期， datetime 对象
        :return: self
        """
        if 日期:
            self.__目标日期 = 日期
        else:
            self.__目标日期 = _datetime.now()
        return self

    def 展示(self, 打印方法: _Callable[[str], None] = None):
        """
        展示语义日期
        :param 打印方法: 可以指定打印语义日期的方法，黰是 print
        :return: None
        """
        if callable(打印方法):
            打印方法(self.__str__())
        elif callable(self.__打印方法):
            self.__打印方法(self.__str__())
        else:
            print(self.__str__())

    @staticmethod
    def 帮助文档(打印方法: _Callable[[str], None] = None) -> None:
        白板: 调试模板 = 调试模板()

        if not callable(打印方法):
            白板.添加一行('语义日期模板用于生成指定日期的语义日期', '|')
            白板.添加一行('目标日期: 进行语义解析的目标日期，_datetime.date 对象', '|')
            白板.添加一行('模板已经重定义 __str__ 方法，生成语义日期字符串', '|')

            白板.分隔线.符号('=').提示内容('╗').文本对齐(对齐方式.右对齐).总长度(白板.表格宽度()).修饰(黄字).展示()
            白板.展示表格()
            白板.分隔线.符号('=').提示内容('╝').文本对齐(对齐方式.右对齐).总长度(白板.表格宽度()).展示()
        else:

            白板.添加一行('语义日期模板用于生成指定日期的语义日期')
            白板.添加一行('目标日期: 进行语义解析的目标日期，_datetime.date 对象')
            白板.添加一行('模板已经重定义 __str__ 方法，生成语义日期字符串')

            白板.展示表格(打印方法=打印方法)

    def __str__(self) -> str:
        语义: str = ''

        天数 = self.偏离天数
        周数 = self.偏离周数
        月数 = self.偏离月数
        年数 = self.偏离年数

        if 天数 == -3:
            语义 = '大前天'
        elif 天数 == -2:
            语义 = '前天'
        elif 天数 == 0:
            语义 = '今天'
        elif 天数 == -1:
            语义 = '昨天'
        elif 天数 == 1:
            语义 = '明天'
        elif 天数 == 2:
            语义 = '后天'
        elif 天数 == 3:
            语义 = '大后天'
        elif 周数 == -2:
            语义 = '上上周'
        elif 周数 == -1:
            语义 = '上周'
        elif 周数 == 1:
            语义 = '下周'
        elif 周数 == 2:
            语义 = '下下周'
        elif 月数 == -2:
            语义 = '上上月'
        elif 月数 == -1:
            语义 = '上月'
        elif 月数 == 1:
            语义 = '下月'
        elif 月数 == 2:
            语义 = '下下月'
        elif 年数 == -3:
            语义 = '大前年'
        elif 年数 == -2:
            语义 = '前年'
        elif 年数 == -1:
            语义 = '去年'
        elif 年数 == 1:
            语义 = '明年'
        elif 年数 == 2:
            语义 = '后年'
        elif 年数 == 3:
            语义 = '大后年'
        elif 年数 != 0:
            语义 = '{}年{}'.format(年数.__abs__(), '前' if 年数 < 0 else '后')
        elif 月数 != 0:
            语义 = '{}个月{}'.format(月数.__abs__(), '前' if 月数 < 0 else '后')
        elif 周数 != 0:
            语义 = '{}周{}'.format(周数.__abs__(), '前' if 周数 < 0 else '后')
        elif 天数 != 0:
            语义 = '{}天{}'.format(天数.__abs__(), '前' if 天数 < 0 else '后')

        return 语义


class 调试模板:
    """
    用于生成语调试模板对像，您可以通过 调试模板.帮助文档() 来打印相关的帮助信息
    """
    # 打印消息的方法
    __打印方法: callable = None
    # 默认 debug 状态为 False
    __调试状态: bool = False
    # 缩进量， 默认无缩进
    __缩进字符: str = ''
    # 默认的打印前缀为 '|-'
    __打印头: str = '|-'
    # 默认的位置提示标记为 '->'
    __位置提示符: str = '->'
    # 定义一个 table 的 buffer，用来临时存储需要打印的table内容
    __表格: list = None
    # 定义一个 list[int] 来控制表格列的对齐控制
    __表格列对齐: list[int] = None
    # 定义一个 list[int] 来控制表格列的宽度
    __表格列宽控制表: list[int] or int = None
    # 定义一个 dict[str, int] 对象, 用于指定特殊字符的显示宽度, 即等效的英文空格数量
    __特殊字符宽度字典: dict[str, int] = None

    # 定义一个 int 变更,用于记录计算的表格宽度值
    __表格宽度: int = -1
    # 定义一个 list[int] 来存储表格的实际列内容长度表
    __表格列宽: list[int] = None
    # 定义一个 list[int] or int, 来存储表格的列间距
    __表格列间距: list[int] or int = None

    def __init__(self,
                 调试状态: bool = False,
                 缩进字符: str = None,
                 打印头: str = None,
                 位置提示符: str = None,
                 特殊字符宽度字典: dict[str, int] = None,
                 表格列间距: list[int] or int = None,
                 打印方法: callable = print):
        if 调试状态:
            self.__调试状态 = True
        else:
            self.__调试状态 = False

        if 缩进字符 is not None:
            self.__缩进字符 = 缩进字符

        if 打印头 is not None:
            self.__打印头 = 打印头

        if 位置提示符 is not None:
            self.__位置提示符 = 位置提示符

        self.特殊字符宽度字典 = 特殊字符宽度字典

        self.__表格列间距 = 2
        self.表格列间距 = 表格列间距

        if callable(打印方法):
            self.__打印方法 = 打印方法

        self.__表格 = []
        self.__表格列对齐 = []
        self.__表格列宽控制表 = 0

    # region 访问器
    @property
    def 调试状态(self) -> bool:
        return self.__调试状态

    @property
    def 缩进字符(self) -> str:
        return self.__缩进字符

    @缩进字符.setter
    def 缩进字符(self, 符号: str = None) -> None:
        if 符号 is None:
            self.__缩进字符 = ''
        else:
            self.__缩进字符 = str(符号)

    @property
    def 打印头(self) -> str:
        return self.__打印头

    @打印头.setter
    def 打印头(self, 符号: str = None) -> None:
        if 符号 is None:
            self.__打印头 = ''
        else:
            self.__打印头 = str(符号)

    @property
    def 位置提示符(self) -> str:
        return self.__位置提示符

    @位置提示符.setter
    def 位置提示符(self, 符号: str = None) -> None:
        """
        设置模板的执行位置消息的提示符
        :param 符号: *, >, ->
        :return:  None
        """
        if 符号 is None:
            self.__位置提示符 = ''
        else:
            self.__位置提示符 = str(符号)

    @property
    def 特殊字符宽度字典(self) -> dict[str, int]:
        return _copy(self.__特殊字符宽度字典)

    @特殊字符宽度字典.setter
    def 特殊字符宽度字典(self, 字典: dict[str, int]) -> None:
        if isinstance(字典, dict):
            self.__特殊字符宽度字典 = _copy(字典)
        else:
            self.__特殊字符宽度字典 = {}

    @property
    def 表格行数(self) -> int:
        if not self.__表格:
            return 0
        else:
            return len(self.__表格)

    @property
    def 表格列数(self) -> int:
        if not self.__表格:
            return 0
        else:
            return max([len(行) for 行 in self.__表格])

    @property
    def 表格列间距(self) -> list[int]:
        if isinstance(self.__表格列间距, int):
            return [self.__表格列间距]
        elif isinstance(self.__表格列间距, list):
            return _copy(self.__表格列间距)
        else:
            return [2]

    @表格列间距.setter
    def 表格列间距(self, 列间距: list[int] or int):
        if isinstance(列间距, int) and 列间距 >= 0:
            self.__表格列间距 = 列间距
        elif isinstance(列间距, list):
            self.__表格列间距 = []
            for 间距 in 列间距:
                if isinstance(间距, int) and 间距 >= 0:
                    self.__表格列间距.append(间距)
                else:
                    self.__表格列间距.append(2)

        # 复位表格宽度值
        if self.__表格宽度 >= 0:
            self.__表格宽度 = -1

        # 复位 表格宽度值
        if self.__表格列宽:
            self.__表格列宽 = []

    @property
    def 表格列宽(self) -> list[int]:
        if self.__表格列宽:
            return self.__表格列宽

        各列最长字符串显示长度: list[int] = [0]

        # 如果 __表格 无内容，则直接返回
        if not self.__表格:
            return 各列最长字符串显示长度

        # 把 self.__表格展开，主要是展开单元格中的子行
        展开的表格: list[list[str]] = self.__表格展开()

        # 计算 展开的表格 中每一行中列数的最大值
        总列数: int = max([len(row) for row in 展开的表格])
        if 总列数 < 1:
            return 各列最长字符串显示长度

        # 计算每一列中各行内容的最大显示长度值
        各列最长字符串显示长度 = [0] * 总列数
        for 行元素 in 展开的表格:
            列数 = len(行元素)
            for 列号 in range(总列数):
                if 列号 < 列数:
                    各列最长字符串显示长度[列号] = max(显示宽度(行元素[列号], self.__特殊字符宽度字典), 各列最长字符串显示长度[列号])

        # 消除 各列最长字符串显示长度 尾部的零，即如果最后 N 列的内容长度都是 0，则可以不再处理最后的 N 列
        临时序列: list = []
        for 列号 in range(总列数):
            if sum(各列最长字符串显示长度[列号:]) > 0:
                临时序列.append(各列最长字符串显示长度[列号])
        各列最长字符串显示长度 = 临时序列

        # 更新 总列数
        总列数 = len(各列最长字符串显示长度)

        # 生成表格列宽控制表
        表格列宽控制表: list[int] = []
        if isinstance(self.__表格列宽控制表, int):
            表格列宽控制表 = [self.__表格列宽控制表] * 总列数
        elif isinstance(self.__表格列宽控制表, list):
            表格列宽控制表 = self.__表格列宽控制表

        # 考虑表格列宽表中对应列的宽度值,取大使用
        表格列宽控制表长度: int = len(表格列宽控制表)
        for 列号 in range(总列数):
            if 列号 < 表格列宽控制表长度:
                各列最长字符串显示长度[列号] = max(各列最长字符串显示长度[列号], 表格列宽控制表[列号])
            else:
                break

        self.__表格列宽 = 各列最长字符串显示长度

        return self.__表格列宽

    @表格列宽.setter
    def 表格列宽(self, 表格列宽: list[int] or int):
        if isinstance(表格列宽, int):
            self.__表格列宽控制表 = 表格列宽
        elif isinstance(表格列宽, list):
            self.__表格列宽控制表 = []
            for 列宽 in 表格列宽:
                if isinstance(列宽, int) and 列宽 >= 0:
                    self.__表格列宽控制表.append(列宽)
                else:
                    self.__表格列宽控制表.append(0)

        # 复位表格宽度值
        if self.__表格宽度 >= 0:
            self.__表格宽度 = -1

        # 复位 表格宽度值
        if self.__表格列宽:
            self.__表格列宽 = []

    @property
    def 表格列表(self) -> list[list[str]]:
        if not self.__表格:
            return []
        else:
            return _deepcopy(self.__表格)

    @property
    def 分隔线(self) -> 分隔线模板:
        新建分隔线: 分隔线模板 = 分隔线模板(打印方法=self.消息, 特殊字符宽度字典=self.__特殊字符宽度字典)
        return 新建分隔线

    @property
    def 调试分隔线(self) -> 分隔线模板:
        新建分隔线: 分隔线模板 = 分隔线模板(打印方法=self.调试消息, 特殊字符宽度字典=self.__特殊字符宽度字典)
        return 新建分隔线

    @property
    def 语义日期(self) -> 语义日期模板:
        语义日期: 语义日期模板 = 语义日期模板(打印方法=self.消息)
        return 语义日期

    @property
    def 副本(self):
        副本: 调试模板 = 调试模板()

        # 复制基本字段
        副本._调试模板__调试状态 = self.__调试状态
        副本._调试模板__打印头 = self.__打印头
        副本._调试模板__缩进字符 = self.__缩进字符
        副本._调试模板__位置提示符 = self.__位置提示符
        副本._调试模板__表格宽度 = self.__表格宽度

        # 复制 特殊字符宽度字典
        副本._调试模板__特殊字符宽度字典 = _copy(self.__特殊字符宽度字典)

        # 复制表格内容
        副本._调试模板__表格 = _deepcopy(self.__表格)

        # 复制表格列宽控制表
        副本.表格列宽 = self.__表格列宽控制表

        # 复制表格列宽表
        if self.__表格列宽:
            副本._调试模板__表格列宽表 = _copy(self.__表格列宽)

        # 复制表格列间距
        副本.表格列间距 = self.__表格列间距

        # 复制表格对齐控制表
        副本._调试模板__表格列对齐 = _copy(self.__表格列对齐)

        return 副本

    # endregion

    # region 表格操作
    def 准备表格(self, 对齐控制串: str = None, 列宽控制表: list[int] = None):
        """
        将表格的 list[list[str]] 清空,以准备接受新的表格内容
        :param 对齐控制串: 一个包含 l c r 的字符串，分别控制对应列的对齐方式，l: 左对齐, c: 居中对齐, r: 右对齐, 例如 'llcr'
        :param 列宽控制表: 一个整数列表, 用于控制对应最的最小列宽, 最大列宽由该列最长的字符内容决定
        :return: 返回次级方法
        """
        self.__表格 = []

        self.表格列宽 = 列宽控制表

        if 对齐控制串 is not None:
            对齐控制串 = str(对齐控制串).strip().lower()
            self.__表格列对齐 = []
            if 对齐控制串:
                for 控制字 in 对齐控制串:
                    if 控制字 == 'c' or 控制字 == '中':
                        self.__表格列对齐.append(对齐方式.居中对齐)
                    elif 控制字 == 'r' or 控制字 == '右':
                        self.__表格列对齐.append(对齐方式.右对齐)
                    else:
                        self.__表格列对齐.append(对齐方式.左对齐)

        class 次次级方法类:
            def 修饰行(self, 方法: _Callable[[str], str] or list[_Callable[[str], str]] = None) -> None:
                pass

        class 添加多行次级方法类:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        class 添加空行次级方法类:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        class 次级方法类:
            def 添加一行(self, *元素列表) -> 次次级方法类:
                pass

            def 添加一调试行(self, *元素列表) -> 次次级方法类:
                pass

            def 添加多行(self, 行列表: list or tuple, 拆分列数: int = -1, 拆分行数: int = -1) -> 添加多行次级方法类:
                pass

            def 添加多调试行(self, 行列表: list or tuple, 拆分列数: int = -1, 拆分行数: int = -1) -> 添加多行次级方法类:
                pass

            def 添加空行(self, 空行数量: int = 1) -> 添加空行次级方法类:
                pass

        次级方法: 次级方法类 = 次级方法类()
        次级方法.添加一行 = self.添加一行
        次级方法.添加一调试行 = self.添加一调试行
        次级方法.添加多行 = self.添加多行
        次级方法.添加多调试行 = self.添加多调试行
        次级方法.添加空行 = self.添加空行

        return 次级方法

    def 设置列对齐(self, 对齐控制串: str = None):
        """
        设置表格的列对齐方式
        :param 对齐控制串: 一个包含 l c r 的字符串，分别控制对应列的对齐方式，l: 左对齐, c: 居中对齐, r: 右对齐, 例如 'llcr'
        :return: 反回次级方法
        """
        # 先做一个清空操作, 即该方法肯定会清除当前的设置项的
        self.__表格列对齐 = []
        if 对齐控制串 is not None:
            对齐控制串 = str(对齐控制串).strip().lower()
            self.__表格列对齐 = []
            if 对齐控制串:
                for 控制字 in 对齐控制串:
                    if 控制字 == 'c' or 控制字 == '中':
                        self.__表格列对齐.append(对齐方式.居中对齐)
                    elif 控制字 == 'r' or 控制字 == '右':
                        self.__表格列对齐.append(对齐方式.右对齐)
                    else:
                        self.__表格列对齐.append(对齐方式.左对齐)

        class 设置列宽次级方法:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        class 次级方法类:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

            def 设置列宽(self, 列宽控制表: list[int] = None) -> 设置列宽次级方法:
                pass

        次级方法: 次级方法类 = 次级方法类()
        次级方法.展示表格 = self.展示表格
        次级方法.设置列宽 = self.设置列宽

        return 次级方法

    def 设置列宽(self, 列宽控制表: list[int] or int = None):
        """
        设置表格的列宽参数
        :param 列宽控制表: 一个整数列表, 用于控制对应最的最小列宽, 最大列宽由该列最长的字符内容决定
        :return: 返回次级方法
        """
        # 先做一个清空操作, 即该方法肯定会清除当前的设置项的
        self.__表格列宽控制表 = 0

        self.表格列宽 = 列宽控制表

        class 设置对齐次级方法:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        class 次级方法类:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

            def 设置列对齐(self, 对齐控制串: str = None) -> 设置对齐次级方法:
                pass

        次级方法: 次级方法类 = 次级方法类()
        次级方法.展示表格 = self.展示表格
        次级方法.设置列对齐 = self.设置列对齐

        return 次级方法

    def 添加一行(self, *元素列表):
        """
        将给定的内容,,整理成一个 list[str] 对象添加到模板内表格的尾部
        但, 如果参数是一个 list 对象, 则该 list 对象被忖为 list[str] 对象后添加到表格的尾部
        :param 元素列表:
        :return:
        """
        if len(元素列表) == 1 and type(元素列表[0]) in [list, tuple]:
            self.__添加一行(元素列表[0])
        elif len(元素列表) > 0:
            self.__添加一行(元素列表)

        class 次级方法类:
            def 修饰行(self, 方法: _Callable[[str], str] or list[_Callable[[str], str]] = None) -> None:
                pass

            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        次级方法: 次级方法类 = 次级方法类()
        次级方法.修饰行 = self.__修饰最后一行
        次级方法.展示表格 = self.展示表格

        return 次级方法

    def 添加空行(self, 空行数量: int = 1):
        """
        将指定数量的 [''] 对象添加到表格的尾部
        :param 空行数量: 需要添加的 [''] 的数量
        :return: 次级方法
        """
        if 空行数量 < 1:
            return None
        for 次数 in range(空行数量):
            self.__添加一行([''])

        class 次级方法类:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        次级方法: 次级方法类 = 次级方法类()
        次级方法.展示表格 = self.展示表格

        return 次级方法

    def 添加多行(self, 行列表: list or tuple, 拆分列数: int = -1, 拆分行数: int = -1):
        """
        如果 行列表 不是 list 或者 tuple 对象, 则将 [str(行列表)] 添加到表格尾部
        如果 行列表是 list 或者 tuple 对象, 则判断如下:
        1, 如果指定的 拆分列数 和 拆分行数 均无效(例如小于1), 则做判断如下:
        1.1, 如果 行列表 内部元素是 list 对象,则整理成 list[str] 对象添加到表格尾部
        1.2, 如果 行列表 内部元素不是 list 对象, 则整理成 [str(元素)] 添加到表格尾部
        2, 如果指定的拆分列数有效,则 行列表 视做一维列表,按指定的列数切片后,添加到表格尾部
        2.1, 如果指定的拆分列数无效,但拆分行数有效,则 行列表 视做一维列表, 按不超过指定行数进行切片后,添加到表格尾部
        将 list[list] 对象中的每一个 list 对象添加到表格的尾部
        如果传入的是
        :param 行列表: 需要添加到表格的数据, 一般为 list 对象,或者 list[list] 对象
        :param 拆分列数: 如果行列表为一维 list 对象, 可以指定拆分的列数控制切片, 如果此时没有指定, 则按 1 列进行拆分
        :param 拆分行数: 如果行列表为一维 list 对象, 可以指定拆分的行数控制切换
        :return: 次级方法
        """
        if type(行列表) in [list, tuple]:
            if 拆分列数 <= 0 and 拆分行数 <= 0:
                for 行元素 in 行列表:
                    if type(行元素) in [list, tuple]:
                        self.__添加一行(行元素)
                    else:
                        self.__添加一行([str(行元素)])
            elif 拆分列数 > 0:
                拆分行列表: list[list] = [行列表[截断位置: 截断位置 + 拆分列数] for 截断位置 in
                                          range(0, len(行列表), 拆分列数)]
                self.添加多行(拆分行列表)
            else:
                计算拆分列数: int = (len(行列表) / 拆分行数).__ceil__()
                self.添加多行(行列表=行列表, 拆分列数=计算拆分列数)
        else:
            self.__添加一行([str(行列表)])

        class 次级方法类:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        次级方法: 次级方法类 = 次级方法类()
        次级方法.展示表格 = self.展示表格

        return 次级方法

    def 添加一调试行(self, *元素列表):
        """
        添加一行表格内容, 但只有在调试状态为 True 时,才能添加成功
        :param 元素列表:  需要添加的内容
        :return: 次级方法
        """
        if self.__调试状态:
            self.添加一行(*元素列表)

        class 次级方法类:
            def 修饰行(self, 方法: _Callable[[str], str] or list[_Callable[[str], str]] = None) -> None:
                pass

            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        次级方法: 次级方法类 = 次级方法类()
        if self.__调试状态:
            次级方法.修饰行 = self.__修饰最后一行
            次级方法.展示表格 = self.展示表格
        else:
            次级方法.修饰行 = self.__空方法
            次级方法.展示表格 = self.__空方法

        return 次级方法

    def 添加多调试行(self, 行列表: list or tuple, 拆分列数: int = -1, 拆分行数: int = -1):
        """
        添加多行表格内容, 但只有在调试状态为 True 时才能添加成功
        :param 行列表: 需要添加的表格内容
        :param 拆分列数: 可以指定拆分列数
        :param 拆分行数: 可以指定拆分行数
        :return: 次级方法
        """
        if self.__调试状态:
            self.添加多行(行列表, 拆分列数, 拆分行数)

        class 次级方法类:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        次级方法: 次级方法类 = 次级方法类()
        if self.__调试状态:
            次级方法.展示表格 = self.展示表格
        else:
            次级方法.展示表格 = self.__空方法

        return 次级方法

    def 上下颠倒表格(self):
        """
        将表格的行进行倒序处理,将最末一行的内容放到第一行
        :return: 次级方法
        """
        if self.__表格:
            self.__表格.reverse()

        class 次次级方法类:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        class 次级方法类:
            def 左右颠倒表格(self) -> 次次级方法类:
                pass

            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        次级方法: 次级方法类 = 次级方法类()
        次级方法.左右颠倒表格 = self.左右颠倒表格
        次级方法.展示表格 = self.展示表格

        return 次级方法

    def 左右颠倒表格(self):
        """
        将表格每一行的 list 对象数量,使用空元素进行补齐到最大列数,然后进行倒序处理,以使最后一列的内容放到第一列
        :return: 次级方法
        """
        if self.__表格:
            表格最大行数: int = max([len(表格行) for 表格行 in self.__表格])

            临时表格: list = []
            for 表格行 in self.__表格:
                这一行: list[str] = 表格行[:] + [''] * (表格最大行数 - len(表格行))
                这一行.reverse()
                临时表格.append(这一行)
            self.__表格 = 临时表格

            # 处理对齐控制表, 需要同步颠倒
            if 表格最大行数 < len(self.__表格列对齐):
                self.__表格列对齐 = self.__表格列对齐[:表格最大行数]
            elif 表格最大行数 > len(self.__表格列对齐):
                for 次序 in range(表格最大行数 - len(self.__表格列对齐)):
                    self.__表格列对齐.append(对齐方式.左对齐)
            self.__表格列对齐.reverse()

            # 处理表格列宽控制表, 需要同步颠倒
            if isinstance(self.__表格列宽控制表, list):
                if 表格最大行数 < len(self.__表格列宽控制表):
                    self.__表格列宽控制表 = self.__表格列宽控制表[:表格最大行数]
                elif 表格最大行数 > len(self.__表格列宽控制表):
                    self.__表格列宽控制表 = self.__表格列宽控制表 + [0] * (表格最大行数 - len(self.__表格列宽控制表))
                self.__表格列宽控制表.reverse()

            # 处理表格列间距, 需要同步颠倒
            if isinstance(self.__表格列间距, list) and 表格最大行数 > 1:
                if 表格最大行数 - 1 < len(self.__表格列间距):
                    self.__表格列间距 = self.__表格列间距[:表格最大行数 - 1]
                elif 表格最大行数 - 1 > len(self.__表格列间距):
                    self.__表格列间距 = self.__表格列间距 + [2] * (表格最大行数 - 1 - len(self.__表格列间距))
                self.__表格列间距.reverse()

        class 次次级方法类:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        class 次级方法类:
            def 上下颠倒表格(self) -> 次次级方法类:
                pass

            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        次级方法: 次级方法类 = 次级方法类()
        次级方法.上下颠倒表格 = self.上下颠倒表格
        次级方法.展示表格 = self.展示表格

        return 次级方法

    def 修饰列(self, 指定列: list[int] or int, 修饰方法: list[_Callable[[str], str]] or _Callable[[str], str]):
        """
        对指定的列用指定的方法进行修饰
        :param 指定列: 指定列号[从 0 开始],或者指定的列号列表,[0,3,4]
        :param 修饰方法: 指定的方法,或者对应指定列号列表的方法列表
        :return: 次级方法
        """
        可修饰: bool = True
        if 可修饰:
            if not isinstance(指定列, list) and not isinstance(指定列, int):
                可修饰 = False
        if 可修饰 and isinstance(指定列, int) and 指定列 < 0:
            可修饰 = False
        if 可修饰 and isinstance(指定列, list):
            for 列号 in 指定列:
                if not isinstance(列号, int):
                    可修饰 = False
                elif 列号 < 0:
                    可修饰 = False
        if 可修饰:
            if not isinstance(修饰方法, list) and not callable(修饰方法):
                可修饰 = False
        if 可修饰 and isinstance(修饰方法, list):
            for 方法 in 修饰方法:
                if not callable(方法):
                    可修饰 = False
                    break
        if 可修饰 and isinstance(指定列, list) and isinstance(修饰方法, list) and len(指定列) != len(修饰方法):
            可修饰 = False

        if 可修饰:
            # 复位表格宽度值
            if self.__表格宽度 >= 0:
                self.__表格宽度 = -1

            # 复位 表格宽度值
            if self.__表格列宽:
                self.__表格列宽 = []

        if 可修饰:
            修饰列列号列表: list[int]
            if isinstance(指定列, int):
                修饰列列号列表 = [指定列]
            else:
                修饰列列号列表 = _copy(指定列)

            修饰方法列表: list[_Callable[[str], str]]
            if isinstance(修饰方法, list):
                修饰方法列表 = _copy(修饰方法)
            else:
                修饰方法列表 = [修饰方法] * len(修饰列列号列表)

            if self.__表格:
                for 表格行 in self.__表格:
                    for 下标 in range(len(修饰列列号列表)):
                        列号 = 修饰列列号列表[下标]
                        方法 = 修饰方法列表[下标]

                        if 列号 < len(表格行):
                            元素 = 表格行[列号]

                            # 查找是否存在换行现象
                            换行符: str = '\n' if 元素.__contains__('\n') else ''
                            if not 换行符:
                                换行符 = '\r' if 元素.__contains__('\r') else ''

                            if not 换行符:
                                元素 = 方法(元素)
                                表格行[列号] = str(元素).strip()
                            else:
                                子元素表: list[str] = []
                                for 子元素 in 元素.split(换行符):
                                    子元素表.append(str(方法(子元素)).strip())
                                表格行[列号] = 换行符.join(子元素表)

        class 次级方法类:
            def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
                pass

        次级方法: 次级方法类 = 次级方法类()
        次级方法.展示表格 = self.展示表格

        return 次级方法

    def 展示表格(self, 列间距: list[int] or int = None, 打印方法: _Callable[[str], None] = print) -> None:
        """
        将表格的每行内容进行对齐后合成字符串,分别进持打印呈现
        :param 列间距: 表格对齐处理时,不同列与前面一列的最小间隙,默认为 2 个空格
        :param 打印方法:  可以指定表格行对齐字符串的打印方法, 如果不指定, 默认是 print 方法
        :return: None
        """
        # 如果 __表格 无内容，则直接返回
        if not self.__表格:
            return None

        # 同步列间距参数
        self.表格列间距 = 列间距

        # 把 self.__表格展开，主要是展开单元格中的子行
        展开的表格: list[list[str]] = self.__表格展开()

        # 计算 展开的表格 中每一行中列数的最大值
        总列数: int = max([len(row) for row in 展开的表格])
        if 总列数 < 1:
            return None

        # 计算每一列中各行内容的最大显示长度值
        各列最长字符串显示长度: list = [idx * 0 for idx in range(总列数)]
        for 行元素 in 展开的表格:
            列数 = len(行元素)
            for 列号 in range(总列数):
                if 列号 < 列数:
                    各列最长字符串显示长度[列号] = max(显示宽度(行元素[列号], self.__特殊字符宽度字典), 各列最长字符串显示长度[列号])

        # 消除 各列最长字符串显示长度 尾部的零，即如果最后 N 列的内容长度都是 0，则可以不再处理最后的 N 列
        临时序列: list = []
        for 列号 in range(总列数):
            if sum(各列最长字符串显示长度[列号:]) > 0:
                临时序列.append(各列最长字符串显示长度[列号])
        各列最长字符串显示长度 = 临时序列

        # 更新总列数
        总列数 = len(各列最长字符串显示长度)

        # 生成表格列宽控制表
        表格列宽控制表: list[int] = []
        if isinstance(self.__表格列宽控制表, int):
            表格列宽控制表 = [self.__表格列宽控制表] * 总列数
        elif isinstance(self.__表格列宽控制表, list):
            表格列宽控制表 = self.__表格列宽控制表

        # 考虑表格列宽表中对应列的宽度值,取大使用
        表格列宽控制表长度: int = len(表格列宽控制表)
        for 列号 in range(总列数):
            if 列号 < 表格列宽控制表长度:
                各列最长字符串显示长度[列号] = max(各列最长字符串显示长度[列号], 表格列宽控制表[列号])
            else:
                break

        # 生成列间距表
        列间距表: list[int] = [0]
        if isinstance(self.__表格列间距, int):
            列间距表 = 列间距表 + [self.__表格列间距] * (总列数 - 1)
        elif isinstance(self.__表格列间距, list):
            列间距表 = 列间距表 + self.__表格列间距
            if len(列间距表) < 总列数:
                列间距表 = 列间距表 + [2] * (总列数 - len(列间距表))
        else:
            列间距表 = 列间距表 + [2] * (总列数 - 1)

        # 计算每一列的起始位置
        列起位置: list = [0] * 总列数
        for 列号 in range(总列数):
            if 列号 == 0:
                # 第一列的列起始位置为 0
                列起位置[列号] = 0
            else:
                # 每列的起始位置计算, 前一列起始位置 + 前一列最大长度 + 指定数量的个空格
                列起位置[列号] = 列起位置[列号 - 1] + 各列最长字符串显示长度[列号 - 1] + 列间距表[列号]

        对齐控制表列数: int = len(self.__表格列对齐)
        # 根据每一列的起始位置，将每一行的内容合成一个字符串
        行字符串列表: list[str] = []
        for 行元素 in 展开的表格:
            列数 = len(行元素)
            行字符串: str = ''
            for 列号 in range(总列数):
                本列对齐方式: int = 对齐方式.左对齐
                if 列号 < 对齐控制表列数:
                    本列对齐方式 = self.__表格列对齐[列号]

                if 列号 < 列数:
                    # 补齐 行字符串 尾部的空格，以使其长度与该列的起始位置对齐
                    行字符串 = '{}{}'.format(行字符串, ' ' * max(0, (列起位置[列号] - 显示宽度(行字符串, self.__特殊字符宽度字典))))

                    # 在补齐的基础上, 添加本列的内容
                    本列内容: str
                    if 本列对齐方式 == 对齐方式.左对齐:
                        # 左对齐
                        本列内容 = 行元素[列号]
                    else:
                        本列宽度: int
                        if 列号 + 1 < 总列数:
                            本列宽度 = 列起位置[列号 + 1] - 列起位置[列号] - 列间距表[列号 + 1]
                        else:
                            本列宽度 = 各列最长字符串显示长度[列号]

                        本列补齐空格数量: int = max(0, 本列宽度 - 显示宽度(行元素[列号], self.__特殊字符宽度字典))
                        if 本列补齐空格数量 > 0:
                            if 本列对齐方式 == 对齐方式.右对齐:
                                # 右对齐
                                本列内容 = '{}{}'.format(' ' * 本列补齐空格数量, 行元素[列号])
                            else:
                                # 居中对齐
                                本列左侧补齐空格数量: int = (本列补齐空格数量 * 0.5).__floor__()
                                本列右侧补齐空格数量: int = 本列补齐空格数量 - 本列左侧补齐空格数量
                                if 本列左侧补齐空格数量 > 0:
                                    本列内容 = '{}{}'.format(' ' * 本列左侧补齐空格数量, 行元素[列号])
                                else:
                                    本列内容 = 行元素[列号]

                                if 本列右侧补齐空格数量 > 0:
                                    # 如果需要做些什么， 可以在这里写你的代码
                                    # 本列内容 = '{}{}'.format(本列内容, ' ' * 本列右侧补齐空格数量)
                                    pass
                        else:
                            本列内容 = 行元素[列号]

                    行字符串 += 本列内容
            行字符串列表.append(行字符串.rstrip())

        # 打印输出每一行的内容
        if not callable(打印方法):
            打印方法 = self.__打印方法
        if 行字符串列表:
            for 行字符串 in 行字符串列表:
                打印方法('{}{}{}'.format(self.__缩进字符, self.__打印头, 行字符串))

        return None

    def 表格宽度(self, 列间距: list[int] or int = None) -> int:
        """
        根据展示表格和逻辑, 计算当前模板对象中表格内容每一行对齐处理后的字符串,取其中最长的一行的显示宽度返回
        :param 列间距: 表格列间距
        :return: 表格宽度
        """
        # 如果 self.__表格宽度 值不小于0
        if self.__表格宽度 >= 0:
            # 如果不指定列间距, 或者指定的列间距 与 列间距成员相同, 则可以直接返回
            if 列间距 is None:
                return self.__表格宽度
            elif self.__表格列间距 == 列间距:
                return self.__表格宽度
            elif isinstance(self.__表格列间距, list):
                if isinstance(列间距, int):
                    if len(self.__表格列间距) == 1 and self.__表格列间距[0] == 列间距:
                        return self.__表格宽度
                elif isinstance(列间距, list):
                    间距等价: bool = True
                    for 下标 in range(min(len(self.__表格列间距), len(列间距))):
                        if self.__表格列间距[下标] != 列间距[下标]:
                            间距等价 = False
                            break
                    if 间距等价:
                        if len(self.__表格列间距) > len(列间距):
                            if self.__表格列间距[len(列间距):len(self.__表格列间距)] != [2] * (len(self.__表格列间距) - len(列间距)):
                                间距等价 = False
                    if 间距等价:
                        if len(列间距) > len(self.__表格列间距):
                            if 列间距[len(self.__表格列间距):len(列间距)] != [2] * (len(列间距) - len(self.__表格列间距)):
                                间距等价 = False

                    if 间距等价:
                        return self.__表格宽度
            elif isinstance(self.__表格列间距, int):
                if isinstance(列间距, list) and len(列间距) == 1 and 列间距[0] == self.__表格列间距:
                    return self.__表格宽度
            else:
                pass

        # 同步列间距参数
        self.表格列间距 = 列间距

        # 如果 __表格 无内容，则直接返回
        if not self.__表格:
            return 0

        # 把 self.__表格展开，主要是展开单元格中的子行
        展开的表格: list[list[str]] = self.__表格展开()

        # 计算 展开的表格 中每一行中列数的最大值
        总列数: int = max([len(row) for row in 展开的表格])
        if 总列数 < 1:
            return 0

        # 计算每一列中各行内容的最大显示长度值
        各列最长字符串显示长度: list = [idx * 0 for idx in range(总列数)]
        for 行元素 in 展开的表格:
            列数 = len(行元素)
            for 列号 in range(总列数):
                if 列号 < 列数:
                    各列最长字符串显示长度[列号] = max(显示宽度(行元素[列号], self.__特殊字符宽度字典), 各列最长字符串显示长度[列号])

        # 消除 各列最长字符串显示长度 尾部的零，即如果最后 N 列的内容长度都是 0，则可以不再处理最后的 N 列
        临时序列: list = []
        for 列号 in range(总列数):
            if sum(各列最长字符串显示长度[列号:]) > 0:
                临时序列.append(各列最长字符串显示长度[列号])
        各列最长字符串显示长度 = 临时序列

        # 更新总列数
        总列数 = len(各列最长字符串显示长度)

        # 生成表格列宽控制表
        表格列宽控制表: list[int] = []
        if isinstance(self.__表格列宽控制表, int):
            表格列宽控制表 = [self.__表格列宽控制表] * 总列数
        elif isinstance(self.__表格列宽控制表, list):
            表格列宽控制表 = self.__表格列宽控制表

        # 考虑表格列宽表中对应列的宽度值,取大使用
        表格列宽控制表长度: int = len(表格列宽控制表)
        for 列号 in range(总列数):
            if 列号 < 表格列宽控制表长度:
                各列最长字符串显示长度[列号] = max(各列最长字符串显示长度[列号], 表格列宽控制表[列号])
            else:
                break

        # 生成列间距表
        列间距表: list[int] = [0]
        if isinstance(self.__表格列间距, int):
            列间距表 = 列间距表 + [self.__表格列间距] * (总列数 - 1)
        elif isinstance(self.__表格列间距, list):
            列间距表 = 列间距表 + self.__表格列间距
            if len(列间距表) < 总列数:
                列间距表 = 列间距表 + [2] * (总列数 - len(列间距表))
        else:
            列间距表 = 列间距表 + [2] * (总列数 - 1)

        # 计算每一列的起始位置
        列起位置: list = []
        for 列号 in range(len(各列最长字符串显示长度)):
            if 列号 == 0:
                # 第一列的列起始位置为 0
                列起位置.append(0)
            else:
                # 每列的起始位置计算, 前一列起始位置 + 前一列最大长度 + 指定数量的个空格
                列起位置.append(列起位置[列号 - 1] + 各列最长字符串显示长度[列号 - 1] + 列间距表[列号])

        # 最后一列的起始位置 + 最后一列的最大宽度, 即为表格宽度
        self.__表格宽度 = 列起位置[-1] + 各列最长字符串显示长度[-1]

        return self.__表格宽度

    def __添加一行(self, 行表: list or tuple = None) -> None:
        if 行表 is None:
            return None

        if type(行表) not in [list, tuple]:
            return None

        这一行: list[str] = []

        # 将每一行中的元素转为字符串，存于list中
        for 元素 in 行表:
            这一行.append(str(元素).strip())

        if 这一行:
            self.__表格.append(这一行)

            # 复位 表格宽度值
            self.__表格宽度 = -1

            # 复位 表格列宽
            self.__表格列宽 = []

        return None

    def __表格展开(self) -> list[list[str]]:
        # 这个函数将 self.__表格 进行展开操作，主要是展开表格内容中的换行符
        展开的表格: list[list[str]] = []
        if self.__表格:
            for 行元素 in self.__表格:
                # 对表格中的每一行元素，做如下处理
                这一行: list[str]

                换行符: str = '\n'
                换行符的个数: int = sum([1 if str(元素).__contains__(换行符) else 0 for 元素 in 行元素])
                if 换行符的个数 == 0:
                    换行符 = '\r'
                    换行符的个数 = sum([1 if str(元素).__contains__(换行符) else 0 for 元素 in 行元素])

                if 换行符的个数 == 0:
                    # 列表中的元素字符串中不包括换行符
                    这一行 = []
                    for 元素 in 行元素:
                        这一行.append(元素)
                    if 这一行:
                        展开的表格.append(这一行)
                else:
                    # 列表中的元素包括了换行符,则需要处理换行符,处理的方案是换行后的内容放到新的表格行中
                    行列表: list[list[str]] = [str(元素).split(换行符) for 元素 in 行元素]
                    最大行数: int = max([len(列表) for 列表 in 行列表])
                    列数: int = len(行列表)
                    for 行号 in range(最大行数):
                        这一行 = []
                        for 列号 in range(列数):
                            列表: list[str] = 行列表[列号]
                            if 行号 < len(列表):
                                这一行.append(列表[行号].strip())
                            else:
                                这一行.append('')
                        if 这一行:
                            展开的表格.append(这一行)
        return 展开的表格

    def __修饰最后一行(self, 方法: _Callable[[str], str] or list[_Callable[[str], str]] = None) -> None:
        if not self.__表格:
            return None

        # 准备修饰方法表
        修饰方法表: list[_Callable[[str], str]] = []
        if callable(方法):
            修饰方法表 = [方法]
        elif isinstance(方法, list):
            可修饰: bool = True
            if 可修饰:
                for 方子 in 方法:
                    if not callable(方子):
                        可修饰 = False
                        break
            if 可修饰:
                修饰方法表 = 方法

        if 修饰方法表:
            最后一行的索引: int = len(self.__表格) - 1
            for 序号 in range(len(self.__表格[最后一行的索引])):
                元素: str = str(self.__表格[最后一行的索引][序号]).strip()

                # 查找是否存在换行现象
                换行符: str = '\n' if 元素.__contains__('\n') else ''
                if not 换行符:
                    换行符 = '\r' if 元素.__contains__('\r') else ''

                if not 换行符:
                    for 方子 in 修饰方法表:
                        元素 = 方子(元素)
                    self.__表格[最后一行的索引][序号] = str(元素).strip()
                else:
                    子元素表: list[str] = []
                    for 子元素 in 元素.split(换行符):
                        for 方子 in 修饰方法表:
                            子元素 = 方子(子元素)
                        子元素表.append(str(子元素).strip())
                    self.__表格[最后一行的索引][序号] = 换行符.join(子元素表)

    def __空方法(self, *args) -> None:
        pass

    # endregion

    def 缩进(self, 缩进字符: str = None):
        """
        将当前打印内容前增加指定的缩进字符, 如果不指定, 则默认增加一个 ' '
        :param 缩进字符: 指定缩进字符
        :return: self
        """
        if 缩进字符 is None:
            self.__缩进字符 = ' ' + self.__缩进字符
        else:
            self.__缩进字符 = 缩进字符 + self.__缩进字符
        return self

    def 打开调试(self):
        """
        将当前模板对象的 调试状态 设置为 True
        :return: self
        """
        self.__调试状态 = True
        return self

    def 关闭调试(self):
        """
        将当前模板对象的 调试状态 设置为 False
        :return: self
        """
        self.__调试状态 = False
        return self

    def 设置打印头(self, 符号: str = None):
        """
        模板默认的打印头为 '|-'
        设置当前模板对象打印消息前的标记, 如果不指定, 则为 ''
        :return: self
        """
        self.打印头 = 符号
        return self

    def 设置位置提示符(self, 符号: str = None):
        """
        模板默认的位置提示符为 '->'
        设置模板对齐提示执行位置消息时的打印头, 如果不指定, 则为 ''
        :param 符号: 位置提示消息的打印头符号
        :return: self
        """
        self.位置提示符 = 符号
        return self

    def 设置特殊字符宽度字典(self, 字典: dict[str, int]):
        """
        指定一个字典,这个字典用于指定特殊字符的显示宽度,即其等效的英文空格的数量
        字符显示宽度的计算,将影响到文本对齐场景下的功能表现
        :param 字典: 一个 dict[str, int] 对象
        :return: self
        """
        self.特殊字符宽度字典 = 字典

        # 特殊字符宽度字符将影响到表格的宽度参数的估算,所以设置 特殊字符宽度字典,将会导致表格宽度和列宽表的复位
        # 复位表格宽度值
        if self.__表格宽度 >= 0:
            self.__表格宽度 = -1

        # 复位 表格宽度值
        if self.__表格列宽:
            self.__表格列宽 = []

        return self

    def 消息(self, *参数表) -> None:
        """
        使用 self.__打印方法 打印一条消息, 消息格式为 '{}{}{}'.format(缩进, 打印头, 消息内容)
        :param 参数表: 需要打印的内容
        :return: None
        """
        self.__打印方法(
            '{}{}{}'.format(self.__缩进字符, self.__打印头, ' '.join((str(参数).strip() for 参数 in 参数表))))

    def 打印空行(self, 行数: int = 1, 仅限调试模式: bool = False) -> None:
        """
        使用 self.__打印方法 打印 指定行数 行的消息, 消息格式为 '{}{}{}'.format(缩进, 打印头, '')
        :param 行数: 指定打印消息的行数
        :param 仅限调试模式: 如果指定为True, 则只有在模板对象的调试状态为True时,才会打印
        :return: None
        """
        if 行数 < 1:
            return None

        打印方法: callable
        if 仅限调试模式:
            打印方法 = self.调试消息
        else:
            打印方法 = self.消息

        for 次数 in range(行数):
            打印方法('')

    def 提示错误(self, *参数表) -> None:
        """
        使用 self.__打印方法 打印一条特殊颜色的消息, 消息格式为 '{}{}{}'.format(缩进, 打印头, 红底黄字(消息内容))
        :param 参数表: 需要打印的消息内容
        :return: None
        """
        self.__打印方法('{}{}{}'.format(self.__缩进字符,
                                        self.__打印头,
                                        红底黄字(' '.join((str(参数).strip() for 参数 in 参数表)))))

    def 调试消息(self, *参数表) -> None:
        """
        打印一条消息, 该消息只有在调试状态为 True时才会打印输出
        :param 参数表: 消息内容
        :return:
        """
        if self.__调试状态:
            self.消息(*参数表)

    def 提示调试错误(self, *参数表) -> None:
        """
        打印一条错误消息,该消息只有在调试状态为True时才会打印输出
        :param 参数表: 错误消息内容
        :return: None
        """
        if self.__调试状态:
            self.提示错误(*参数表)

    def 执行位置(self, 参数) -> None:
        """
        使用 self.__打印方法 打印一条消息,提示当前代码的运行位置,消息格式 '{}{}{}'.format(缩进, 位置提示符, 参数.__name__ + '开始执行')
        :param 参数: 需要进行提示的方法, 参数.__name__ 是该方法的名称,也可以直接使用字符串指定提示内容
        :return: None
        """
        if self.__调试状态:
            提示文本: str
            if not callable(参数):
                提示文本 = str(参数)
            else:
                提示文本 = str(参数.__name__)

            提示文本 = 提示文本.strip()
            if 提示文本:
                self.__打印方法('{}{}{}'.format(self.__缩进字符, self.__位置提示符, 黄字(提示文本) + ' 开始执行'))

    @staticmethod
    def 帮助文档(打印方法: _Callable[[str], None] = None) -> None:
        白板: 调试模板 = 调试模板()

        if not callable(打印方法):
            白板.添加一行(青字('方法'), 青字('功能说明'), '|')
            白板.添加一行('属性.缩进', '获取或者设置模板对象的缩进字符', '|')
            白板.添加一行('属性.打印头', '获取或者设置模板对象的打印头字符', '|')
            白板.添加一行('属性.位置提示符', '获取或者设置模板对象的位置提示符字符', '|')
            白板.添加一行('属性.分隔线', '获取一个分隔线对象,这个对象的 打印方法是 self.消息', '|')
            白板.添加一行('属性.语义日期', '获取一个语义日期对象,这个对象的 打印方法是 self.消息', '|')
            白板.添加一行('属性.副本', '生成并返回一个新的模板对象,新对象中的成员值复制自当前对象', '|')
            白板.添加一行('', '', '|')
            白板.添加一行('消息', '打印一条指定内容的消息', '|')
            白板.添加一行('错误', '打印一条指定内容的错误消息,该消息以着色方式显示', '|')
            白板.添加一行('调试消息', '打印一条指定内容的消息, 只有调试状态为True时才会打印', '|')
            白板.添加一行('调试错误 ',
                          '打印一条指定内容的错误消息,该消息以着色方式显示, 只有在调试状态为True时才会打印', '|')
            白板.添加一行('执行位置', '打印一条消息, 显示当前程序的执行位置', '|')
            白板.添加一行('', '', '|')
            白板.添加一行('表格属性.表格行数', '获取当前模板对象中表格的行数', '|')
            白板.添加一行('表格属性.表格列数', '获取当前模板对象中表格的列数', '|')
            白板.添加一行('表格属性.表格列表', '获取当前模板对象中表格 list[list]] 对象副本', '|')
            白板.添加一行('表格属性.表格列宽', '获取当前模板对象中表格各列最大宽度的list[int]对象', '|')
            白板.添加一行('表格属性.表格列间距', '获取或设置表格列前的间隙, list[int] 或者 int', '|')
            白板.添加一行('表格操作.准备表格', '通过 准备表格().__doc__ 查看详情', '|')
            白板.添加一行('表格操作.添加一行', '通过 添加一行().__doc__ 查看详情', '|')
            白板.添加一行('表格操作.添加多行', '通过 添加多行().__doc__ 查看详情', '|')
            白板.添加一行('表格操作.添加一调试行', '通过 添加一调试行().__doc__ 查看详情', '|')
            白板.添加一行('表格操作.添加多调试行', '通过 添加多调试行().__doc__ 查看详情', '|')
            白板.添加一行('表格操作.设置列对齐', '通过 设置列对齐().__doc__ 查看详情', '|')
            白板.添加一行('表格操作.设置列宽', '通过 设置列宽().__doc__ 查看详情', '|')
            白板.添加一行('表格操作.修饰列', '通过 修饰列().__doc__ 查看详情', '|')
            白板.添加一行('表格操作.展示表格', '通过 展示表格().__doc__ 查看详情', '|')

            白板.分隔线.符号('=').提示内容('╗').文本对齐(对齐方式.右对齐).总长度(白板.表格宽度()).修饰(黄字).展示()
            白板.展示表格()
            白板.分隔线.符号('=').提示内容('╝').文本对齐(对齐方式.右对齐).总长度(白板.表格宽度()).展示()
        else:
            白板.添加一行(青字('方法'), 青字('功能说明'))
            白板.添加一行('属性.缩进', '获取或者设置模板对象的缩进字符')
            白板.添加一行('属性.打印头', '获取或者设置模板对象的打印头字符')
            白板.添加一行('属性.位置提示符', '获取或者设置模板对象的位置提示符字符')
            白板.添加一行('属性.分隔线', '获取一个分隔线对象,这个对象的 打印方法是 self.消息')
            白板.添加一行('属性.语义日期', '获取一个语义日期对象,这个对象的 打印方法是 self.消息')
            白板.添加一行('属性.副本', '生成并返回一个新的模板对象,新对象中的成员值复制自当前对象')
            白板.添加一行('', '')
            白板.添加一行('消息', '打印一条指定内容的消息')
            白板.添加一行('错误', '打印一条指定内容的错误消息,该消息以着色方式显示')
            白板.添加一行('调试消息', '打印一条指定内容的消息, 只有调试状态为True时才会打印')
            白板.添加一行('调试错误 ',
                          '打印一条指定内容的错误消息,该消息以着色方式显示, 只有在调试状态为True时才会打印')
            白板.添加一行('执行位置', '打印一条消息, 显示当前程序的执行位置')
            白板.添加一行('', '')
            白板.添加一行('表格属性.表格行数', '获取当前模板对象中表格的行数')
            白板.添加一行('表格属性.表格列数', '获取当前模板对象中表格的列数')
            白板.添加一行('表格属性.表格列表', '获取当前模板对象中表格 list[list]] 对象副本')
            白板.添加一行('表格属性.表格列宽', '获取当前模板对象中表格各列最大宽度的list[int]对象')
            白板.添加一行('表格属性.表格列间距', '获取或设置表格列前的间隙, list[int] 或者 int')
            白板.添加一行('表格操作.准备表格', '通过 准备表格().__doc__ 查看详情')
            白板.添加一行('表格操作.添加一行', '通过 添加一行().__doc__ 查看详情')
            白板.添加一行('表格操作.添加多行', '通过 添加多行().__doc__ 查看详情')
            白板.添加一行('表格操作.添加一调试行', '通过 添加一调试行().__doc__ 查看详情')
            白板.添加一行('表格操作.添加多调试行', '通过 添加多调试行().__doc__ 查看详情')
            白板.添加一行('表格操作.设置列对齐', '通过 设置列对齐().__doc__ 查看详情')
            白板.添加一行('表格操作.设置列宽', '通过 设置列宽().__doc__ 查看详情')
            白板.添加一行('表格操作.修饰列', '通过 修饰列().__doc__ 查看详情')
            白板.添加一行('表格操作.展示表格', '通过 展示表格().__doc__ 查看详情')

            白板.展示表格(打印方法=打印方法)


# region 装饰器
def 秒表(目标方法: callable):
    @_wraps(目标方法)
    def 参数接收器(*args, **kwargs):
        # 秒表消息通过白板打印输出
        白板: 调试模板 = 调试模板()
        # 清除打印头字符, 避免干扰
        白板.打印头 = ''

        # 检查方法参数中是否存在 调试模板 对象，如果存在，则复用之
        已经找到白板参数: bool = False
        for 参数 in args:
            if isinstance(参数, 调试模板):
                白板 = 参数
                已经找到白板参数 = True
        if not 已经找到白板参数:
            for 参数 in kwargs.values():
                if isinstance(参数, 调试模板):
                    白板 = 参数
                    已经找到白板参数 = True
        if 已经找到白板参数:
            # 为了不影响原白板内容,这里需要做一个副本出来,并缩进一格
            白板 = 白板.副本.缩进()
            # 恢复列左对齐
            白板.设置列对齐('l')
            # 恢复列宽设置
            白板.设置列宽([0])

        秒表启动时间 = _time.time()
        时钟计数开始 = _time.perf_counter()
        时钟计数开始_ns = _time.perf_counter_ns()
        程序计时开始 = _time.process_time()
        程序计时开始_ns = _time.process_time_ns()

        # 执行目标方法
        运行结果 = 目标方法(*args, **kwargs)

        时钟计数结束 = _time.perf_counter()
        时钟计数结束_ns = _time.perf_counter_ns()
        程序计时结束 = _time.process_time()
        程序计时结束_ns = _time.process_time_ns()
        秒表结束时间 = _time.time()

        时钟计时 = 时钟计数结束 - 时钟计数开始
        时钟计时_ns = 时钟计数结束_ns - 时钟计数开始_ns

        程序计时 = 程序计时结束 - 程序计时开始
        程序计时_ns = 程序计时结束_ns - 程序计时开始_ns

        秒表计时 = 秒表结束时间 - 秒表启动时间

        # 准备打印内容
        白板.准备表格('lll').添加一行('项目', '值', '计时器', '备注').修饰行(青字)
        if 目标方法.__doc__:
            白板.添加一行('方法名称', 目标方法.__name__, '', 目标方法.__doc__)
        else:
            白板.添加一行('方法名称', 目标方法.__name__)
        白板.添加一行('秒表启动:', _datetime.fromtimestamp(秒表启动时间), 'time')

        if 秒表计时 > 1:
            白板.添加一行('计时/s:', 绿字(秒表计时), '_time.time')
        else:
            白板.添加一行('计时/ms:', 绿字(秒表计时 * 1000), 'time')

        if 时钟计时 > 1:
            白板.添加一行('计时/s:', 绿字(时钟计时), 'perf_counter')
        elif 时钟计时 > 0.001:
            白板.添加一行('计时/ms:', 绿字(时钟计时 * 1000), 'perf_counter')
        elif 时钟计时 > 0.000001:
            白板.添加一行('计时/us:', 绿字(时钟计时_ns * 0.001), 'perf_counter_ns')
        else:
            白板.添加一行('计时/ns:', 绿字(时钟计时_ns), 'perf_counter_ns')

        if 程序计时 > 1:
            白板.添加一行('计时/s:', 绿字(程序计时), 'process_time')
        elif 程序计时 > 0.001:
            白板.添加一行('计时/ms:', 绿字(程序计时 * 1000), 'process_time')
        elif 程序计时 > 0.000001:
            白板.添加一行('计时/us:', 绿字(程序计时_ns * 0.001), 'process_time_ns')
        else:
            白板.添加一行('计时/ns:', 绿字(程序计时_ns), 'process_time_ns')

        白板.添加一行('秒表结束:', _datetime.fromtimestamp(秒表结束时间), 'time')

        白板.分隔线.提示内容('秒表信息').修饰(红字).总长度(白板.表格宽度()).展示()

        # 以默认列间距展示表格内容
        白板.展示表格()
        return 运行结果

    return 参数接收器

# endregion

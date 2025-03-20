r"""
lua_to_exe项目源码
:author: WaterRun
:time: 2025-03-20
:file: lua_to_exe.py
"""
import subprocess
import tkinter

def self_check():
    r"""
    进行自检
    :raise RuntimeError: 如果自检过程出现错误
    """

def gui():
    r"""
    由tkinter实现的GUI界面,提供了交互式的操作转换功能
    """
    
def lua_to_exe(lua: str, exe: str):
    r"""
    将指定的.lua文件转换为.exe
    :param lua: 待转换的lua文件路径
    :param exe: 转换后的exe文件路径
    :raise FileExistsError: 如果输入或输出的文件不存在
    :raise RuntimeError: 如果转换过程中出现其它问题
    """
    self_check()
    
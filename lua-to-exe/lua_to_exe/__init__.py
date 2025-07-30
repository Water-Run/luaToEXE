"""
lua-to-exe: Convert Lua scripts into standalone .exe executables

This package provides utilities for converting Lua script files (.lua)
into standalone executable files (.exe) on Windows platforms,
based on the srlua.

Author: WaterRun
"""

from .lua_to_exe import lua_to_exe, gui, all_available

__version__ = "1.0"
__author__ = "WaterRun"
__all__ = ['lua_to_exe', 'gui']
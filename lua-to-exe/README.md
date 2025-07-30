# lua-to-exe

> `lua-to-exe` is part of the [`luaToEXE`](https://github.com/Water-Run/luaToEXE) project suite.

## Introduction

**`lua-to-exe` provides a Python library for packaging `.lua` files into standalone `.exe` executables.**  
- The conversion is powered by [`srlua`](https://github.com/LuaDist/srlua).
- **Platform limitation: Windows 64-bit.**
- **Multiple Lua versions are supported.**  
  The generated executables do not require any external DLLs to run.

---

## Installation

Install via pip:

```shell
pip install lua-to-exe
```

---

## Directory Structure

```
.../lua_to_exe/
    __init__.py
    lua_to_exe.py
    srlua/
        5.1.5-64/
            srlua.exe
            srglue.exe
        5.4.6-64/
            srlua.exe
            srglue.exe
        ...
```
> You can provide multiple Lua interpreter versions under the `srlua` directory.

---

## Usage

### 1. Python API

#### Import

```python
import lua_to_exe
```

#### Convert a Lua Script to EXE

```python
lua_to_exe.lua_to_exe("hello.lua", "hello.exe")
```

**Specify a Lua Version**

```python
lua_to_exe.lua_to_exe("hello.lua", "hello.exe", lua_version="5.4.6-64")
```
- The `lua_version` parameter is optional.  
- If not provided, the default version is `"5.1.5-64"`.
- The value must match a valid subdirectory under `srlua/`.

#### List All Available Lua Versions

```python
versions = lua_to_exe.all_available()
print(versions)  # Example: ['5.1.5-64', '5.4.6-64']
```

---

### 2. Graphical User Interface (GUI)

Launch the GUI:

```python
lua_to_exe.gui()
```

**Features:**
- Select your Lua script and output EXE path.
- Choose the Lua version (from available versions).
- See tool and Lua version information in the window.
- One-click conversion with clear status feedback.

---

## API Reference

### `lua_to_exe(lua_file, exe_file, lua_version='5.1.5-64')`
Converts a `.lua` file to a standalone `.exe`.

- `lua_file` (str): Path to the input Lua script.
- `exe_file` (str): Path for the output executable.
- `lua_version` (str, optional): Folder name for the Lua runtime. Must be present under `srlua/`.
- Raises `RuntimeError` on any error.

### `all_available()`
Returns a list of all available Lua versions (those with both `srlua.exe` and `srglue.exe` in their directory).

### `gui()`
Launches the GUI for interactive conversion.

---

## Notes

- **Windows 32/64-bit only.**
- Each `srlua/<version>/` subdirectory must contain both `srlua.exe` and `srglue.exe`.
- The listed Lua versions are those actually present under `srlua/`.
- If no version is available, conversion will not be possible.

---

## Example

```python
import lua_to_exe

# List all available Lua versions
print(lua_to_exe.all_available())

# Convert hello.lua to hello.exe using the default Lua version
lua_to_exe.lua_to_exe("hello.lua", "hello.exe")

# Convert using a specific Lua version
lua_to_exe.lua_to_exe("hello.lua", "hello.exe", lua_version="5.4.6-64")

# Launch the GUI
lua_to_exe.gui()
```

---

For further details, refer to the [GitHub repository](https://github.com/Water-Run/luaToEXE).

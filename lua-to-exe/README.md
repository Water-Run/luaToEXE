# lua-to-exe

> `lua-to-exe` is part of the [`luaToEXE`](https://github.com/Water-Run/luaToEXE) project suite.

## Introduction

**`lua-to-exe` provides a Python library for packaging `.lua` files into standalone `.exe` executables.**  

- The conversion process is powered by [`srlua`](https://github.com/LuaDist/srlua).
- **Platform limitation: Windows 32/64-bit.**
- **Supports multiple Lua versions.**  
  The generated executable files can run without any external DLLs.
- **Includes a GUI interface implemented with Tkinter.**  

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
import lua_to_exe # Note: use underscore, not `-`
```

#### Convert Lua Script to EXE

**Default conversion (using `Lua 5.1.5-64`)**  

```python
lua_to_exe.lua_to_exe("hello.lua", "hello.exe")
```

**Specify Lua Version**

```python
lua_to_exe.lua_to_exe("hello.lua", "hello.exe", lua_version="5.4.6-64")
```

- The `lua_version` parameter is optional.  
- If not specified, `"5.1.5-64"` is used by default.
- The value must match a valid subdirectory under `srlua/`.

#### List All Available Lua Versions

```python
versions = lua_to_exe.all_available()
print(versions)  # Example output: ['5.1.5-64', '5.4.6-64']
```

---

### 2. Graphical User Interface (GUI)

Launch the GUI:

```python
lua_to_exe.gui()
```

**Features:**

- Select the Lua script and output EXE path.
- Choose the Lua version (from available versions).
- View tool and Lua version info in the window.
- One-click conversion with status feedback.

---

## API Reference

### `lua_to_exe(lua_file, exe_file, lua_version='5.1.5-64')`

Converts a `.lua` file into a standalone `.exe` executable.

- `lua_file` (str): Path to the input Lua script.
- `exe_file` (str): Path for the output exe file.
- `lua_version` (str, optional): Name of the Lua runtime folder, must exist under `srlua/`.
- Raises `RuntimeError` on error.

### `all_available()`

Returns a list of all available Lua versions (i.e., those with both `srlua.exe` and `srglue.exe` present).

### `gui()`

Launches the graphical interface for interactive conversion.

---

## Notes

- **Only supports Windows 64-bit.**
- Each `srlua/<version>/` subdirectory must contain both `srlua.exe` and `srglue.exe` for that version.
- The available Lua versions are determined by the actual subfolders under `srlua/`.
- If no version is available, conversion will not be possible.

---

## Example

```python
import lua_to_exe

# List all available Lua versions
print(lua_to_exe.all_available())

# Convert hello.lua to hello.exe using default Lua version
lua_to_exe.lua_to_exe("hello.lua", "hello.exe")

# Convert using a specific Lua version
lua_to_exe.lua_to_exe("hello.lua", "hello.exe", lua_version="5.4.6-64")

# Launch the graphical interface
lua_to_exe.gui()
```

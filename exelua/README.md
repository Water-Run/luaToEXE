# exelua

> `exelua` is part of the [luaToEXE](https://github.com/Water-Run/luaToEXE) tool suite.

## Introduction

**`exelua` provides a ready-to-use command-line tool for packaging `.lua` files into `.exe` executables.**

- `exelua` is available in both 32-bit and 64-bit versions.
- **The 32-bit version of `exelua` only includes 32-bit Lua interpreters and can only generate 32-bit executables.**
- **The 64-bit version of `exelua` includes both 32-bit and 64-bit Lua interpreters, allowing you to generate either 32-bit or 64-bit executables.**
- The source code of `exelua` itself is written in Lua and packaged as an exe.
- The conversion process is powered by [srlua](https://github.com/LuaDist/srlua).
- **This tool statically links with different Lua versions, so the generated exe does not require any external DLLs.**
- **Platform limitation: Windows 32/64-bit only.**

---

## Installation

1. Download the appropriate version of `exelua` for your system architecture (32-bit or 64-bit) from the [releases page](https://github.com/Water-Run/luaToEXE/releases).
2. Extract it to any directory, and add the extracted `exelua` folder to your system `PATH` environment variable. Restart your computer.
3. Run `exelua -v` in a terminal. If it displays the version number, the installation was successful.

> Note: The `srlua` folder must be in the same directory as the program.

---

## Directory Structure

```
exelua.exe
\srlua\
   \5.1.5-32\
      srlua.exe
      srglue.exe
   \5.1.5-64\
      srlua.exe
      srglue.exe
   \5.4.6-32\
      srlua.exe
      srglue.exe
   \5.4.6-64\
      srlua.exe
      srglue.exe
   ...
```

> The Lua interpreter version is customizable, as long as it follows the `[LuaVersion]-[Arch]` naming convention.
> 
> **The 32-bit version of exelua only contains folders for 32-bit Lua versions (e.g., 5.1.5-32, 5.4.6-32, etc.), while the 64-bit version contains folders for both 32-bit and 64-bit Lua versions, allowing you to choose the corresponding architecture for the generated executable.**

---

## Usage

### Show Version

```powershell
exelua -v
```

### Show Help

```powershell
exelua -h
```

### List Available Lua Versions

```powershell
exelua -list
```

Sample output:

```
Available Lua versions:
  5.1.5-32
  5.1.5-64
  5.4.6-32
  5.4.6-64
```

*(The 32-bit version of exelua will only list 32-bit Lua versions, such as 5.1.5-32, 5.4.6-32, etc.)*

### Compile Lua Script to EXE

#### Use Default Lua Version (64-bit exelua defaults to `5.1.5-64`, 32-bit exelua defaults to `5.1.5-32`)

```powershell
exelua -c hello.lua hello.exe
```

#### Specify Lua Version

```powershell
exelua -c hello.lua hello.exe -lua 5.4.6-32
```

- `-lua <version>` specifies the interpreter version (must match the subfolder name under `srlua/`). If not specified, the 64-bit exelua defaults to `5.1.5-64`, and the 32-bit exelua defaults to `5.1.5-32`. If no Lua versions are available, a corresponding message will be displayed.

---

## Command-Line Options

| Option           | Description                                           |
| ---------------- | ----------------------------------------------------- |
| -v               | Show exelua version                                   |
| -h               | Show help information                                 |
| -list            | List all available Lua versions in the `srlua` folder |
| -c               | Compile the specified Lua file to exe                 |
| -lua `<version>` | Specify Lua version (optional, used with `-c`)        |

---

## Notes

- **exelua only supports Windows 32/64-bit systems.**
- Each subfolder under `srlua/` must contain both `srlua.exe` and `srglue.exe` for that version.
- Not supported on Linux or macOS.
- The supported Lua versions are determined by the actual folders present under `srlua/`.
- **The 32-bit exelua can only generate 32-bit exes; the 64-bit exelua can generate either 32-bit or 64-bit exes depending on the selected Lua version.**

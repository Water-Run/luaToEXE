# exelua

> `exelua` is part of the [`luaToEXE`](https://github.com/Water-Run/luaToEXE) tool suite.

## Introduction

**`exelua` provides a ready-to-use command-line tool for packaging `.lua` files into `.exe` executables.**

- `exelua` itself is implemented in Lua and packaged as an exe.
- The conversion is powered by [`srlua`](https://github.com/LuaDist/srlua).
- **This tool statically links with various Lua versions, so generated executables do not require external DLLs.**
- **Platform limitation: Windows 64-bit.**

---

## Installation

1. Download `exelua-0.3.zip` from the [release page](https://github.com/Water-Run/luaToEXE/releases).
2. Extract it anywhere, and add the extracted `exelua` folder to your system `PATH` environment variable. Restart your computer.
3. Run `exelua -v` in a terminal. If it displays the version number, installation was successful.

---

## Directory Structure

```
exelua.exe
\srlua\
   \5.1.5-64\
      srlua.exe
      srglue.exe
   \5.4.6-64\
      srlua.exe
      srglue.exe
   ...
```

> You may place multiple Lua interpreter versions under the `srlua` directory.

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
  5.1.5-64
  5.4.6-64
```

### Compile Lua Script to EXE

#### Use Default Lua Version (`5.1.5-64`)

```powershell
exelua -c hello.lua hello.exe
```

#### Specify Lua Version

```powershell
exelua -c hello.lua hello.exe -lua 5.4.6-64
```

- `-lua <version>` specifies the interpreter version (must match a subfolder under `srlua/`). If not provided, the default is `5.1.5-64`.

---

## Command-Line Parameters

| Option           | Description                                           |
| ---------------- | ----------------------------------------------------- |
| -v               | Show exelua version                                   |
| -h               | Show help information                                 |
| -list            | List all available Lua versions in the `srlua` folder |
| -c               | Compile the specified Lua file to an exe              |
| -lua `<version>` | Specify Lua version (optional, used with `-c`)        |

---

## Notes

- **exelua only works on Windows 64-bit systems.**
- Each subdirectory under `srlua/` must contain both `srlua.exe` and `srglue.exe` for that Lua version to be available.
- Not supported on Linux or macOS.
- The list of supported Lua versions is determined by the actual folders present under `srlua/`.

---

For additional details or troubleshooting, please refer to the [GitHub repository](https://github.com/Water-Run/luaToEXE).

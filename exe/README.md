# exe  

> `exe` is part of the [`luaToEXE`](https://github.com/Water-Run/luaToEXE) project suite.  

## Introduction  

**`exe` provides a `lua` library with ready-to-use tools for packaging `.lua` files into `.exe` files.**  
> The conversion is powered by [`srlua`](https://github.com/LuaDist/srlua).  
>> ***Platform limitation: Windows 64-bit***  

## Getting Started  

### Installation  

Install using `luarocks`:  

```cmd
luarocks install exe
```

### Usage  

Import the installed `exe` module into your project:  

```lua
local exe = require("exe")
```

The `exe` module provides a function called `buildExe`, which accepts two parameters:  

- `inputLua`: `string` The file path of the `.lua` file to be converted.  
- `outputExe`: `string` The file path where the resulting `.exe` file will be saved.  

The `buildExe` function does not return a value. It will throw an exception under the following conditions:  

1. The input or output file names are invalid.  
2. The input file does not exist.  
3. Any other conversion failure occurs.  

***Example Usage***  

```lua
local exe = require("exe")
exe.buildExe("helloworld.lua", "helloworld.exe") -- Packages helloworld.lua into helloworld.exe
```
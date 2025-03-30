# lua-to-exe  

> `lua_to-exe` is part of the [`luaToEXE`](https://github.com/Water-Run/luaToEXE) project suite.  

## Introduction  

**`lua-to-exe` provides a Python library that enables ready-to-use functionality to compile `.lua` files into self-executable `.exe` files.**  
> The conversion is powered by [`srlua`](https://github.com/LuaDist/srlua).  
>> ***Platform limitation: Windows 64-bit***  

## Getting Started  

### Installation  

Install using `pip`:  

```cmd
pip install lua-to-exe
```

### Usage  

Import `lua-to-exe` into your project *(note the use of an underscore)*:  

```python
import lua_to_exe
```

`lua-to-exe` provides two methods:  

1. **`gui()`**: A `GUI` interface implemented using `tkinter`. This allows you to select the files to convert and perform the conversion through a graphical interface.  
2. **`lua_to_exe()`**: Performs the conversion of `.lua` files to `.exe`. It does not return a value and accepts two sequential `str` arguments: the path of the `.lua` file to convert (`lua`) and the path for the resulting `.exe` file (`exe`). If an error occurs (e.g., the path does not exist), the corresponding exception will be raised.  

***Example Usage***  

```python
import lua_to_exe
lua_to_exe.gui() # Launch the GUI interface
lua_to_exe.lua_to_exe("helloworld.lua", "helloworld.exe") # Convert helloworld.lua to helloworld.exe  
```

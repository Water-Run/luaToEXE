# exelua  

> `exelua` is part of the [`luaToEXE`](https://github.com/Water-Run/luaToEXE) project suite.  

## Introduction  

**`exelua` provides a ready-to-use command-line tool for packaging `.lua` files into `.exe` files.**  
> `exelua` itself is implemented in `lua` and converted into an `exe`.  

> The conversion is powered by [`srlua`](https://github.com/LuaDist/srlua).  
>> ***Platform limitation: Windows 64-bit***  

## Getting Started  

### Installation  

*Follow these steps to complete the installation:*  

1. Download `exelua-0.3.zip` from the `release` section of the [project's GitHub page](https://github.com/Water-Run/luaToEXE).  
2. Extract it to your device and add the extracted `exelua` folder to your system's `PATH` environment variable. Then restart your device.  
3. Run `exelua -v` in a terminal. If it displays the version number, the installation was successful.  

### Usage  

Right-click in the file explorer at the directory where you want to operate, and open a terminal.  

***Check Version***  

```powershell
PS C:\Users\linzh> exelua -v
exelua: ver 0.1
```

*Explanation:*  

- The `-v` command displays the version number.  

***Convert***  

```powershell
PS C:\Users\linzh> exelua -c "helloworld.lua" "helloworld.exe"
exelua: success
```

*Explanation:*  

- `-c` triggers the compilation process.  
- The first argument following `-c` is the file path of the `.lua` file to be converted, and the second argument is the file path for the resulting `.exe` file.  
- If the conversion succeeds, it will display `success`. Otherwise, it will display the corresponding error message.

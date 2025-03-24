-- exe-0.1-1.rockspec
package = "exe"
version = "0.1-1"
source = {
    url = "https://github.com/Water-Run/luaToEXE/releases/download/exe/exe.zip", -- 更新为你的 exe.zip 直接下载链接
    dir = "luaToEXE" -- 解压缩后主目录名称
}
description = {
    summary = "A Lua library for converting .lua files into .exe executables",
    detailed = [[
        The `exe` library provides tools to package Lua scripts into standalone Windows executables.
        It uses `srlua` as its backend and is part of the `luaToEXE` project.
    ]],
    homepage = "https://github.com/Water-Run/luaToEXE",
    license = "MIT",
    maintainer = "WaterRun"
}
dependencies = {
    "lua >= 5.1"
}
build = {
    type = "builtin",
    modules = {
        exe = "exe.lua"
    }
}
-- exe-0.1-1.rockspec
package = "exe"
version = "0.1-1"
source = {
    url = "https://github.com/Water-Run/luaToEXE/releases/download/v0.1/luaToEXE-v0.1.zip",
    dir = "luaToEXE"
}
description = {
    summary = "A Lua library for converting .lua files into .exe executables",
    detailed = [[
        The `exe` library provides tools to package Lua scripts into standalone Windows executables.
        It uses `srlua` as its backend and is part of the `luaToEXE` project.
    ]],
    homepage = "https://github.com/Water-Run/luaToEXE",
    license = "MIT",
    maintainer = "WaterRun <2263633954@qq.com>"
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
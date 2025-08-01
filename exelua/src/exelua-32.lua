--[[
exelua - Convert Lua scripts to standalone Windows executables
Author: WaterRun
Version: 1.0-32
]]

local _VERSION = "1.0-32"
local _DEFAULT_LUA_VER = "5.1.5-32"

local _HELP_INFO = [[
exelua - convert lua scripts to standalone windows executables

Usage:
  exelua -v
      Show version information
  exelua -h
      Show this help message
  exelua -list
      List all available lua runtime versions
  exelua -c <input.lua> <output.exe> [-lua <version>]
      Compile <input.lua> into <output.exe>
      Optionally specify the lua runtime version (default: 5.1.5-64)

Examples:
  exelua -c script.lua script.exe
  exelua -c script.lua script.exe -lua 5.4.6-64
  exelua -list
]]

local function file_exists(filepath)
    local file = io.open(filepath, "r")
    if file then file:close() return true end
    return false
end

local function get_executable_path()
    local path = arg[0] or ""
    local sep = package.config:sub(1,1)
    path = path:gsub("[/\\]", sep)
    return path:match("^(.*"..sep..")") or ".\\"
end

local function list_versions()
    local base = get_executable_path() .. "srlua" .. package.config:sub(1,1)
    local versions = {}
    local p = io.popen('dir "'..base..'" /b /ad 2>nul')
    if p then
        for version in p:lines() do
            local sep = package.config:sub(1,1)
            local vpath = base .. version .. sep
            if file_exists(vpath.."srlua.exe") and file_exists(vpath.."srglue.exe") then
                table.insert(versions, version)
            end
        end
        p:close()
    end
    if #versions == 0 then
        print("\nexelua: no available lua versions found in 'srlua/'\n")
    else
        print("\nexelua: available lua versions:\n")
        for _, v in ipairs(versions) do print("  - " .. v) end
        print("")
    end
end

local function selfCheck(lua_version)
    if package.config:sub(1, 1) ~= "\\" then
        print("exelua: only windows platforms are supported (error)\n")
        error("PLATFORM ERROR")
    end
    local handle = io.popen("wmic os get osarchitecture")
    local result = handle:read("*a")
    handle:close()
    if not result:match("64") then
        print("exelua: only 64-bit windows systems are supported (error)\n")
        error("PLATFORM ERROR")
    end
    local sep = package.config:sub(1,1)
    local base_path = get_executable_path() .. "srlua" .. sep .. lua_version .. sep
    for _, filename in ipairs({ "srlua.exe", "srglue.exe" }) do
        local filepath = base_path .. filename
        if not file_exists(filepath) then
            print(string.format(
                "exelua: missing '%s' for lua version '%s' (error)\n" ..
                "        please ensure both srlua.exe and srglue.exe are present in 'srlua\\%s\\'\n",
                filename, lua_version, lua_version))
            error("RUNTIME ERROR")
        end
    end
end

local function ensureExtension(filepath, ext)
    if not filepath:lower():match("%." .. ext:sub(2):lower() .. "$") then
        return filepath .. ext
    end
    return filepath
end

local function quote(str)
    if not str:match('^".*"$') then
        return '"' .. str .. '"'
    else
        return str
    end
end

local function convert(inputLua, outputExe, lua_version)
    inputLua = ensureExtension(inputLua, ".lua")
    outputExe = ensureExtension(outputExe, ".exe")
    if not file_exists(inputLua) then
        print("exelua: input lua file not found: " .. inputLua .. " (error)\n")
        error("INPUT FILE NOT FOUND")
    end
    local sep = package.config:sub(1,1)
    local base_path = get_executable_path() .. "srlua" .. sep .. lua_version .. sep
    local srglue = base_path .. "srglue.exe"
    local srluaMain = base_path .. "srlua.exe"
    if not file_exists(srglue) or not file_exists(srluaMain) then
        print("exelua: missing srlua.exe or srglue.exe (error)\n")
        error("RUNTIME ERROR")
    end
    local batname = os.tmpname()
    if not batname:match("%.bat$") then batname = batname .. ".bat" end
    if not batname:match("^[A-Za-z]:") then
        batname = get_executable_path() .. batname:gsub("^[/\\]", "")
    end
    local cmd = table.concat({
        quote(srglue),
        quote(srluaMain),
        quote(inputLua),
        quote(outputExe)
    }, " ")
    local bat = assert(io.open(batname, "w"))
    bat:write("@echo off\n")
    bat:write(cmd .. "\n")
    bat:close()
    print("exelua: building executable ...\n")
    local result = os.execute('cmd /c "' .. batname .. '"')
    os.remove(batname)
    if file_exists(outputExe) then
        print("exelua: executable created at: " .. outputExe .. " (success)\n")
    else
        print("exelua: failed to generate executable (error)\n")
        error("RUNTIME ERROR")
    end
end

local function parseArgs(rawargs)
    local args, lua_version = {}, _DEFAULT_LUA_VER
    local i, n = 1, #rawargs
    while i <= n do
        local v = rawargs[i]
        if v == "-lua" and i < n then
            lua_version = rawargs[i + 1]
            i = i + 1
        else
            table.insert(args, v)
        end
        i = i + 1
    end
    return args, lua_version
end

local function main()
    local rawargs = {}
    for i = 1, #arg do rawargs[i] = arg[i] end
    if #rawargs == 1 and rawargs[1] == '-v' then
        print("exelua: version " .. _VERSION)
    elseif #rawargs == 1 and rawargs[1] == '-h' then
        print(_HELP_INFO)
    elseif #rawargs == 1 and rawargs[1] == '-list' then
        list_versions()
    else
        local args, lua_version = parseArgs(rawargs)
        if #args == 3 and args[1] == "-c" then
            selfCheck(lua_version)
            convert(args[2], args[3], lua_version)
        else
            print("\nexelua: invalid command, use 'exelua -h' to show help (error)\n")
            os.exit(1)
        end
    end
end

main()
--[[
exelua project source code. Compiled with srlua.
Author: WaterRun
Date: 2025-07-31
File: exelua.lua
]]

_VERSION = "1.0"
_DEFAULT_LUA_VER = "5.1.5-64"

_HELP_INFO = [[
exelua - convert lua scripts to standalone windows executables

usage:
  exelua -v
      show version information
  exelua -h
      show this help message
  exelua -list
      list all available lua runtime versions
  exelua -c <input.lua> <output.exe> [-lua <version>]
      compile <input.lua> into <output.exe>
      optionally specify the lua runtime version (default: 5.1.5-64)

examples:
  exelua -c script.lua script.exe
  exelua -c script.lua script.exe -lua 5.4.6-64
  exelua -list
]]

--- check if a file exists
---@param filepath string
---@return boolean
local function file_exists(filepath)
    local file = io.open(filepath, "r")
    if file then file:close() return true end
    return false
end

--- get the directory of the current executable/script
---@return string
local function get_executable_path()
    local path = arg[0] or ""
    path = path:gsub("\\", "/")
    return path:match("(.*/)")
end

--- list all available lua runtime versions (directories under srlua/)
local function list_versions()
    local base = get_executable_path() .. "srlua/"
    local versions = {}
    local p = io.popen('dir "'..base..'" /b /ad 2>nul')
    if p then
        for version in p:lines() do
            local vpath = base .. version .. "/"
            local srlua = vpath.."srlua.exe"
            local srglue = vpath.."srglue.exe"
            if file_exists(srlua) and file_exists(srglue) then
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

--- check runtime environment and required files for the selected lua version
---@param lua_version string
local function selfCheck(lua_version)
    if package.config:sub(1, 1) ~= "\\" then
        print("exelua: only windows platforms are supported (error)\n")
        error(">>>PLATFORM ERR<<<")
    end

    local handle = io.popen("wmic os get osarchitecture")
    local result = handle:read("*a")
    handle:close()
    if not result:match("64") then
        print("exelua: only 64-bit windows systems are supported (error)\n")
        error(">>>PLATFORM ERR<<<")
    end

    local base_path = get_executable_path() .. "srlua/" .. lua_version .. "/"
    local files = { "srlua.exe", "srglue.exe" }
    for _, filename in ipairs(files) do
        local filepath = base_path .. filename
        if not file_exists(filepath) then
            print(string.format(
                "exelua: missing required file '%s' for lua version '%s' (error)\n" ..
                "        please ensure both srlua.exe and srglue.exe are present in 'srlua/%s/'\n", 
                filename, lua_version, lua_version
            ))
            error(">>>RUNTIME ERR<<<")
        end
    end
end

--- ensure a file path has the correct extension, append if missing
---@param filepath string
---@param ext string
---@return string
local function ensureExtension(filepath, ext)
    if not filepath:match("%." .. ext:sub(2) .. "$") then
        print(string.format("exelua: appending '%s' extension to '%s' (note)", ext, filepath))
        return filepath .. ext
    end
    return filepath
end

--- convert a lua script file to a standalone executable
---@param inputLua string
---@param outputExe string
---@param lua_version string
local function convert(inputLua, outputExe, lua_version)
    inputLua = ensureExtension(inputLua, ".lua")
    outputExe = ensureExtension(outputExe, ".exe")

    if not file_exists(inputLua) then
        print("exelua: input lua file not found: " .. inputLua .. " (error)\n")
        error(">>>INPUT FILE NOT FOUND<<<")
    end

    local base_path = get_executable_path() .. "srlua/" .. lua_version .. "/"
    local srglue = base_path .. "srglue.exe"
    local srluaMain = base_path .. "srlua.exe"

    if not file_exists(srglue) then
        print("exelua: missing srglue.exe for lua version '"..lua_version.."' (error)\n")
        error(">>>RUNTIME ERR<<<")
    end
    if not file_exists(srluaMain) then
        print("exelua: missing srlua.exe for lua version '"..lua_version.."' (error)\n")
        error(">>>RUNTIME ERR<<<")
    end

    local cmd = string.format('"%s" "%s" "%s" "%s"', srglue, srluaMain, inputLua, outputExe)
    print("\nexelua: building executable ...\n")
    local result = os.execute(cmd)
    if result == 0 then
        print("exelua: executable created at: " .. outputExe .. " (success)\n")
    else
        print("exelua: failed to generate executable (error)\n")
        error(">>>RUNTIME ERR<<<")
    end
end

--- parse cli arguments and extract main args and optional lua version
---@param rawargs table
---@return table, string
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

--- main program entry
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
            local inputPath, outputPath = args[2], args[3]
            convert(inputPath, outputPath, lua_version)
        else
            print("\nexelua: invalid command, use 'exelua -h' to show help (error)\n")
            os.exit(1)
        end
    end
end

main()
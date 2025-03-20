--[[
exelua project source code. Compiled with srlua.
Author: WaterRun
Date: 2025-03-20
File: exelua.lua
]]

--- Version
_VERSION = 0.1

--- Help information
_HELP_INFO = "exelua: help\n" .. "Get version>> exelua -v\n" .. "Compile to exe>> exelua -c `input Lua file path` `output exe file path`"

--- Check if a file exists
--- @param filepath string: The file path to check
local function file_exists(filepath)
    local file = io.open(filepath, "rb") -- Try to open in binary mode
    if file then
        file:close()
        return true
    else
        return false
    end
end

--- Check the runtime environment and srlua files
local function selfCheck()
    local os_type
    local arch

    -- Check system type
    if package.config:sub(1, 1) == "\\" then
        os_type = "Windows"
        -- Check system architecture
        local handle = io.popen("wmic os get osarchitecture")
        local result = handle:read("*a")
        handle:close()
        if result:match("64") then
            arch = "x64"
        else
            print("exelua: can only run on 64-bit systems")
            error(">>>PLATFORM ERR<<<")
        end
    else
        print("exelua: can only run on Windows platforms")
        error(">>>PLATFORM ERR<<<")
    end

    -- Check files in the srlua directory
    local base_path = "./srlua/"
    local files = { "srlua.exe", "srglue.exe" }

    for _, filename in ipairs(files) do
        local filepath = base_path .. filename
        if not file_exists(filepath) then
            print("exelua: missing srlua file: " .. filename)
            error(">>>RUNTIME ERR<<<")
        end
    end
end

--- Ensure file extension
--- @param filepath string: The file path
--- @param ext string: The extension to check and add (e.g., ".lua" or ".exe")
local function ensureExtension(filepath, ext)
    if not filepath:match("%." .. ext:sub(2) .. "$") then
        print("exelua: auto-completion of extension " .. ext .. " for `" .. filepath .. "`")
        return filepath .. ext
    end
    return filepath
end

--- Convert Lua to exe
--- @param inputLua string: The input Lua file path
--- @param outputExe string: The output exe file path
local function convert(inputLua, outputExe)
    -- Ensure the validity of the input Lua file and output exe file
    inputLua = ensureExtension(inputLua, ".lua")
    outputExe = ensureExtension(outputExe, ".exe")

    -- Check if the input file exists
    if not file_exists(inputLua) then
        print("exelua: input .lua not find: " .. inputLua)
        error(">>>FILEEXISTS ERR<<<")
    end

    -- Get paths for srlua and srglue
    local base_path = "srlua\\"
    local srglue = base_path .. "srglue.exe"
    local srluaMain = base_path .. "srlua.exe"

    -- Ensure necessary files exist
    if not file_exists(srglue) then
        print("exelua: missing " .. srglue)
        error(">>>RUNTIME ERR<<<")
    end
    if not file_exists(srluaMain) then
        print("exelua: missing " .. srluaMain)
        error(">>>RUNTIME ERR<<<")
    end

    -- Build the command
    local cmd = string.format('%s %s %s %s', srglue, srluaMain, inputLua, outputExe)
    print("exelua: generating executable file")
    print("exelua: executing command: " .. cmd)

    -- Execute the command
    local result = os.execute(cmd)
    if result == 0 then
        print("exelua: executable file generated successfully: " .. outputExe)
    else
        print("exelua: failed to generated")
        error(">>>RUNTIME ERR<<<")
    end
end

--- Main program
local function main()
    local args = {}
    for i = 1, #arg do
        args[i] = arg[i]
    end
    if #args == 1 and args[1] == '-v' then
        print("exelua: ver " .. _VERSION)
    elseif #args == 1 and args[1] == '-h' then
        print(_HELP_INFO)
    elseif #args == 3 and args[1] == '-c' then
        selfCheck()
        local inputPath, outputPath = args[2], args[3]
        convert(inputPath, outputPath)
    else
        error("Invalid command: Use `exelua -h` to get help")
    end
end

main()

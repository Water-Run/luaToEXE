--[[
exelua project source code. Compiled with srlua.
Author: WaterRun
Date: 2025-03-20
File: exelua.lua
]]

--- Version
_VERSION = 0.1

--- Help information
_HELP_INFO = "exelua help:\n" .. "Get version: exelua -v\n" .. "Compile to exe: exelua -c `input Lua file path` `output exe file path`"

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
            error(">>>ERR<<<   exelua can only run on 64-bit systems")
        end
    else
        error(">>>ERR<<<   exelua can only run on Windows platforms")
    end

    -- Check files in the srlua directory
    local base_path = "./srlua/"
    local files = { "srlua.exe", "srglue.exe" }

    for _, filename in ipairs(files) do
        local filepath = base_path .. filename
        if not file_exists(filepath) then
            error(">>>ERR<<<   Missing srlua file: " .. filename)
        end
    end
end

--- Ensure file extension
--- @param filepath string: The file path
--- @param ext string: The extension to check and add (e.g., ".lua" or ".exe")
local function ensure_extension(filepath, ext)
    if not filepath:match("%." .. ext:sub(2) .. "$") then
        print(">>>WARN<<<   File path is missing extension, automatically added: " .. filepath .. ext)
        return filepath .. ext
    end
    return filepath
end

--- Convert Lua to exe
--- @param inputLua string: The input Lua file path
--- @param outputExe string: The output exe file path
local function convert(inputLua, outputExe)
    -- Ensure the validity of the input Lua file and output exe file
    inputLua = ensure_extension(inputLua, ".lua")
    outputExe = ensure_extension(outputExe, ".exe")

    -- Check if the input file exists
    if not file_exists(inputLua) then
        error(">>>ERR<<<   Input Lua file not found: " .. inputLua)
    end

    -- Get paths for srlua and srglue
    local base_path = "./srlua/"
    local srglue = base_path .. "srglue.exe"
    local srlua_main = base_path .. "srlua.exe"

    -- Ensure necessary files exist
    if not file_exists(srglue) then
        error(">>>ERR<<<   Missing srglue tool: " .. srglue)
    end
    if not file_exists(srlua_main) then
        error(">>>ERR<<<   Missing srlua main program: " .. srlua_main)
    end

    -- Build the command
    local cmd = string.format('%s %s %s %s', srglue, srlua_main, inputLua, outputExe)
    print(">>>INFO<<<   Generating executable file...")
    print(">>>INFO<<<   Executing command: " .. cmd)

    -- Execute the command
    local result = os.execute(cmd)
    if result == 0 then
        print(">>>INFO<<<   Executable file generated successfully: " .. outputExe)
    else
        error(">>>ERR<<<   Failed to generate executable file")
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

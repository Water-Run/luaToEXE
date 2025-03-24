--[[
Lua Library: exe project source code
Author: WaterRun
Date: 2025-03-24
File: exe.lua
]]

--- Check if a file exists
--- @param filepath string: File path
--- @return boolean: Returns true if the file exists, otherwise false
local function file_exists(filepath)
    local file = io.open(filepath, "rb")
    if file then
        file:close()
        return true
    else
        return false
    end
end

--- Ensure file extension
--- @param filepath string: File path
--- @param ext string: The extension to ensure (e.g., ".lua" or ".exe")
--- @return string: Automatically appends the extension if not present
local function ensure_extension(filepath, ext)
    if not filepath:match("%." .. ext:sub(2) .. "$") then
        return filepath .. ext
    end
    return filepath
end

--- Check if files are valid and if srlua files are available
--- @param luaFile string: Path to the Lua file to check
--- @param exeFile string: Path to the target .exe file to check
local function checkStatus(luaFile, exeFile)
    -- Ensure correct extensions for input and output files
    luaFile = ensure_extension(luaFile, ".lua")
    exeFile = ensure_extension(exeFile, ".exe")

    -- Check if the Lua file exists
    if not file_exists(luaFile) then
        error("input lua not found")
    end

    -- Check if necessary files exist in the srlua directory
    local base_path = "srlua\\"
    local srglue = base_path .. "srglue.exe"
    local srluaMain = base_path .. "srlua.exe"

    if not file_exists(srglue) then
        error("missing " .. srglue)
    end
    if not file_exists(srluaMain) then
        error("missing " .. srluaMain)
    end
end

--- Perform the conversion from Lua to exe
--- @param luaFile string: Path to the Lua file to convert
--- @param exeFile string: Path to the resulting exe file
local function buildExe(luaFile, exeFile)
    -- Check file status and runtime environment
    checkStatus(luaFile, exeFile)

    -- Get paths for srlua and srglue
    local base_path = "srlua\\"
    local srglue = base_path .. "srglue.exe"
    local srluaMain = base_path .. "srlua.exe"

    -- Construct the conversion command
    local cmd = string.format('%s %s %s %s', srglue, srluaMain, luaFile, exeFile)
    
    -- Execute the command
    local result = os.execute(cmd)
    if result ~= 0 then
        error("failed to generate executable file")
    end
end

--- Return module interface
return {
    buildExe = buildExe
}

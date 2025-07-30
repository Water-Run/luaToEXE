r"""
lua_to_exe Project Source Code
:author: WaterRun
:time: 2025-07-31
:file: lua_to_exe.py
"""

import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import platform
import sys

__version__ = "1.0"
_DEFAULT_LUA_VERSION = "5.1.5-64"

def _get_package_dir():
    """Get the directory of this package"""
    return os.path.dirname(os.path.abspath(__file__))

def _get_srlua_dir():
    """Get the srlua folder path inside the package"""
    return os.path.join(_get_package_dir(), 'srlua')

def all_available():
    """
    List all available Lua versions (folder names under srlua/ with valid binaries).
    
    Returns:
        List[str]: List of available Lua version names.
    """
    versions = []
    srlua_dir = _get_srlua_dir()
    if not os.path.isdir(srlua_dir):
        return []
    for d in os.listdir(srlua_dir):
        version_dir = os.path.join(srlua_dir, d)
        srlua_exe = os.path.join(version_dir, "srlua.exe")
        srglue_exe = os.path.join(version_dir, "srglue.exe")
        if os.path.isdir(version_dir) and os.path.isfile(srlua_exe) and os.path.isfile(srglue_exe):
            versions.append(d)
    return versions

def _get_srlua_path(lua_version):
    """Get the srlua tool path for the given version"""
    # Check current operating system
    if platform.system() != 'Windows':
        raise RuntimeError("lua_to_exe: Only supports Windows platform")
    # Check system architecture
    if not platform.machine().endswith('64'):
        raise RuntimeError("lua_to_exe: Only supports 64-bit systems")
    # srlua/ folder
    srlua_dir = _get_srlua_dir()
    version_dir = os.path.join(srlua_dir, lua_version)
    if not os.path.isdir(version_dir):
        raise RuntimeError(f"lua_to_exe: Cannot find Lua version directory: {version_dir}")
    # Check needed files
    srlua_exe = os.path.join(version_dir, "srlua.exe")
    srglue_exe = os.path.join(version_dir, "srglue.exe")
    if not os.path.isfile(srlua_exe):
        raise RuntimeError(f"lua_to_exe: Missing {srlua_exe}")
    if not os.path.isfile(srglue_exe):
        raise RuntimeError(f"lua_to_exe: Missing {srglue_exe}")
    return srglue_exe, srlua_exe

def _ensure_extension(filepath, ext):
    if not filepath.lower().endswith(ext):
        return filepath + ext
    return filepath

def _file_exists(filepath):
    return os.path.isfile(filepath)

def lua_to_exe(lua_file, exe_file, lua_version=_DEFAULT_LUA_VERSION):
    """
    Convert Lua script to executable file using the given Lua version.

    Parameters:
        lua_file (str): Input Lua file path
        exe_file (str): Output exe file path
        lua_version (str): Lua version folder name (default: 5.1.5-64)

    Raises:
        RuntimeError if conversion fails or input is invalid.
    """
    try:
        lua_file = _ensure_extension(lua_file, ".lua")
        exe_file = _ensure_extension(exe_file, ".exe")
        if not _file_exists(lua_file):
            raise RuntimeError(f"lua_to_exe: Cannot find input Lua file: {lua_file}")
        srglue, srlua_main = _get_srlua_path(lua_version)
        cmd = f'"{srglue}" "{srlua_main}" "{lua_file}" "{exe_file}"'
        process = subprocess.run(cmd, shell=True, check=True,
                                 capture_output=True, text=True)
        if _file_exists(exe_file):
            print(f"lua_to_exe: Successfully generated executable file: {exe_file}")
        else:
            raise RuntimeError("lua_to_exe: Generation failed")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"lua_to_exe: Command execution failed: {e.stderr}")
    finally:
        print('::: See more on https://github.com/Water-Run/luaToEXE :::')

def gui():
    """Launch GUI interface for file selection and conversion with Lua version selection."""
    root = tk.Tk()
    # 标题栏包含作者信息
    root.title("Lua to EXE Tool    by @WaterRun")
    # 固定窗口大小
    window_width = 700
    window_height = 520
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)  # 禁止拉伸

    primary_color = "#2196f3"
    secondary_color = "#03a9f4"
    text_color = "#212121"
    bg_color = "#ffffff"
    light_bg = "#f5f5f5"
    border_color = "#e0e0e0"

    main_frame = tk.Frame(root, bg=bg_color, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    # Header
    header = tk.Frame(main_frame, bg=bg_color)
    header.pack(fill="x", pady=(0, 15))
    canvas = tk.Canvas(header, width=50, height=50, bg=bg_color, highlightthickness=0)
    canvas.create_oval(5, 5, 45, 45, fill=primary_color, outline="")
    canvas.create_text(25, 25, text="L", fill="white", font=("Segoe UI", 20, "bold"))
    canvas.pack(side="left", padx=(0, 15))
    title_area = tk.Frame(header, bg=bg_color)
    title_area.pack(side="left", fill="y")
    title = tk.Label(
        title_area,
        text="Lua to EXE Converter",
        font=("Segoe UI", 24, "bold"),
        fg=text_color,
        bg=bg_color
    )
    title.pack(anchor="w")
    subtitle = tk.Label(
        title_area,
        text="Convert Lua scripts into standalone executables",
        font=("Segoe UI", 11),
        fg="#757575",
        bg=bg_color
    )
    subtitle.pack(anchor="w")
    version = tk.Label(
        header,
        text=f"v{__version__}",
        font=("Segoe UI", 10),
        fg="#9e9e9e",
        bg=bg_color
    )
    version.pack(side="right")

    separator = tk.Frame(main_frame, height=1, bg=border_color)
    separator.pack(fill="x", pady=15)

    content = tk.Frame(main_frame, bg=bg_color)
    content.pack(fill="both", expand=True)

    # Variables
    lua_file_path = tk.StringVar()
    exe_file_path = tk.StringVar()
    available_versions = all_available()
    selected_version = tk.StringVar(value=_DEFAULT_LUA_VERSION if _DEFAULT_LUA_VERSION in available_versions else (available_versions[0] if available_versions else ""))

    # File selection frame
    file_frame = tk.Frame(content, bg=bg_color)
    file_frame.pack(fill="x", pady=10)
    file_frame.columnconfigure(1, weight=1)

    # Lua file row
    tk.Label(
        file_frame,
        text="Lua File",
        font=("Segoe UI", 11),
        fg=text_color,
        bg=bg_color,
        anchor="w"
    ).grid(row=0, column=0, sticky="w", pady=10, padx=(0, 10))

    lua_entry_frame = tk.Frame(file_frame, bg=border_color, bd=1)
    lua_entry_frame.grid(row=0, column=1, sticky="ew", padx=5)
    lua_entry = tk.Entry(
        lua_entry_frame,
        textvariable=lua_file_path,
        font=("Segoe UI", 10),
        bd=0,
        highlightthickness=0
    )
    lua_entry.pack(fill="x", expand=True, ipady=8, padx=10)

    def browse_lua():
        filepath = filedialog.askopenfilename(
            filetypes=[("Lua Files", "*.lua"), ("All Files", "*.*")]
        )
        if filepath:
            lua_file_path.set(filepath)
            if not exe_file_path.get():
                base = os.path.splitext(filepath)[0]
                exe_file_path.set(base + ".exe")

    lua_browse = tk.Button(
        file_frame,
        text="Browse",
        command=browse_lua,
        bg=primary_color,
        fg="white",
        font=("Segoe UI", 10),
        bd=0,
        padx=15,
        pady=5
    )
    lua_browse.grid(row=0, column=2, padx=(5, 0), pady=10)

    # EXE file row
    tk.Label(
        file_frame,
        text="EXE File",
        font=("Segoe UI", 11),
        fg=text_color,
        bg=bg_color,
        anchor="w"
    ).grid(row=1, column=0, sticky="w", pady=10, padx=(0, 10))
    exe_entry_frame = tk.Frame(file_frame, bg=border_color, bd=1)
    exe_entry_frame.grid(row=1, column=1, sticky="ew", padx=5)
    exe_entry = tk.Entry(
        exe_entry_frame,
        textvariable=exe_file_path,
        font=("Segoe UI", 10),
        bd=0,
        highlightthickness=0
    )
    exe_entry.pack(fill="x", expand=True, ipady=8, padx=10)

    def browse_exe():
        filepath = filedialog.asksaveasfilename(
            defaultextension=".exe",
            filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")]
        )
        if filepath:
            exe_file_path.set(filepath)

    exe_browse = tk.Button(
        file_frame,
        text="Browse",
        command=browse_exe,
        bg=primary_color,
        fg="white",
        font=("Segoe UI", 10),
        bd=0,
        padx=15,
        pady=5
    )
    exe_browse.grid(row=1, column=2, padx=(5, 0), pady=10)

    # Lua version selection row
    tk.Label(
        file_frame,
        text="Lua Version",
        font=("Segoe UI", 11),
        fg=text_color,
        bg=bg_color,
        anchor="w"
    ).grid(row=2, column=0, sticky="w", pady=10, padx=(0, 10))

    version_frame = tk.Frame(file_frame, bg=bg_color)
    version_frame.grid(row=2, column=1, sticky="ew", padx=5)
    version_combo = ttk.Combobox(
        version_frame,
        textvariable=selected_version,
        values=available_versions,
        font=("Segoe UI", 10),
        state="readonly"
    )
    version_combo.pack(fill="x", expand=True, ipady=4, padx=10)

    def refresh_versions():
        versions = all_available()
        version_combo['values'] = versions
        if _DEFAULT_LUA_VERSION in versions:
            selected_version.set(_DEFAULT_LUA_VERSION)
        elif versions:
            selected_version.set(versions[0])
        else:
            selected_version.set("")
            convert_button.config(state="disabled")
            status_var.set("No Lua version available")
            messagebox.showwarning("No Lua Version Found",
                "No valid Lua versions detected in 'srlua/' folder.\n"
                "Please ensure at least one version exists (e.g., '5.1.5-64') with both srlua.exe and srglue.exe."
            )
        if versions:
            convert_button.config(state="normal")

    refresh_btn = tk.Button(
        file_frame,
        text="↻",  # Unicode refresh symbol
        font=("Segoe UI", 10, "bold"),
        bg=bg_color,
        fg=primary_color,
        bd=0,
        command=refresh_versions,
        cursor="hand2"
    )
    refresh_btn.grid(row=2, column=2, padx=(5, 0), pady=10)

    # Status panel
    status_frame = tk.Frame(content, bg=light_bg, bd=0)
    status_frame.pack(fill="x", pady=(20, 15))
    status_var = tk.StringVar()
    status_var.set("Ready to convert")
    status_inner = tk.Frame(status_frame, bg=light_bg, padx=15, pady=10)
    status_inner.pack(fill="x")
    indicator = tk.Canvas(status_inner, width=12, height=12, bg=light_bg, highlightthickness=0)
    indicator.create_oval(1, 1, 11, 11, fill="#4caf50", outline="")
    indicator.pack(side="left")
    status_text = tk.Label(
        status_inner,
        textvariable=status_var,
        bg=light_bg,
        fg=text_color,
        font=("Segoe UI", 11)
    )
    status_text.pack(side="left", padx=(8, 0))

    # Convert button
    button_area = tk.Frame(content, bg=bg_color)
    button_area.pack()
    convert_button = tk.Button(
        button_area,
        text="Convert",
        command=lambda: convert(),
        bg=primary_color,
        fg="white",
        font=("Segoe UI", 12, "bold"),
        width=15,
        bd=0,
        padx=10,
        pady=8
    )
    convert_button.pack(pady=5)

    def convert():
        lua_file = lua_file_path.get()
        exe_file = exe_file_path.get()
        lua_version = selected_version.get()
        if not lua_file:
            messagebox.showerror("Error", "Please select a Lua file")
            return
        if not exe_file:
            messagebox.showerror("Error", "Please select an output EXE file path")
            return
        if not lua_version:
            messagebox.showerror("Error", "No Lua version available")
            return
        status_var.set("Converting...")
        indicator.delete("all")
        indicator.create_oval(1, 1, 11, 11, fill="#ff9800", outline="")
        root.update()
        try:
            lua_to_exe(lua_file, exe_file, lua_version)
            status_var.set("Conversion successful")
            indicator.delete("all")
            indicator.create_oval(1, 1, 11, 11, fill="#4caf50", outline="")
            messagebox.showinfo("Success", f"Successfully converted {lua_file} to {exe_file} (Lua {lua_version})")
        except Exception as e:
            status_var.set("Conversion failed")
            indicator.delete("all")
            indicator.create_oval(1, 1, 11, 11, fill="#f44336", outline="")
            messagebox.showerror("Error", str(e))

    # 只保留一行底部GitHub链接，居中显示
    github_bottom_frame = tk.Frame(main_frame, bg=bg_color)
    github_bottom_frame.pack(fill="x", side="bottom", pady=(18, 8))
    github_main_link = tk.Label(
        github_bottom_frame,
        text="🌐  GitHub: https://github.com/Water-Run/luaToEXE",
        font=("Segoe UI", 11, "bold", "underline"),
        fg=primary_color,
        bg=bg_color,
        cursor="hand2"
    )
    github_main_link.pack(anchor="center")

    def open_github(event):
        import webbrowser
        webbrowser.open("https://github.com/Water-Run/luaToEXE")
    github_main_link.bind("<Button-1>", open_github)
    github_main_link.bind("<Enter>", lambda e: github_main_link.config(fg=secondary_color))
    github_main_link.bind("<Leave>", lambda e: github_main_link.config(fg=primary_color))

    # 取消原有底部多余GitHub和attribution部分
    # defunct_code...

    def on_hover(event, button, color):
        button.config(bg=color)
    lua_browse.bind("<Enter>", lambda e: on_hover(e, lua_browse, secondary_color))
    lua_browse.bind("<Leave>", lambda e: on_hover(e, lua_browse, primary_color))
    exe_browse.bind("<Enter>", lambda e: on_hover(e, exe_browse, secondary_color))
    exe_browse.bind("<Leave>", lambda e: on_hover(e, exe_browse, primary_color))
    convert_button.bind("<Enter>", lambda e: on_hover(e, convert_button, secondary_color))
    convert_button.bind("<Leave>", lambda e: on_hover(e, convert_button, primary_color))

    def on_close():
        root.destroy()
        sys.exit(0)
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Warn if no Lua versions are available
    if not available_versions:
        messagebox.showwarning("No Lua Version Found",
            "No valid Lua versions detected in 'srlua/' folder.\n"
            "Please ensure at least one version exists (e.g., '5.1.5-64') with both srlua.exe and srglue.exe."
        )
        status_var.set("No Lua version available")
        convert_button.config(state="disabled")

    root.mainloop()
    
# 启动入口
if __name__ == "__main__":
    gui()
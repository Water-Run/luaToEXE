r"""
lua_to_exe Project Source Code
:author: WaterRun
:time: 2025-03-30
:file: lua_to_exe.py
"""

import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import platform
import sys

__version__ = "0.1"

def _get_srlua_path():
    """Get the srlua tool path dynamically"""
    # Check current operating system
    if platform.system() != 'Windows':
        raise RuntimeError("lua_to_exe: Only supports Windows platform")
    
    # Check system architecture
    if not platform.machine().endswith('64'):
        raise RuntimeError("lua_to_exe: Only supports 64-bit systems")
    
    # Get the package directory
    package_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the srlua directory path inside the package
    srlua_dir = os.path.join(package_dir, 'srlua')
    
    # Check if the srlua directory exists
    if not os.path.isdir(srlua_dir):
        raise RuntimeError(f"lua_to_exe: Cannot find srlua directory: {srlua_dir}")
    
    return srlua_dir

def _ensure_extension(filepath, ext):
    """Ensure file has the correct extension"""
    if not filepath.lower().endswith(ext):
        return filepath + ext
    return filepath

def _file_exists(filepath):
    """Check if file exists"""
    return os.path.isfile(filepath)

def lua_to_exe(lua_file, exe_file):
    """
    Convert Lua script to executable file
    
    Parameters:
    lua_file (str): Input Lua file path
    exe_file (str): Output exe file path
    
    Exceptions:
    RuntimeError: If an error occurs during conversion
    """
    # Ensure correct file extensions
    lua_file = _ensure_extension(lua_file, ".lua")
    exe_file = _ensure_extension(exe_file, ".exe")
    
    # Check if input file exists
    if not _file_exists(lua_file):
        raise RuntimeError(f"lua_to_exe: Cannot find input Lua file: {lua_file}")
    
    # Get srlua directory
    srlua_dir = _get_srlua_path()
    
    # Get srlua and srglue paths
    srglue = os.path.join(srlua_dir, "srglue.exe")
    srlua_main = os.path.join(srlua_dir, "srlua.exe")
    
    # Ensure necessary files exist
    if not _file_exists(srglue):
        raise RuntimeError(f"lua_to_exe: Missing {srglue}")
    if not _file_exists(srlua_main):
        raise RuntimeError(f"lua_to_exe: Missing {srlua_main}")
    
    # Build command
    cmd = f'"{srglue}" "{srlua_main}" "{lua_file}" "{exe_file}"'
    
    try:
        # Execute command
        process = subprocess.run(cmd, shell=True, check=True, 
                               capture_output=True, text=True)
        
        # Check if executable file was successfully generated
        if _file_exists(exe_file):
            print(f"lua_to_exe: Successfully generated executable file: {exe_file}")
        else:
            raise RuntimeError("lua_to_exe: Generation failed")
            
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"lua_to_exe: Command execution failed: {e.stderr}")

def gui():
    """Launch GUI interface for file selection and conversion"""
    # Create main window
    root = tk.Tk()
    root.title("Lua to EXE Tool")
    root.geometry("650x450")
    root.configure(bg="#ffffff")
    root.minsize(600, 400)

    # Color scheme
    primary_color = "#2196f3"    # Blue
    secondary_color = "#03a9f4"  # Light Blue
    text_color = "#212121"       # Near Black
    bg_color = "#ffffff"         # White
    light_bg = "#f5f5f5"         # Light Gray
    border_color = "#e0e0e0"     # Border color
    
    # Create main frame with padding
    main_frame = tk.Frame(root, bg=bg_color, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    
    # Header area
    header = tk.Frame(main_frame, bg=bg_color)
    header.pack(fill="x", pady=(0, 15))
    
    # Logo - blue circle with L
    canvas = tk.Canvas(header, width=50, height=50, bg=bg_color, highlightthickness=0)
    canvas.create_oval(5, 5, 45, 45, fill=primary_color, outline="")
    canvas.create_text(25, 25, text="L", fill="white", font=("Segoe UI", 20, "bold"))
    canvas.pack(side="left", padx=(0, 15))
    
    # Title area
    title_area = tk.Frame(header, bg=bg_color)
    title_area.pack(side="left", fill="y")
    
    # Title
    title = tk.Label(
        title_area, 
        text="Lua to EXE Converter",
        font=("Segoe UI", 20, "bold"),
        fg=text_color,
        bg=bg_color
    )
    title.pack(anchor="w")
    
    # Subtitle
    subtitle = tk.Label(
        title_area, 
        text="Convert Lua scripts into standalone executables",
        font=("Segoe UI", 11),
        fg="#757575",
        bg=bg_color
    )
    subtitle.pack(anchor="w")
    
    # Version
    version = tk.Label(
        header, 
        text=f"v{__version__}",
        font=("Segoe UI", 10),
        fg="#9e9e9e",
        bg=bg_color
    )
    version.pack(side="right")
    
    # Separator
    separator = tk.Frame(main_frame, height=1, bg=border_color)
    separator.pack(fill="x", pady=15)
    
    # Content area
    content = tk.Frame(main_frame, bg=bg_color)
    content.pack(fill="both", expand=True)
    
    # Create path variables
    lua_file_path = tk.StringVar()
    exe_file_path = tk.StringVar()
    
    # File selection frame
    file_frame = tk.Frame(content, bg=bg_color)
    file_frame.pack(fill="x", pady=10)
    
    # Configure grid columns
    file_frame.columnconfigure(1, weight=1)
    
    # Lua file row
    lua_label = tk.Label(
        file_frame,
        text="Lua File",
        font=("Segoe UI", 11),
        fg=text_color,
        bg=bg_color,
        anchor="w"
    )
    lua_label.grid(row=0, column=0, sticky="w", pady=10, padx=(0, 10))
    
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
            # Auto-set exe path if empty
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
    exe_label = tk.Label(
        file_frame,
        text="EXE File",
        font=("Segoe UI", 11),
        fg=text_color,
        bg=bg_color,
        anchor="w"
    )
    exe_label.grid(row=1, column=0, sticky="w", pady=10, padx=(0, 10))
    
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
    def convert():
        lua_file = lua_file_path.get()
        exe_file = exe_file_path.get()
        
        if not lua_file:
            messagebox.showerror("Error", "Please select a Lua file")
            return
        
        if not exe_file:
            messagebox.showerror("Error", "Please select an output EXE file path")
            return
        
        status_var.set("Converting...")
        indicator.delete("all")
        indicator.create_oval(1, 1, 11, 11, fill="#ff9800", outline="")
        root.update()
        
        try:
            lua_to_exe(lua_file, exe_file)
            status_var.set("Conversion successful")
            indicator.delete("all")
            indicator.create_oval(1, 1, 11, 11, fill="#4caf50", outline="")
            messagebox.showinfo("Success", f"Successfully converted {lua_file} to {exe_file}")
        except Exception as e:
            status_var.set("Conversion failed")
            indicator.delete("all")
            indicator.create_oval(1, 1, 11, 11, fill="#f44336", outline="")
            messagebox.showerror("Error", str(e))
    
    button_area = tk.Frame(content, bg=bg_color)
    button_area.pack()
    
    convert_button = tk.Button(
        button_area,
        text="Convert",
        command=convert,
        bg=primary_color,
        fg="white",
        font=("Segoe UI", 12, "bold"),
        width=15,
        bd=0,
        padx=10,
        pady=8
    )
    convert_button.pack(pady=5)
    
    # Footer
    footer = tk.Frame(main_frame, bg=bg_color)
    footer.pack(fill="x", side="bottom", pady=(15, 0))
    
    # Left side - GitHub
    left_footer = tk.Frame(footer, bg=bg_color)
    left_footer.pack(side="left")
    
    gh_label = tk.Label(
        left_footer,
        text="GitHub:",
        font=("Segoe UI", 9),
        fg="#757575",
        bg=bg_color
    )
    gh_label.pack(side="left")
    
    gh_link = tk.Label(
        left_footer,
        text="github.com/Water-Run/luaToEXE",
        font=("Segoe UI", 9, "underline"),
        fg=primary_color,
        bg=bg_color,
        cursor="hand2"
    )
    gh_link.pack(side="left", padx=(4, 0))
    
    # Right side - Attribution
    attribution = tk.Label(
        footer,
        text="Based on srlua",
        font=("Segoe UI", 9),
        fg="#9e9e9e",
        bg=bg_color
    )
    attribution.pack(side="right")
    
    # GitHub link functionality
    def open_github(event):
        import webbrowser
        webbrowser.open("https://github.com/Water-Run/luaToEXE")
    
    gh_link.bind("<Button-1>", open_github)
    
    # Button hover effects
    def on_hover(event, button, color):
        button.config(bg=color)
    
    lua_browse.bind("<Enter>", lambda e: on_hover(e, lua_browse, secondary_color))
    lua_browse.bind("<Leave>", lambda e: on_hover(e, lua_browse, primary_color))
    
    exe_browse.bind("<Enter>", lambda e: on_hover(e, exe_browse, secondary_color))
    exe_browse.bind("<Leave>", lambda e: on_hover(e, exe_browse, primary_color))
    
    convert_button.bind("<Enter>", lambda e: on_hover(e, convert_button, secondary_color))
    convert_button.bind("<Leave>", lambda e: on_hover(e, convert_button, primary_color))
    
    gh_link.bind("<Enter>", lambda e: gh_link.config(fg=secondary_color))
    gh_link.bind("<Leave>", lambda e: gh_link.config(fg=primary_color))
    
    # Override close button to exit completely
    def on_close():
        root.destroy()
        sys.exit(0)
    
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    # Start main loop
    root.mainloop()
    
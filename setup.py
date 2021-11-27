from cx_Freeze import setup, Executable
import sys


base = None
if sys.platform == "win32":
    base = "Win32GUI"
    
executables = [Executable("Minecraft 2.0.py", base=base, icon="resources/icon.ico")]

setup(
    name="Minecraft 2.0",
    version="2.0",
    description="Minecraft 2.0 made with python!",
    executables=executables,
)
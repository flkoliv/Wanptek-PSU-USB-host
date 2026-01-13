import subprocess
import os

base_dir = os.path.dirname(__file__)
python = os.path.join(base_dir, ".venv", "Scripts", "pythonw.exe")

subprocess.Popen([python, "main.py"])
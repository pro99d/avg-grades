import subprocess
subprocess.run("pyinstaller --onefile --hidden-import my_module src/main.py".split())

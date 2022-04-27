import subprocess

subprocess.run("python3 manual_control.py & python3 manual_control_1.py --res 320x240 & python3 manual_control_2.py --res 320x240 & python3 manual_control_3.py --res 320x240 & python3 manual_control_4.py", shell=True)
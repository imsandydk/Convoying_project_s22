import subprocess
import argparse
import sys
import config

subprocess.run("python3 manual_control.py --convoy 6 & python3 manual_control_1.py --convoy 6 & python3 manual_control_2.py --convoy 6 --res 320x240 & python3 manual_control_3.py --convoy 6 & python3 manual_control_4.py --convoy 6", shell=True)

def main():
    parser = argparse.ArgumentParser(description='Run the specified test')
    parser.add_argument('--convoy', default=2,type=int,help='The test to run')
    args = parser.parse_args()
    if args.convoy == 2:
        subprocess.run("python3 manual_control.py --convoy 2", shell=True)
    elif args.convoy == 3:
        subprocess.run("python3 manual_control.py --convoy 3 & python3 manual_control_1.py --convoy 3", shell=True)
    elif args.convoy == 4:
        subprocess.run("python3 manual_control.py --convoy 4 & python3 manual_control_1.py --convoy 4 & python3 manual_control_2.py --convoy 4", shell=True)
    elif args.convoy == 5:
        subprocess.call("python3 manual_control.py --convoy 5 & python3 manual_control_1.py --convoy 5 & python3 manual_control_2.py --convoy 5 --res 320x240 & python3 manual_control_3.py --convoy 5", shell=True)
    elif args.convoy == 6:
        subprocess.run("python3 manual_control.py --convoy 6 & python3 manual_control_1.py --convoy 6 & python3 manual_control_2.py --convoy 6 --res 320x240 & python3 manual_control_3.py --convoy 6 & python3 manual_control_4.py --convoy 6", shell=True)


# if __name__ == "__main__":
#     sys.exit(main())    
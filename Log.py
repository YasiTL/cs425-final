import subprocess
import os

logFile = None

winCommand = "start cmd /k powershell Get-Content postgres.log -Wait"
unixCommand = "tail -f postgres.log"


def init():
    global logFile
    if os.name == "nt":
        logFile = open("postgres.log", "w", 20)
        subprocess.run(winCommand, shell=True)
    # TODO : Unix log file


def log(ID: str, string: str):
    global logFile
    if logFile != None:
        logFile.write("[{}] {}\n".format(ID, string))
        logFile.flush()
    else:
        print("[{}] {}".format(ID, string))
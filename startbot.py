#!/usr/bin/python3
import os
import subprocess

pgrep_proc = subprocess.Popen(['pgrep -af .*tchoupibot.py'], shell=True, stdout=subprocess.PIPE)
processes: list[bytes] = pgrep_proc.communicate("")[0].splitlines()

current_pid = str(os.getpid()).encode()
if current_pid in processes:
	processes.remove(current_pid)
print("DEBUG", processes)
if processes:
	print("Bot already running.")
	exit(1)
subprocess.run("python src/tchoupibot.py")
exit(0)
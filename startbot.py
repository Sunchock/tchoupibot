#!/usr/bin/python3
import os
import subprocess

pgrep_proc = subprocess.Popen(['pgrep -af .*tchoupibot.py'], shell=True, stdout=subprocess.PIPE)
processes: list[bytes] = pgrep_proc.communicate("")[0].splitlines()

print(subprocess.check_output(['pgrep -f .*tchoupibot.py'], shell=True))

current_pid = str(os.getpid()).encode()

print(processes, current_pid) # DEBUG
if current_pid in processes:
	processes.remove(current_pid)
print(processes, current_pid) # DEBUG
if processes:
	print("Bot already running.")
	exit(1)
bot_process = subprocess.run("python src/tchoupibot.py")
exit(0)
#!/usr/bin/python3
import os
import subprocess

# Entry point
if __name__ == "__main__":
	pgrep_proc = subprocess.Popen(['pgrep -f .*tchoupibot.py'], shell=True, stdout=subprocess.PIPE)
	processes: list[bytes] = pgrep_proc.communicate("")[0].splitlines()

	current_pid = str(os.getpid()).encode()

	print(processes, current_pid) # DEBUG
	if current_pid in processes:
		processes.remove(current_pid)
	print(processes, current_pid) # DEBUG
	if processes:
		print("Bot already running.")
		exit(1)
	else:
		print("Starting bot ...")
	exit(0)
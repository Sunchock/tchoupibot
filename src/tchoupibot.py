#!/usr/bin/python3
import logging
import os
import subprocess
import sys
import traceback

# Needed by host to load other files
sys.path.insert(0, os.path.dirname(__file__))

from core import TchoupiCore
from dotenv import load_dotenv

def __start():
	# Load .env file
	load_dotenv()
	try:
		core = TchoupiCore()
		core.run()
	except Exception:
		logging.error(traceback.format_exc())
		print("Unable to start core, exit.", file=sys.stderr)
		exit(1)

def tchoupibot(environ, start_response):
	start_response('200 OK', [('Content-type', 'text/plain')])
	yield b'Hello World\n'

# Entry point
if __name__ == "__main__":
	pgrep_proc = subprocess.Popen(['pgrep -f .*tchoupibot.py'], shell=True, stdout=subprocess.PIPE)
	processes: list[bytes] = pgrep_proc.communicate("")[0].splitlines()

	current_pid = str(os.getpid()).encode()
	pgrep_pid = str(pgrep_proc.pid).encode()

	print(processes, current_pid, pgrep_pid) # DEBUG
	if current_pid in processes:
		processes.remove(current_pid)
	print(processes, current_pid, pgrep_pid) # DEBUG
	if processes:
		print("Bot already running.")
	else:
		print("Starting bot ...")
		__start()
	exit(0)

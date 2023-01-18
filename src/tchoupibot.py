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
	pgrep_proc = subprocess.Popen(['pgrep -af .*tchoupibot.*'], shell=True, stdout=subprocess.PIPE)
	processes: list[bytes] = pgrep_proc.communicate("")[0].splitlines()

	print(processes, os.getpid(), pgrep_proc.pid) # DEBUG
	processes.remove(str(os.getpid()).encode())
	processes.remove(str(pgrep_proc.pid).encode())
	if processes:
		print("Bot already running.")
	else:
		print("Starting bot ...")
		__start()
	exit(0)

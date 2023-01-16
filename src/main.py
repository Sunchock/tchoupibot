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
	p = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)

	out, err = p.communicate()
	for line in out.splitlines():
		if 'tchoupibot'.encode('utf-8') in line:
			print("Bot already running.")
		else:
			__start()
			print("Bot started !")

# Entry point
if __name__ == "__main__":
	__start()
	exit(0)
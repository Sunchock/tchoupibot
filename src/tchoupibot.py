#!/usr/bin/python3
import logging
import os
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
		print("Starting bot ...")
		core.run()
		exit(0)
	except Exception:
		logging.error(traceback.format_exc())
		print("Unable to start core, exit.", file=sys.stderr)
		exit(1)

def tchoupibot(environ, start_response):
	start_response('200 OK', [('Content-type', 'text/plain')])
	yield b'Hello World\n'
	__start()

# Entry point
if __name__ == "__main__":
	__start()

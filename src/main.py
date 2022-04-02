#!/usr/bin/python3
import logging
import sys
import traceback
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

def application(environ, start_response):
	status = '200 OK'
	headers = [('Content-type', 'text/plain')]
	start_response(status, headers)
	__start()
	return [b'Hello World']

# Entry point
if __name__ == "__main__":
	__start()
	exit(0)
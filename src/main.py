#!/usr/bin/python3
from core import TchoupiCore
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Entry point
if __name__ == "__main__":
	tchoupi = TchoupiCore()
	tchoupi.run()
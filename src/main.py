#!/usr/bin/python3

import os
from dotenv import load_dotenv
from components.TchoupiBot import TchoupiBot

load_dotenv()

tchoupi = TchoupiBot()
tchoupi.run(os.getenv("TOKEN"))
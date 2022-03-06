#!/usr/bin/python3

import os
from dotenv import load_dotenv
from components.TchoupiBot import TchoupiBot

load_dotenv()

tchoupi_bot = TchoupiBot()
tchoupi_bot.run(os.getenv("TOKEN"))
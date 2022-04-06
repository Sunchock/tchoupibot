#!/usr/bin/python3
import logging
import os
import traceback
from components.TchoupiBot import TchoupiBot
from multiprocessing import Process, Queue

# Core class for manage commands and the discord bot
class TchoupiCore:
	__bot_process: Process = None
	__bot_queue: Queue = None
	__discord_bot: TchoupiBot = None


	# Init the core
	def __init__(self) -> None:
		# Queue for inter-process communication
		self.__bot_queue = Queue()

	"""
	
	"""
	# Get user input for custom commands (help, exit, ...)
	def get_user_input(self):
		# Get user input
		user_input: str = input("TchoupiBot> ")
		# Exit and free the bot process
		if user_input == "exit":
			print("TchoupiBot is shutting down...")
			if self.__discord_bot:
				self.__discord_bot.close()
			self.__bot_process.terminate()
			exit()
		# Print help
		elif user_input == "help":
			print("""help : Show this help message\nexit : Exit the bot""")
		# Unable to understand the user input
		else:
			print("Unknown command. Use help for more informations.")
		# Recursive call
		self.get_user_input()


	# Start the discord bot
	def __start_bot__(self):
		try:
			self.__discord_bot = TchoupiBot(self.__bot_queue)
			self.__discord_bot.run(os.getenv("TOKEN"))
		except Exception:
			logging.error(traceback.format_exc())


	# Start the core
	def run(self):
		self.__bot_process = Process(target=self.__start_bot__)
		self.__bot_process.start()
		print("TchoupiBot v0.1.0, use 'exit' to quit or 'help' for more options.")
		if self.__bot_queue.get() == "connected":
			self.get_user_input()
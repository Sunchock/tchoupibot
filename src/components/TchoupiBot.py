#!/usr/bin/python3
import discord
from discord.ext import commands
from multiprocessing import Queue

# Implement the discord integration
class TchoupiBot(commands.Bot):
	__bot_queue: Queue = None

	# catch 'on_ready' event
	async def on_ready(self):
		### DEBUG ###
		test_channel = self.get_channel(981822457046515712)
		await test_channel.send("TchoupiBot is connected")
		### DEBUG ###
		print(f"{self.user.display_name} is connected to Discord")
		self.__bot_queue.put("connected")

	def __init__(self, queue):
		self.__bot_queue = queue
		default_intents = discord.Intents.all()
		default_intents.members = True
		default_intents.reactions = True
		super().__init__(command_prefix="!", intents=default_intents)
		
		@self.command(name="hello")
		async def hello(ctx):
			welcome_channel = self.get_channel(853383864713871390)
			await welcome_channel.purge()
			await ctx.channel.purge()
			await ctx.send("""Bonjour ! Bienvenue sur le discord de la résidence Daniel Faucher :partying_face: !

				Pour avoir accès aux autres salons de ce serveur, tu dois d'abord lire et accepter les règles !

				1 : Soyez aimable et courtois
				2 : Pas d'incitation à la haine, ni de harcèlement
				3 : Respectez la confidentialité de tous
				4 : Pas de promotions idéologiques/commerciales

				Approuve les règles et obtiens tes accès avec l'émoji qui correspond au numéro de ton bâtiment :slight_smile: 

				Bât 1 : :one:  | Bât 2 : :two:  | Bât 3 : :three:  | Bât 4 : :four:  | Bât 5 : :five:  | Bât 6 : :six:  | Bât 7 : :seven:  | Bât 8 : :eight:
				
				En poursuivant ta navigation sur ce serveur, tu reconnais avoir pris connaissance et approuvé les règles énnoncées ci-dessus.""")
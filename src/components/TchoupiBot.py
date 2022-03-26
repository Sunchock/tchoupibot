#!/usr/bin/python3

import discord
from discord.ext import commands
from components.laundryScraper import laundryScraper

class TchoupiBot(commands.Bot):
	def __init__(self):
		default_intents = discord.Intents.default()
		default_intents.members = True 
		super().__init__(command_prefix="!", intents=default_intents)

		@self.command(name='laverie')
		async def laverie(ctx):
			scraper = laundryScraper.scrape()
			content = "Machines de la laverie en direct:\n"
			for machine in scraper:
				content += f"{machine['type']} \tn° **{machine['id']}**,\tEtat: **{machine['state']}**"
				if not machine['state']:
					content += f", Disponible dès : {machine['end_time']}"
				content += "\n"
			print(scraper)
			await ctx.send(content)
		
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

	async def on_ready(self):
		print(f"{self.user.display_name} est connecté au serveur.")

	# # To test
	# async def on_member_join(self, member):
	# 	general_chanel: discord.TextChannel = self.get_channel(697409297537171531)
	# 	await general_chanel.send(content=f"Bienvenue sur le serveur {member.display_name}")
	# 	print(f"{member.display_name} a rejoint le serveur !")
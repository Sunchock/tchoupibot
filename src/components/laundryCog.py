#!/usr/bin/python3
# Librairies
import discord
import time
from math import floor
from discord.ext import commands
# Custom classes
from components.laundryScraper import laundryScraper

# Retourne un nombre entre 1 et 12 pour l'emoji :clock{number}: de discord
# Basé sur le pourcentage restant du temps d'une opération (max 60min)
# get_clock_emoji_timer("08:37", "09:12") ->
def get_clock_emoji_timer(start_time: str, end_time: str) -> int:
	# calc = lambda x1, x2, y1, y2: (y1 - x1) * 60 - x2 + y2
	# floor(calc("8:57", current_time="9:12") * 12 / 60)
	
	# Conversion des arguments textes en nombres réels
	start = start_time.split(':')
	start_hour, start_min = start[0], start[1]
	if (end_time != '-'): # Fix pour le temps de fin non présent des LAVE LINGE 6 KG
		end = end_time.split(':')
		end_hour, end_min = end[0], end[1]
	else:
		end_hour, end_min = start[0] + 1, start[1]
	# Calcul du temps restant (max 60 minutes)
	remaining_time = abs((end_hour - start_hour) * 60 - start_min + end_min) % 60
	# Calcul du pourcentage
	return floor(remaining_time * 12 / 60) or 1

class laundryCog(commands.Cog):
	__laverie_enabled: bool = True
	__laverie_messages: list = []

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if reaction.message in self.__laverie_messages:
			if self.bot.user.id != user.id and reaction.emoji == "🔄":
				# Test-bot channel 981822457046515712
				test_channel = self.bot.get_channel(981822457046515712)
				print(f"{user.name} ({user.display_name}) a essayé de rafraichir la laverie")
				await test_channel.send(f"{user.name} ({user.display_name}) a essayé de rafraichir la laverie")
				await reaction.message.delete()
				embed_laundry = await self.laverie()
				if embed_laundry:
					message = await reaction.message.channel.send(embed=embed_laundry)
					self.__laverie_messages.append(message)
					await message.add_reaction("🔄")

	# Custom command to print laundry machines infos
	@commands.command(name='laverie')
	async def get_laundry_embed(self, ctx):
		### DEBUG ###
		test_channel = self.bot.get_channel(981822457046515712)
		await test_channel.send("'!laverie' called")
		### DEBUG ###
		embed_laundry: discord.Embed = await self.laverie()
		if embed_laundry:
			message = await ctx.send(embed=embed_laundry)
			self.__laverie_messages.append(message)
			await message.add_reaction("🔄")
		else:
			print('error: Unable to get machines list')

	async def laverie(self) -> discord.Embed:
		# Initialize the embed message
		embed_message: discord.Embed = discord.Embed(title="Laverie Proxiwash | Bâtiment 2", color=0x00ff00)
		embed_message.description = "Horaires d'ouverture: 7h - 23h"
		embed_message.url = "https://www.proxiwash.com/weblaverie/index.php/ma-laverie-2?s=444ec2&5376c3d89e9a678824fb1b6661d35851=1"
		# Laverie fermée (en dehors des horaires) ou si la commande 'laverie' est désactivée
		current_time = time.localtime()
		if (current_time.tm_hour < 7 or current_time.tm_hour >= 23) or not self.__laverie_enabled:
			embed_message.add_field(name="Laverie", value="La laverie est actuellement fermée. :x:")
			return embed_message
		# Récupère les informations pour la liste des machines
		machines_list: list[dict[str, str]] = laundryScraper.scrape()
		if machines_list:
			# Build the embed message
			for machine in machines_list:
				# Build embed entry
				machine_name: str = f"{machine['type']} n°{machine['id']} "
				machine_state: str = ""
				# Check for current machine state
				match machine['state']:
					case 'DISPONIBLE':
						machine_name += ":white_check_mark:"
						machine_state += "DISPONIBLE"
					case 'TERMINE':
						machine_name += ":ok:"
						machine_state += "TERMINÉE"
					case '':
						machine_name += f":clock{get_clock_emoji_timer(machine['start_time'], machine['end_time'])}:"
						machine_state += f"EN COURS, {machine['start_time']} => {machine['end_time']}."
					case _:
						machine_name += ":x:"
						machine_state += "Désactivée"
				# Add the entry to the embed message
				embed_message.add_field(name=machine_name, value=machine_state, inline=False)
			# Footer : dernière heure de mise à jour
			embed_message.set_footer(text="Dernière mise à jour : " + time.strftime("%H:%M:%S", current_time))
		else:
			embed_message.add_field(name="Erreur", value="Impossible d'obtenir les informations de la laverie :x:")
		return embed_message

	# Commande pour activer/désactiver la laverie
	@commands.command(name="set_laverie")
	@commands.check_any(commands.has_role(705756751139700779), commands.has_role(853388371372408842))
	async def set_laverie_state(self, ctx, state: str):
		self.__laverie_enabled = state.lower() in ("yes", "true", "1", "on")
		await ctx.send(f"Laverie is now {'enabled' if self.__laverie_enabled else 'disabled'}")
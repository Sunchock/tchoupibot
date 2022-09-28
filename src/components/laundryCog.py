#!/usr/bin/python3
import discord
from components.laundryScraper import laundryScraper
import time

from discord.ext import commands

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
		embed_message: discord.Embed = discord.Embed(title="Machines de la laverie | Bâtiment 2", color=0x00ff00)
		if not self.__laverie_enabled:
			embed_message.add_field(name="Laverie", value="La laverie est actuellement fermée. :x:")
			return embed_message
		machines_list: list[dict[str, str]] = laundryScraper.scrape()
		if machines_list:
			# Build the embed message
			for machine in machines_list:
				# Build embed entry
				machine_name: str = f"Machine {machine['id']} "
				machine_value: str = f"{machine['type']}, "
				# Check for current machine state
				if machine['state'] == 'DISPONIBLE':
					machine_name += ":white_check_mark:"
					machine_value += f"{machine['state']}"
				elif machine['state'] == 'TERMINE':
					machine_name += ":ok:"
					machine_value += "TERMINÉE"
				elif machine['state'] == '':
					machine_name += ":clock2:"
					if machine['end_time'] == '-':
						machine_value += "EN COURS"
					else:
						machine_value += f"Fin à {machine['end_time']}."
				else:
					machine_name += ":x:"
					machine_value = f"{machine['type']}, Désactivée"
				# Add the entry to the embed message
				embed_message.add_field(name=machine_name, value=machine_value, inline=False)
				# Add timestamp
				embed_message.set_footer(text="Dernière mise à jour : " + time.strftime("%H:%M:%S", time.localtime()))
		else:
			embed_message.add_field(name="Laverie", value="Erreur: impossible d'obtenir les informations :x:")
		return embed_message

	@commands.command(name="set_laverie")
	@commands.check_any(commands.has_role(705756751139700779), commands.has_role(853388371372408842))
	async def set_laverie_state(self, ctx, state: str):
		self.__laverie_enabled = state.lower() in ("yes", "true", "1", "on")
		await ctx.send(f"Laverie is now {'enabled' if self.__laverie_enabled else 'disabled'}")
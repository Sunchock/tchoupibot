import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path='.config')

class TchoupiBot(commands.Bot):
	def __init__(self):
		default_intents = discord.Intents.default()
		default_intents.members = True
		super().__init__(command_prefix="!tchoupi ", intents=default_intents)

		@self.command(name='test')
		async def tchoupi_help(ctx):
			admin_chanel: discord.TextChannel = self.get_channel(705763034295173120)
			await admin_chanel.send(content="Liste des commandes :")
			await admin_chanel.send(content="Aucune ! Le bot est en travaux dsl")
			print("call tchoupi's help")

	async def on_ready(self):
		print(f"{self.user.display_name} est connecté au serveur.")

	# To test
	async def on_member_join(self, member):
		general_chanel: discord.TextChannel = self.get_channel(697409297537171531)
		await general_chanel.send(content=f"Bienvenue sur le serveur {member.display_name}")
		print(f"{member.display_name} a rejoint le serveur !")

tchoupi_bot = TchoupiBot()
tchoupi_bot.run(os.getenv("TOKEN"))

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path='.config')

default_intents = discord.Intents.default()
default_intents.members = True
bot = commands.Bot(command_prefix="!tchoupi ", intents=default_intents)

@bot.event
async def on_ready():
	print("Le bot est prêt !")

@bot.command(name="test")
async def tchoupi_help(ctx):
	admin_chanel: discord.TextChannel = bot.get_channel(705763034295173120)
	await admin_chanel.send(content="Liste des commandes :")
	await admin_chanel.send(content="Aucune ! Le bot est en travaux dsl")
	print("call tchoupi's help")

@bot.event
async def on_member_join(member):
	general_chanel: discord.TextChannel = bot.get_channel(697409297537171531)
	await general_chanel.send(content=f"Bienvenue sur le serveur {member.display_name}")
	print(f"{member.display_name} a rejoint le serveur !")

bot.run(os.getenv("TOKEN"))
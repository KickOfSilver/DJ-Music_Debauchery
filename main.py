import os
import json
import discord
from discord import app_commands

# Importando funções e comandos personalizados
from bot.functions.commands_check import *
from bot.functions.bot_profile import *
from bot.commands.play import *

# Carregando as informações de configuração do arquivo config.json
with open("config.json") as f:
    config = json.load(f)
os.system("cls")

# Configuração do bot
BOT_ID = config["BOT_ID"]
TOKEN = config["TOKEN"]
PREFIX = config["PREFIX"]
INTENTS = discord.Intents.all()  # para que o bot possa receber eventos de membros

# Configurando guilda do bot
AAA = discord.Object(id=986769650119483442)
MY_GUILD = None


# Definição da classe MusicBot
class MusicBot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=AAA)
        await self.tree.sync(guild=AAA)

    async def on_ready(self):
        await set_bot_activity(self, PREFIX)

        print(f"{self.user.name} Online")


# Criação do objeto client da classe MusicBot e definição da guilda do bot
client = MusicBot(intents=INTENTS)
MY_GUILD = client.get_guild(986769650119483442)


# Definição do evento on_message
@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    if message.content.startswith(f"{PREFIX}play"):
        if not await check_command_message(client, message, audio=True):
            return

        await music_search(client, message)


# Definição do comando play na árvore de comandos
@client.tree.command(name="play", description="play music")
async def play_music(interaction, musica: str):
    message = interaction.data['options'][0]['value']
    print(message)
    # await music_search(client, message)

# Execução do bot
client.run(TOKEN)

import os
import json
import discord

# Funções personalizadas
from functions.commands_check import *
from functions.bot_profile import *

# Comandos personalizados
from commands.play import *

# Carregando as informações de configuração do arquivo config.json
with open("config.json") as f:
    config = json.load(f)
os.system("cls")

# Configuração do bot
BOT_ID = config["BOT_ID"]
TOKEN = config["TOKEN"]
PREFIX = config["PREFIX"]
INTENTS = discord.Intents.all()


class MusicBot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)

    async def on_ready(self):
        await set_bot_activity(self, PREFIX)

        print(f"{self.user.name} Online")

    async def on_message(self, message):
        if message.author == self.user or message.author.bot:
            return

        if message.content.startswith(f"{PREFIX}play"):
            if not await check_command_message(self, message, audio=True):
                return

            await music_search(client, message)


intents = discord.Intents.all()  # para que o bot possa receber eventos de membros
client = MusicBot(intents=INTENTS)
client.run(TOKEN)

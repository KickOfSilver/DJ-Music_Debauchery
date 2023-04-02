import os
import json
import discord
from functions.commands_check import *
from functions.bot_profile import *


# Carregando as informações de configuração do arquivo config.json
with open("config.json") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]
PREFIX = config["PREFIX"]


class MusicBot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)

    async def on_ready(self):
        await set_bot_activity(self, PREFIX)

        os.system("cls")
        print(f"{self.user.name} Online")

    async def on_message(self, message):
        if message.author == self.user or message.author.bot:
            return

        if message.content.startswith(f"{PREFIX}play"):
            if not await check_command_message(self, message, audio=True):
                return

            print("feito")


intents = discord.Intents.all()  # para que o bot possa receber eventos de membros
client = MusicBot(intents=intents)
client.run(TOKEN)

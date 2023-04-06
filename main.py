import os
import json
import discord
from datetime import datetime
from discord import app_commands

# Importando funções e comandos personalizados
from bot.functions.MyBot.profile import set_bot_activity
from bot.functions.commands.check import check_command_message
from bot.functions.commands.registration import update_slash_commands
from bot.commands.search import music_search

# Carregando as informações de configuração do arquivo config.json
with open("config.json") as f:
    config = json.load(f)
os.system("cls")

# Configuração do bot
BOT_ID = config["BOT_ID"]
TOKEN = config["TOKEN"]
PREFIX = config["PREFIX"]
INTENTS = discord.Intents.all()  # para que o bot possa receber eventos de membros


# Definição da classe MusicBot
class MusicBot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await set_bot_activity(self, PREFIX)
        await update_slash_commands(self)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time = "\033[90m" + current_time + "\033[0m"
        info = f"\033" + "[36mINFO" + "\033[0m"
        user_bot = "\033[35m" + f"{self.user.name}" + "\033[0m"
        print(f"{time} {info}     {user_bot} Olá! Estou online e pronto para ajudar!")

    async def on_guild_join(self, guild):
        await update_slash_commands(self)


# Criação do objeto client da classe MusicBot e definição da guilda do bot
client = MusicBot(intents=INTENTS)


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
@client.tree.command(name="play", description="consulta")
async def play_music(interaction, musica: str):
    message = interaction.data['options'][0]['value']
    print(message)
    # await music_search(client, message)

# Execução do bot
client.run(TOKEN)

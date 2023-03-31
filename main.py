import asyncio
import os
import discord
import youtube_dl
from dotenv import load_dotenv

ffmpeg = "ffmpeg/ffmpeg.exe"


class MyClient(discord.Client):
    async def on_ready(self):
        print("Estou pronto")

    async def on_message(self, message):
        if message.author == self.user:  # ignorar mensagens enviadas pelo bot
            return
        if message.content.startswith("!play "):
            # obter a consulta de pesquisa do usuário
            query = message.content[6:]

            voice_channel = message.author.voice.channel  # obter o canal de voz do usuário
            if not voice_channel:  # o usuário não está conectado a um canal de voz
                await message.channel.send("Você precisa estar em um canal de voz para tocar música!")
                return

            if message.guild.voice_client is not None:  # o bot já está conectado a um canal de voz
                await message.channel.send(f"O bot já está sendo usado no canal de voz {message.guild.voice_client.channel.name}!")
                return  

            voice_client = await voice_channel.connect()  # conectar ao canal de voz

            try:
                # baixar a música do YouTube
                ydl_opts = {"format": "bestaudio", "noplaylist": "True"}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f"ytsearch:{query}", download=False)[
                        'entries'][0]
                    url = info['url']
                    title = info['title']

                # tocar a música
                source = discord.FFmpegPCMAudio(
                    url, executable=ffmpeg)
                voice_client.play(source)
                await message.channel.send(f"Tocando: {title}")

                # tocar a próxima música na lista
                while voice_client.is_playing():
                    await asyncio.sleep(5)
                await voice_client.disconnect()

            except Exception as e:
                await message.channel.send(f"Ocorreu um erro ao tocar a música: {e}")
                await voice_client.disconnect()


load_dotenv()  # carrega as variáveis de ambiente do arquivo .env
TOKEN = os.getenv("DISCORD_TOKEN")  # obtém o token do Discord do arquivo .env

intents = discord.Intents.all()  # para que o bot possa receber eventos de membros
client = MyClient(intents=intents)
client.run(TOKEN)

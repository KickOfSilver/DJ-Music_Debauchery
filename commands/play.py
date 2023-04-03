import asyncio
import pytube
import youtube_dl
from youtubesearchpython import VideosSearch


YT_SEARCH = ""
PLAY_LIST = []


async def music_search(client, message):

    YT_SEARCH = message.content.split(' ', 1)[1].strip()

    if "playlist?list" in YT_SEARCH:
        playlist = pytube.Playlist(YT_SEARCH)

        for video in playlist.videos:
            PLAY_LIST.append(video.watch_url)

    elif "watch?v" in YT_SEARCH:
        PLAY_LIST.append(YT_SEARCH)

    else:
        video = videos = VideosSearch(YT_SEARCH, limit=5).result()["result"]
        if not video:
            await message.channel.send(f"Não foi possível encontrar resultados para {YT_SEARCH}!")
            return False

        results_message = "Escolha uma das opções abaixo:\n"

        for i, video in enumerate(videos):
            results_message += f"{i+1}. {video['title']} ({video['duration']})\n"

        results_message += "Digite o número correspondente à opção desejada ou 'cancel' para cancelar a busca."

        await message.channel.send(results_message)

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            msg = await client.wait_for("message", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send("Tempo limite para escolher uma opção atingido.")
            return False

        choice = msg.content.strip().lower()

        if choice == "cancel":
            await message.channel.send("Busca cancelada.")
            return False

        try:
            choice = int(choice) - 1
            video_url = f"https://www.youtube.com/watch?v={videos[choice]['id']}"
            PLAY_LIST.append(video_url)
            await message.channel.send(f"Vídeo adicionado à lista de reprodução: {video_url}")
        except (ValueError, IndexError):
            await message.channel.send("Opção inválida. Busca cancelada.")
            return False

    print(PLAY_LIST)

    # try:
    #     # Verificar se o usuário inseriu um link
    #     if "youtube.com/watch?" in YT_SEARCH or "youtube.com/playlist?" in YT_SEARCH:
    #         ydl_opts = {"format": "bestaudio", "noplaylist": "True"}
    #         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #             info = ydl.extract_info(YT_SEARCH, download=False)

    #             # Se for uma playlist, adicionar cada vídeo à lista de reprodução
    #             if 'entries' in info:
    #                 for entry in info['entries']:
    #                     url = entry['url']
    #                     title = entry['title']
    #                     PLAY_LIST.append((url, title))

    #             # Se for um vídeo, adicionar à lista de reprodução
    #             else:
    #                 url = info['url']
    #                 title = info['title']
    #                 PLAY_LIST.append((url, title))

    #     # Se não for um link, pesquisar no YouTube
    #     else:
    #         ydl_opts = {"format": "bestaudio", "noplaylist": "True"}
    #         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #             info = ydl.extract_info(f"ytsearch:{YT_SEARCH}", download=False)[
    #                 'entries'][0]
    #             url = info['url']
    #             title = info['title']
    #             PLAY_LIST.append((url, title))

    # except:
    #     print("Erro ao adicionar na lista de reprodução")

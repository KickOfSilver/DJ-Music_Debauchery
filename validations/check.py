async def check_command_message(self, message, audio=True):

    # Verificar se o autor da mensagem está em um canal de voz
    if audio and not message.author.voice:
        await message.channel.send("Você precisa estar em um canal de voz para usar este comando.")
        return False

    # Verificar se o bot já está em um canal de voz diferente
    if audio and not message.guild.voice_client is None and message.author.voice.channel != message.guild.voice_client.channel:
        await message.channel.send("O bot já está sendo usado em outro canal de voz. Você precisa estar no mesmo canal de voz que o bot para usar este comando!")
        return False

    # Verificar as permissões do bot para se conectar ao canal de voz
    if audio and not message.author.voice.channel.permissions_for(message.guild.me).connect:
        await message.channel.send("O bot não tem permissão para entrar neste canal de voz!")
        return False

    # Verificar as permissões do bot para reproduzir música
    if audio and not message.author.voice.channel.permissions_for(message.guild.me).speak:
        await message.channel.send("O bot não tem permissão para reproduzir música neste canal de voz!")
        return False

    return True

from discord import app_commands


async def update_slash_commands(bot):
    # Adiciona ou atualiza os slash commands em todos os servidores em que o bot está presente
    for guild in bot.guilds:
        # Obtém a instância do objeto ApplicationCommandManager do servidor
        command_manager = guild.get_application_command_manager()

        # Adiciona ou atualiza os slash commands na instância do objeto ApplicationCommandManager
        await command_manager.set_global_commands(
            [app_commands.Command(name="test", description="Apenas um teste")]
        )

from discord import app_commands


async def update_slash_commands(self):
    # Adiciona ou atualiza os slash commands em todos os servidores em que o bot está presente
    for guild in self.guilds:
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

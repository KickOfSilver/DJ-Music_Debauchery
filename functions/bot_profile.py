import discord


async def set_bot_activity(self, PREFIX):
    active_channels = 0
    for guild in self.guilds:
        for member in guild.members:
            if member.voice and member.voice.self_stream:
                active_channels += 1
    atividade = discord.Activity(
        type=discord.ActivityType.listening, name=f"{PREFIX}help | {active_channels} CHANNELS")
    await self.change_presence(activity=atividade)

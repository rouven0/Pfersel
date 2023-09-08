import discord
from discord.ext import commands


class Pin(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message: discord.Message = await channel.fetch_message(payload.message_id)
        if payload.emoji.name == "📌":
            await message.pin()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message: discord.Message = await channel.fetch_message(payload.message_id)
        if payload.emoji.name == "📌" and "📌" not in [reaction.emoji for reaction in message.reactions]:
            await message.unpin()
            await channel.send(
                embed=discord.Embed(
                    description=":white_check_mark: Nachricht wurde von der Pinnwand entfernt.",
                    colour=discord.Colour.green(),
                )
            )


def setup(bot):
    bot.add_cog(Pin(bot))

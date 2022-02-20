from discord.ext import commands


class Tags(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.slash_command(guild_ids=[886583607806787604, 681868752681304066])
    async def codeblocks(self, ctx):
        """Anleitung um Programmcode schön darzustellen"""
        with open("./codeblocks.md", "r") as file:
            await ctx.respond(file.read())


def setup(bot):
    bot.add_cog(Tags(bot))

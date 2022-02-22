from random import randint
import discord
from discord.ext import commands
from discord.commands import Option, OptionChoice
import database

con = database.__con__
cur = database.__cur__


def get_matching_quotes(ctx):
    choices = []
    cur.execute("SELECT * from quotes where quote like ?", ("%" + ctx.value + "%",))
    for record in cur.fetchmany(25):
        choices.append(OptionChoice(name=record[1][:100], value=int(record[0])))
    return choices


class Quotes(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.slash_command(guild_ids=[886583607806787604, 681868752681304066])
    async def quote(self, ctx, suche: Option(int, "Suchst du was?", autocomplete=get_matching_quotes) = 0):
        """Schaue dir einen wunderschönen quote an"""
        if suche <= 0:
            suche = randint(1, 172)
        cur.execute("SELECT * from quotes where number=?", (int(suche),))
        record = cur.fetchone()
        await ctx.respond(f"{record[1]} {record[3]}")


def setup(bot):
    bot.add_cog(Quotes(bot))

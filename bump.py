from time import time
import discord
from discord.ext import commands
from discord.ext import tasks
import re

import bumpers


class Bump(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_bump.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 302050872383242240:
            match = re.match(r"<@!*(\d+)>.*:thumbsup:", message.embeds[0].description)
            if match:
                bumper_id = int(match.groups()[0])
                next_bump = round(time()) + 7200
                time_file = open("./next_bump.txt", "w")
                time_file.write(str(next_bump))
                time_file.close()
                try:
                    bumper = bumpers.get(bumper_id)
                    bumpers.add_bump(bumper)
                except bumpers.BumperNotRegistered:
                    bumpers.insert(bumper_id)
                await message.add_reaction(self.bot.get_emoji(811622525636182086))
                await message.channel.send(
                    embed=discord.Embed(
                        description=f"Der nächste bump ist <t:{next_bump}:R>", colour=discord.Colour.green()
                    )
                )
                return
            match = re.match(r".*noch (\d{1,3}) Minute", message.embeds[0].description)
            if match:
                next_bump = round(time()) + int(match.groups()[0]) * 60
                time_file = open("./next_bump.txt", "w")
                time_file.write(str(next_bump))
                time_file.close()
                await message.add_reaction("🕙")

    @tasks.loop(seconds=2)
    async def check_bump(self):
        time_file = open("./next_bump.txt", "r")
        next_bump = int(time_file.readline())
        time_file.close()
        if next_bump == 0:
            return
        if next_bump < time():
            bump_channel = await self.bot.fetch_channel(771742240229031947)
            pinged = bumpers.get_pinged()
            message = ":eyes:"
            for user in pinged:
                message += f" <@{user[0]}>"
            await bump_channel.send(
                message,
                embed=discord.Embed(
                    title="Es ist wieder Zeit für einen Bump", description="!d bump", colour=discord.Colour.green()
                ),
            )
            time_file = open("./next_bump.txt", "w")
            time_file.write(str(0))
            time_file.close()

    @commands.slash_command(guild_ids=[886583607806787604, 681868752681304066])
    async def ping(self, ctx, toggle: bool):
        """Willst du bei remindern gepingt werden?"""
        try:
            bumper = bumpers.get(ctx.author.id)
        except bumpers.BumperNotRegistered:
            await ctx.respond("Du musst mindestens einmal gebumpt haben, um diesen Command zu benutzen")
            return

        if toggle:
            bumpers.enable_ping(bumper)
            await ctx.respond("Dein Ping wurde aktiviert")
        else:
            bumpers.disable_ping(bumper)
            await ctx.respond("Dein Ping wurde deaktiviert")

    @commands.slash_command(guild_ids=[886583607806787604, 681868752681304066])
    async def next(self, ctx):
        """Nächster bump"""
        time_file = open("./next_bump.txt", "r")
        next_bump = int(time_file.readline())
        time_file.close()
        if next_bump == 0:
            msg = "Der nächste bump ist **JETZT**"
        else:
            msg = f"Der nächste bump ist <t:{next_bump}:T>"
        await ctx.respond(embed=discord.Embed(description=msg, colour=discord.Colour.green()))

    @commands.slash_command(guild_ids=[886583607806787604, 681868752681304066])
    async def top(self, ctx):
        """Die ehrenwertesten bumper"""
        top_content = ""
        top_tuple = bumpers.get_top()
        total_bumps = 0
        for i in range(0, len(top_tuple)):
            top_content += f"**{i+1}** <@{top_tuple[i][0]}> {top_tuple[i][1]} bumps \n"
            total_bumps += top_tuple[i][1]
        top_embed = discord.Embed(
            title="Manasoup top list", description=top_content, colour=discord.Colour.dark_green()
        )
        top_embed.set_footer(text=f"Bumps insgesamt: {total_bumps}")
        await ctx.respond(embed=top_embed)

    @commands.slash_command(guild_ids=[886583607806787604])
    async def rescue(self, ctx):
        if ctx.author.id not in [235046787122069504, 692796548282712074]:
            return
        await ctx.channel.send("Reminder gesetzt")
        time_file = open("./next_bump.txt", "w")
        time_file.write(str(round(time()) + 7200))
        time_file.close()


def setup(bot):
    bot.add_cog(Bump(bot))

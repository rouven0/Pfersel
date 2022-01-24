from time import time
import logging
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands.errors import MissingRequiredArgument
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
            match = re.match(r"<@!*(\d+)>.*👍", message.embeds[0].description)
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

    @commands.command()
    async def ping(self, ctx, toggle: str):
        try:
            bumper = bumpers.get(ctx.author.id)
        except bumpers.BumperNotRegistered:
            await ctx.channel.send("Du musst mindestens einmal gebumpt haben, um diesen Command zu benutzen")
            return

        if toggle in ["on", "enable"]:
            bumpers.enable_ping(bumper)
            await ctx.reply("Dein Ping wurde aktiviert")
        elif toggle in ["off", "disable"]:
            bumpers.disable_ping(bumper)
            await ctx.reply("Dein Ping wurde deaktiviert")
        else:
            await ctx.channel.send("**Syntax:** mana ping [on/off]")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            # angepasst auf den ping command
            await ctx.channel.send("**Syntax:** mana ping [on/off]")
        else:
            logging.error(error)

    @commands.command()
    async def next(self, ctx):
        time_file = open("./next_bump.txt", "r")
        next_bump = int(time_file.readline())
        time_file.close()
        if next_bump == 0:
            msg = "Der nächste bump ist **JETZT**"
        else:
            msg = f"Der nächste bump ist <t:{next_bump}:t>"
        await ctx.channel.send(embed=discord.Embed(description=msg, colour=discord.Colour.green()))

    @commands.command()
    async def top(self, ctx):
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
        await ctx.channel.send(embed=top_embed)

    @commands.command()
    async def rescue(self, ctx):
        if ctx.author.id not in [235046787122069504, 692796548282712074]:
            return
        await ctx.channel.send("Reminder gesetzt")
        time_file = open("./next_bump.txt", "w")
        time_file.write(str(round(time()) + 7200))
        time_file.close()


def setup(bot):
    bot.add_cog(Bump(bot))

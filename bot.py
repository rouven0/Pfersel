from time import time
import discord
from discord.ext import commands, tasks
import logging

from discord.ext.commands.errors import MissingRequiredArgument
import bumpers
import config

bot = commands.Bot(
    command_prefix=["!d ", "!D ", "mana "], help_command=None, case_insensitive=True, strip_after_prefix=True
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(config.LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(console_handler)


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.streaming, name="Blender", url="https://www.twitch.tv/manasoup_dev"
        )
    )


@bot.command(aliases=["p"])
async def profile(ctx):
    try:
        bumper = bumpers.get(ctx.author.id)
    except bumpers.BumperNotRegistered:
        await ctx.channel.send("Du musst mindestens einmal gebumpt haben, um diesen Command zu benutzen")
        return
    profile_embed = discord.Embed(description=f"{bumper.bumps} bumps")
    profile_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=profile_embed)


@bot.command()
async def bump(ctx):
    def check(message):
        return message.author.id == 302050872383242240

    if ctx.prefix in (["!d ", "!D "]):
        response: discord.Message = await bot.wait_for("message", check=check)
        if ":thumbsup:" in response.embeds[0].description:
            next_bump = round(time()) + 7200
            time_file = open("./next_bump.txt", "w")
            time_file.write(str(next_bump))
            time_file.close()
            try:
                bumper = bumpers.get(ctx.author.id)
                bumpers.add_bump(bumper)
            except bumpers.BumperNotRegistered:
                bumpers.insert(ctx.author.id)
            await response.add_reaction(bot.get_emoji(811622525636182086))
            await ctx.channel.send(
                embed=discord.Embed(
                    description=f"Der nächste bump ist <t:{next_bump}:R>", colour=discord.Colour.green()
                )
            )
        elif "Bitte warte" in response.embeds[0].description:
            await response.add_reaction("🕑")
        else:
            await ctx.channel.send(
                "Irgendwas ist falsch gelaufen :( ||<@692796548282712074> fix your bot <:dachs:788347876601364532>||"
            )


@tasks.loop(seconds=2)
async def check_bump():
    time_file = open("./next_bump.txt", "r")
    next_bump = int(time_file.readline())
    time_file.close()
    if next_bump == 0:
        return
    if next_bump < time():
        bump_channel = await bot.fetch_channel(771742240229031947)
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


@bot.command()
async def ping(ctx, toggle: str):
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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        # angepasst auf den ping command
        await ctx.channel.send("**Syntax:** mana ping [on/off]")
    else:
        logging.error(error)


@bot.command()
async def next(ctx):
    time_file = open("./next_bump.txt", "r")
    next_bump = int(time_file.readline())
    time_file.close()
    if next_bump == 0:
        msg = "Der nächste bump ist **JETZT**"
    else:
        msg = f"Der nächste bump ist <t:{next_bump}:t>"
    await ctx.channel.send(embed=discord.Embed(description=msg, colour=discord.Colour.green()))


@bot.command()
async def top(ctx):
    top_content = ""
    top_tuple = bumpers.get_top()
    total_bumps = 0
    for i in range(0, len(top_tuple)):
        top_content += f"**{i+1}** <@{top_tuple[i][0]}> {top_tuple[i][1]} bumps \n"
        total_bumps += top_tuple[i][1]
    top_embed = discord.Embed(title="Manasoup top list", description=top_content, colour=discord.Colour.dark_green())
    top_embed.set_footer(text=f"Bumps insgesamt: {total_bumps}")
    await ctx.channel.send(embed=top_embed)


@bot.command()
async def rescue(ctx):
    if ctx.author.id not in [235046787122069504, 692796548282712074]:
        return
    await ctx.channel.send("Reminder gesetzt")
    time_file = open("./next_bump.txt", "w")
    time_file.write(str(round(time()) + 7200))
    time_file.close()


check_bump.start()
bot.load_extension("welcome")
bot.load_extension("pin")


bot.run("ODY4MTA0MzM2Mzk0MjkzMjcx.YPqzKg.YDcWCyM9BOszebhzfjXx9TeaQlY")

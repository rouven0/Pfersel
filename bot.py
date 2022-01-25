import discord
from discord.ext import commands
import logging

import config

bot = commands.Bot(command_prefix=["mana "], help_command=None, case_insensitive=True, strip_after_prefix=True)
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


bot.load_extension("welcome")
bot.load_extension("bump")


bot.run("ODY4MTA0MzM2Mzk0MjkzMjcx.YPqzKg.YDcWCyM9BOszebhzfjXx9TeaQlY")

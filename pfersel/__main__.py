import discord
import logging

from pfersel import config
from os import getenv

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(config.LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(console_handler)

BOT_TOKEN = open(getenv("CREDENTIALS_DIRECTORY", default="/dev/null") + "discord-token", "r").readline().strip()


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.streaming, name="Blender", url="https://www.twitch.tv/manasoup_dev"
        )
    )


bot.load_extension("pfersel.welcome")
bot.load_extension("pfersel.bump")
bot.load_extension("pfersel.tags")
bot.load_extension("pfersel.quotes")


bot.run(BOT_TOKEN) 

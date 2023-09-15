import re
import discord
from discord.ext import commands
import datetime


class Welcome(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if "herzlich willkommen <" in str.lower(message.content):
            await message.channel.send(
                "Herzlich Willkommen! \n"
                "Sieh dich in Ruhe um, gib dir in <id:customize> deine Interessen und Fachgebiete.\n"
                "Fülle <#748189945943818272> mit deinen Ideen und aktuellen Projekten. "
                "Erzähle gerne ausführlich über dich in der <#742276310134685718>. "
                "Eigenwerbung ist erlaubt, vermeidet nur bitte Spam. "
                "Füge gerne Links zu Twitch und Sozialen Netzwerken an. "
                "Bei allen Fragen stehen die Admins und Moderatoren jederzeit zu Verfügung."
            )
        if "betatest" in str.lower(message.content).replace(" ", ""):
            await message.channel.send(
                "Obacht, derzeit gehen scammer umher, die Schadsoftware als angebliche Testversionen bewerben. Bitte öffne Programme und binaries nur von Leuten, denen du vertraust."
            )


def setup(bot):
    bot.add_cog(Welcome(bot))

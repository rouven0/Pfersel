import re
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if "herzlich willkommen <:" in str.lower(message.content):
            await message.channel.send(
                "Herzlich Willkommen! \n"
                "Sieh dich in Ruhe um, gib dir in den <#749718475001430019> deine Interessen und Fachgebiete.\n"
                "Fülle <#748189945943818272> mit deinen Ideen und aktuellen Projekten. "
                "Erzähle gerne ausführlich über dich in der <#742276310134685718>. "
                "Eigenwerbung ist erlaubt, vermeidet nur bitte Spam. "
                "Füge gerne Links zu Twitch und Sozialen Netzwerken an. "
                "Bei allen Fragen stehen die Admins und Moderatoren jederzeit zu Verfügung."
            )
        if "😛" in str.lower(message.content):
            await message.add_reaction(self.bot.get_emoji(788347876601364532))
        if "guten morgen" in str.lower(message.content) and message.author.id == 158573690081116160:
            await message.channel.send("Du siehst furchtbar aus")
        if re.match("^\\[[\\w ]+]", str.lower(message.content)) and message.channel.id == 748189945943818272:
            name = message.content[1 : message.content.find("]")]
            thread = await message.channel.create_thread(name=f"Feedback zu {name}", message=message)
            await thread.send(
                f"Servus {message.author.name} <:GS:742287169787396126> "
                "Vielen Dank, dass du mit uns dein Projekt geteilt hast. "
                "Dieser Thread ist für feedback und Gespräche über dein Projekt gedacht. Viel Spaß!"
            )


def setup(bot):
    bot.add_cog(Welcome(bot))

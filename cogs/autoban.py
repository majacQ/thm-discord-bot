import datetime
import time

from discord.ext import commands

import libs.config as config
from libs.embedmaker import officialEmbed
from libs.command_manager import check

############
# COG Body #
############

# defaultAvatar = [
#     "https://cdn.discordapp.com/embed/avatars/5.png",
#     "https://cdn.discordapp.com/embed/avatars/4.png",
#     "https://cdn.discordapp.com/embed/avatars/3.png",
#     "https://cdn.discordapp.com/embed/avatars/2.png",
#     "https://cdn.discordapp.com/embed/avatars/1.png",
#     "https://cdn.discordapp.com/embed/avatars/0.png"
# ]

isOn = False
# checkPfp = True
checkAge = True

def isTooYoung(created_at):
    now = datetime.date.today()
    diff = now - created_at

    return diff.days < 7


class Autoban(commands.Cog, name="AutoBan Commands"):
    def __init__(self, bot):
        self.bot = bot

        @check(roles=["admin", "modlead"], dm_flag=False)
        @bot.command(description="Toggles the autoban feature.", hidden=True)
        async def autoban(ctx):
            global isOn
            isOn = not isOn

            # Sends.
            await ctx.channel.send("AutoBan is " + str(isOn))

        @check(roles=["admin", "modlead"], dm_flag=False)
        @bot.command(description="Gives status on the AutoBan.")
        async def ab_status(ctx):
            # Sends.
            await ctx.channel.send("AutoBan status: " + str(isOn) + "\nAccount age status: " + str(checkAge))

        @bot.event
        async def on_member_join(member):
            if isOn:
                if checkAge and isTooYoung(member.created_at.date()):
                    member.ban()
                elif not checkAge:
                    member.ban()

def setup(bot):
    bot.add_cog(Autoban(bot))

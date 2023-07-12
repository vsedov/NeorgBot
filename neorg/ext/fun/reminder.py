from discord import Embed
from discord.ext import commands

from datetime import datetime
import asyncio

from neorg import constants as c


class Reminder(commands.Cog):
    """Keep reminders."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.hybrid_command()
    async def reminder(self, ctx, user_time, *, message='No Text'):
        """
        Neorg: Reminder (timer)
        Example :
            n.reminder 00:01:00 buy milk -> alerts the message after 1min
            n.rem 00:00:59 wake up --report -> DM user with the message
        """
        msg = message.replace("--report", "").replace("--dm", "")

        try:
            user_time = datetime.strptime(user_time or '00:00:10', '%H:%M:%S')
        except:
            await ctx.send(
                embed=Embed(
                    description="Data format error! use HH:MM:SS format.", color=c.NORG_BLUE
                )
            )
            return

        h_now, m_now, s_now = user_time.hour, user_time.minute, user_time.second
        seconds = (h_now * 3600) + (m_now * 60) + s_now

        content  = f"***Time left***: {seconds}s\n"
        content += f"***Reminder***: {msg}\n"
        content += f"***Set by :*** {ctx.author.mention}"

        embed = Embed(
            title=f':alarm_clock:__Reminder Set for {seconds}s from now :alarm_clock:__',
            description=content,
            color=c.NORG_BLUE
        )
        await ctx.send(embed=embed)

        await asyncio.sleep(seconds)


        done_em = Embed(
            title=':exclamation::alarm_clock:__Reminder Alert__:alarm_clock::exclamation:',
            description=f"***User:***{ctx.author.mention}\n***Reminder:*** {msg}",
            colour=c.NORG_BLUE,
        )
        if "--dm" in message:
            # await ctx.author.send(f"***Your reminder time is up!\nReminder: ***{msg}")
            await ctx.author.send(embed=done_em)
        elif "--report" in message:
            await ctx.send(f"{ctx.message.author.mention}", embed=done_em)
        else:
            # embed2 = done_em
            await ctx.send(embed=done_em)



async def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    await bot.add_cog(Reminder(bot))


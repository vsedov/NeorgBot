from discord import Embed
from discord.ext import commands
from datetime import datetime
import asyncio


class Reminder(commands.Cog):
    """Keep reminders."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(aliases=["remainder", "rem"])
    async def reminder(self, ctx, user_time='00:00:10', *message):
        """
        Neorg: Reminder (timer)
        Example :
            n.reminder 00:01:00 buy milk -> alerts the message after 1min
            n.rem 00:00:59 wake up --report -> DM user with the message
        """
        msg = ' '.join(message).replace("--report", "") if message else 'No Text'

        try:
            user_time = datetime.strptime(user_time, '%H:%M:%S')
        except:
            await ctx.send("Data format error! use HH:MM:SS format.")
            return

        h_now, m_now, s_now = user_time.hour, user_time.minute, user_time.second
        seconds = (h_now * 3600) + (m_now * 60) + s_now

        content  = f"***Time left***: {seconds}s\n"
        content += f"***Reminder***: {msg}\n"
        content += f"***Set by :*** {ctx.author.mention}"

        embed = Embed(
            title=f':alarm_clock:__Reminder Set for {seconds}s from now :alarm_clock:__',
            description=content,
            color=0x4878BE
        )
        await ctx.send(embed=embed)

        await asyncio.sleep(seconds)

        embed2 = Embed(
            title=f':exclamation::alarm_clock:__Reminder Alert__:alarm_clock::exclamation:',
            description=f"***User:***{ctx.author.mention}\n***Reminder:*** {msg}",
            colour=0x4878BE
        )
        await ctx.send(embed=embed2)

        if "--report" in message:
            await ctx.author.send(f"***Your reminder time is up!\nReminder: ***{msg}")


def setup(bot: commands.Bot) -> None:
    """Add cog to bot."""
    bot.add_cog(Reminder(bot))


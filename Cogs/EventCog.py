import discord
from discord.ext import commands
from datetime import datetime, timezone
from pytz import timezone, utc
# from tzlocal import get_localzone


class Event(commands.Cog):
    """
    特殊なイベントでの処理です
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lastchecktime = (datetime.now(utc))
        self.room = self.bot.get_channel(self.bot.config['wkwm']['room_id'])
        if not(self.room):
            print("getchannelerror")

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        br = set(before.roles)
        ar = set(after.roles)
        dif = len(br) - len(ar)
        if dif != 0:
            conf = list((br-ar) if len(br) > len(ar) else (ar-br))
            # print(f"__________{self.lastchecktime}____________")
            async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_role_update, oldest_first=False):
                if entry.created_at > self.lastchecktime.replace(tzinfo=None):
                    if isinstance(entry.target, discord.Member):
                        if dif > 0:
                            conf = list(br-ar)
                            await self.room.send(f'{entry.user.mention} は {entry.target.mention} から **{conf[0].name}** のロールを抜きました')

                        elif dif < 0:
                            conf = list(ar - br)
                            await self.room.send(f'{entry.user.mention} が {entry.target.mention} に **{conf[0].name}** のロールを与え給いました')

        self.lastchecktime = (datetime.now(utc))


def setup(bot):
    return bot.add_cog(Event(bot))

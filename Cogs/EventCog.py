from discord import Embed, Member, AuditLogAction, User, Message
from discord.ext import commands
from datetime import datetime
from pytz import utc
from Cogs.app.OptionalSetting import Option
from web import table


class Event(commands.Cog):
    """
    特殊なイベントでの処理です
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.opt = Option()
        self.db_ms = table.MsfRtb()
        self.lastchecktime = (datetime.now(utc))
        self.room_id = int(self.bot.config['wkwm']['room_id'])
        self.role_nozoki_id = int(self.bot.config['wkwm']['nozoki_role_id'])
        self.welcome_room_id = int(self.bot.config['wkwm']['welcome_room_id'])
        self.welcome_message = str(self.bot.config['wkwm']['welcome_message'])
        self.leave_notice_room_id = int(
            self.bot.config['wkwm']['leave_notice_room_id'])

    @ commands.Cog.listener()
    async def on_member_join(self, member: Member):
        ms = Message
        if member.bot:
            return
        role_member = member.guild.get_role((self.role_nozoki_id))
        await member.add_roles(role_member)
        welcome_room = self.bot.get_channel(self.welcome_room_id)
        ms = await welcome_room.send(embed=await self.opt.default_embed(description=f"ようこそ猿sのばなな農園へ🍌\r{member.mention}さん\r{self.welcome_message}"))
        self.db_ms.add(id=str(ms.id), cid=str(ms.channel.id), seed='w')

    @ commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        if member.bot:
            return
        leave_notice_room = self.bot.get_channel(self.leave_notice_room_id)
        await leave_notice_room.send(embed=await self.opt.default_embed(description=f" **{member.name}** が脱退しました \rUserID: {member.mention}"))

    @ commands.Cog.listener()
    async def on_member_update(self, before, after):
        self.room = self.bot.get_channel(self.room_id)
        br = set(before.roles)
        ar = set(after.roles)
        dif = len(br) - len(ar)
        if dif != 0:
            conf = list((br - ar) if len(br) > len(ar) else (ar - br))
            # print(f"__________{self.lastchecktime}____________")
            async for entry in after.guild.audit_logs(action=AuditLogAction.member_role_update, oldest_first=False):
                if entry.created_at > self.lastchecktime.replace(tzinfo=None):
                    if isinstance(
                            entry.target,
                            Member) | isinstance(
                            entry.target,
                            User):
                        if dif > 0:
                            conf = list(br - ar)
                            await self.room.send(f'{entry.user.mention} は {after.mention} から **{conf[0].name}** のロールを抜きました')
                        elif dif < 0:
                            conf = list(ar - br)
                            await self.room.send(f'{entry.user.mention} が {after.mention} に **{conf[0].name}** のロールを与え給いました')
        self.lastchecktime = (datetime.now(utc))


def setup(bot):
    return bot.add_cog(Event(bot))

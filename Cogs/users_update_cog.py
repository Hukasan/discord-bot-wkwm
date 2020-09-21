from discord import Embed, Member, AuditLogAction, User, Message
from discord.ext.commands import Cog, Bot
from datetime import datetime
from pytz import utc
from Cogs.app import table, make_embed as me


class UserEvent(Cog):
    """
    ユーザ情報の改定を検知したときの処理
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.db_ms = table.MsfRtb()
        self.lastchecktime = (datetime.now(utc))
        self.role_nozoki_id = int(self.bot.config['wkwm']['nozoki_role_id'])
        self.room_id = int(self.bot.config['wkwm']['room_id'])
        self.leave_notice_room_id = int(
            self.bot.config['wkwm']['leave_notice_room_id'])

    @ Cog.listener()
    async def on_member_remove(self, member: Member):
        if member.bot:
            return
        leave_notice_room = self.bot.get_channel(self.leave_notice_room_id)
        opt = me.MyEmbed().setTarget(target=leave_notice_room)
        await opt.default_embed(header_icon=member.avatar_url, header=f"{member.name}", description=["が脱退しました。", f"UserID: {member.mention}"])
        await opt.sendEmbed()

    @ Cog.listener()
    async def on_member_update(self, before, after):
        br = set(before.roles)
        ar = set(after.roles)
        dif = len(br) - len(ar)
        if dif != 0:
            room = self.bot.get_channel(self.room_id)
            opt = me.MyEmbed().setTarget(room)
            conf = list((br - ar) if len(br) > len(ar) else (ar - br))
            async for entry in after.guild.audit_logs(action=AuditLogAction.member_role_update, oldest_first=False):
                if entry.created_at > self.lastchecktime.replace(tzinfo=None):
                    if isinstance(
                            entry.target,
                            Member) | isinstance(
                            entry.target,
                            User):
                        nozoki = room.guild.get_role(self.role_nozoki_id)
                        if dif > 0:
                            conf = list(br - ar)
                            if conf[0] != nozoki:
                                await opt.default_embed(description=[f"管理者{entry.user.mention} があなたから", f"<**{conf[0].name}**>のロールを抜きましたどんまい"])
                        elif dif < 0:
                            conf = list(ar - br)
                            if conf[0] != nozoki:
                                await opt.default_embed(description=[f"管理者{entry.user.mention} があなたに", f"<**{conf[0].name}**>のロールを与えました🎉"])
                        if opt.config:
                            await opt.sendEmbed(nomal=f"{after.mention}")
        self.lastchecktime = (datetime.now(utc))


def setup(bot: Bot):
    return bot.add_cog(UserEvent(bot))

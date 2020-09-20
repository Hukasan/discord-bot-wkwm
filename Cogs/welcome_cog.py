from discord import Embed, Member, AuditLogAction, User, Message
from discord.ext.commands import Cog, Bot
from Cogs.app import table, make_embed as me, extentions


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_nozoki_id = int(self.bot.config['wkwm']['nozoki_role_id'])
        self.welcome_room_id = int(self.bot.config['wkwm']['welcome_room_id'])
        self.welcome_message = (self.bot.config['wkwm']['welcome_message'])
        self.header = "*このチャットはあなたがリアクションをつけると消去されます*"
        self.db_ms = table.MsfRtb()

    @ Cog.listener()
    async def on_member_join(self, member: Member):
        if member.bot:
            return
        nozoki_role = member.guild.get_role((self.role_nozoki_id))
        welcome_room = self.bot.get_channel(self.welcome_room_id)

        desc = [f"{member.name}さん", "ようこそ猿sのばなな農園へ🍌🐵", ]
        desc.extend(self.welcome_message)
        if nozoki_role:
            if welcome_room:
                await member.add_roles(nozoki_role)
                opt = me.MyEmbed().setTarget(target=welcome_room)
                await opt.default_embed(description=desc, header=self.header)
                ms = await opt.sendEmbed(greeting=member.mention)
                self.db_ms.add(id=str(ms.id), cid=str(ms.channel.id), seed='w')
            else:
                raise extentions.GetDatafromDiscordError(
                    f"Welcomeチャンネルオブジェクトの取得に失敗しました。\r登録しているIDを確認してください({self.welcome_room_id})")
        else:
            raise extentions.GetDatafromDiscordError(
                f"Nozokiロールオブジェクトの取得に失敗しました。\r登録しているIDを確認してください({self.role_nozoki_id})")


def setup(bot):
    return bot.add_cog(Welcome(bot))

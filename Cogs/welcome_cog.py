from discord import Embed, Member, AuditLogAction, User, Message
from discord.ext.commands import Cog, Bot
from Cogs.app import table, make_embed as me, extentions


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_room_id = int(self.bot.config['wkwm']['welcome_room_id'])
        self.header = ""
        self.db_ms = table.MsfRtb()

    @ Cog.listener()
    async def on_member_join(self, member: Member):
        if member.bot:
            return
        welcome_room = self.bot.get_channel(self.welcome_room_id)

        desc = "はじめまして、わけわかめBotです"
        if welcome_room:
            opt = me.MyEmbed().setTarget(target=welcome_room)
            opt.setBot(bot=self.bot)
            await opt.default_embed(header=desc, header_icon=True, description="ようこそ猿sのばなな農園へ🍌🐵\r🙇公開チャンネルに入る前にお読みだせい")
            opt.add(
                name="> 規約事項",
                value="・ 宣伝は必ず許可を取ってください\r・ このサーバの会話の転載はお控えください")
            opt.add(
                name="> 参加方法",
                value="規約事項を読み理解したらこのチャットの🗑を押してください"
            )
            await opt.sendEmbed(greeting=(member.mention + self.header), seed='w', bottums='🗑')
        else:
            raise extentions.GetDatafromDiscordError(
                f"Welcomeチャンネルオブジェクトの取得に失敗しました。\r登録しているIDを確認してください({self.welcome_room_id})")


def setup(bot):
    return bot.add_cog(Welcome(bot))

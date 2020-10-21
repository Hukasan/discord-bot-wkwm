from discord import Embed, Member, AuditLogAction, User, Message
from discord.ext.commands import Cog, Bot
from Cogs.app import table, make_embed as me, extentions


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_room_id = int(self.bot.config["wkwm"]["welcome_room_id"])
        self.header = ""
        self.db_ms = table.MsfRtb()

    @Cog.listener()
    async def on_member_join(self, member: Member):
        if member.bot:
            return
        welcome_room = self.bot.get_channel(self.welcome_room_id)

        desc = "はじめまして、わけわかめBotです"
        if welcome_room:
            opt = me.MyEmbed().setTarget(target=welcome_room, bot=self.bot)
            await opt.default_embed(
                header=desc,
                header_icon=True,
                description="ようこそ猿sのばなな農園へ🍌🐵\r🙇公開チャンネルに入る前にお読みださい",
                footer="ウェルカムメッセージ",
            )
            opt.add(
                name="> おやくそく",
                value="・ 宣伝は許可を取ってください\r・ 会話の転載はやめてください\r・ 誹謗中傷はやめてください\rお約束が守れない場合、勝手に追放します",
            )
            opt.add(name="> 🗑押してください", value="読み理解したらこのチャットの🗑を押してください")
            await opt.sendEmbed(greeting=(member.mention + self.header), footer_arg="w-1")
        else:
            raise extentions.GetDatafromDiscordError(
                f"Welcomeチャンネルオブジェクトの取得に失敗しました。\r登録しているIDを確認してください({self.welcome_room_id})"
            )


def setup(bot):
    return bot.add_cog(Welcome(bot))

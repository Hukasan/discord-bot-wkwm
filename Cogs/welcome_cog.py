from discord import Embed, Member, AuditLogAction, User, Message
from discord.ext.commands import Cog, Bot
from Cogs.app import table, make_embed as me, extentions


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        if member.bot:
            return
        welcome_room = self.bot.get_channel(
            int(self.bot.config[str(member.guild.id)]["channel_ids"]["welcome"])
        )
        if welcome_room:
            opt = me.MyEmbed().setTarget(target=welcome_room, bot=self.bot)
            await opt.default_embed(
                header="はじめまして、わけわかめBotです",
                header_icon=True,
                description="ようこそ猿sのばなな農園へ!🍌🐵\r🙇公開チャンネルに入る前に、おやくそくです",
                footer="ウェルカムメッセージ",
            )
            opt.add(
                name="> おやくそく",
                value="・ 無許可宣伝(url転載含む)\r・ 他人を傷付ける言葉\rはやめれください\r気持ち良いサーバづくりにご協力ください\r\r了解されたら、↓🍌を押してください",
            )
            await opt.sendEmbed(
                greeting=(member.mention), footer_arg="w-1", dust=False, bottums="🍌"
            )
        else:
            raise extentions.GetDatafromDiscordError(
                f"Welcomeチャンネルオブジェクトの取得に失敗しました。\r登録しているIDを確認してください({self.welcome_room_id})"
            )


def setup(bot):
    return bot.add_cog(Welcome(bot))

from discord import (
    Embed,
    Member,
    Reaction,
    RawReactionActionEvent,
    TextChannel,
    Message,
    Emoji,
)
from discord.ext.commands import Cog, Bot
from discord.abc import GuildChannel, PrivateChannel
from Cogs.app import table, extentions, make_embed as me

# from datetime import datetime
# from pytz import utc
# from Cogs.app.MakeEmbed import MakeEmbed


class ReactionEvent(Cog):
    """
    リアクションに対しての処理(ページ遷移を除く)
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.db_ms = table.MsfRtb()
        self.funcs = {"w1": self.ear_welcome1, "w2": self.ear_welcome2}
        self.role_nozoki_id = int(self.bot.config["wkwm"]["nozoki_role_id"])

    async def embed_react_action(self, usr_id: int, ms: Message, react: Emoji) -> bool:
        result = self.db_ms.tbselect(id=str(ms.id))
        if result:
            func = self.funcs.get(result[0].seed)
            if func:
                return await func(usr_id, ms, react)
            else:
                pass
        else:
            usr = self.bot.get_user(usr_id)
            if (str(react) == "🗑") & (usr in ms.mentions):
                await ms.delete()

    async def ear_welcome2(self, usr_id: int, ms: Message, react: Emoji):
        usr = self.bot.get_user(usr_id)
        if usr in ms.mentions:
            self.db_ms.tbdelete(id=str(ms.id))
            await ms.delete()

    async def ear_welcome1(self, usr_id: int, ms: Message, react: Emoji):
        self.db_ms.tbdelete(id=str(ms.id))
        nozoki_role = ms.guild.get_role((self.role_nozoki_id))
        member = ms.guild.get_member(usr_id)
        usr = self.bot.get_user(usr_id)
        print("きてます")
        embed = me.MyEmbed().setTarget(target=ms.channel, bot=self.bot)
        if bool(nozoki_role) & bool(member):
            if usr in ms.mentions:
                await member.add_roles(nozoki_role)
                await ms.delete()
                await embed.default_embed(
                    header_icon=ms.guild.icon_url,
                    header="公開チャンネルの説明です",
                    footer="ウェルカムメッセージ",
                    description="有難うございますd(ﾟДﾟ )\r公開チャンネルが見れるようになりました。",
                )
                embed.add(
                    name="> 各チャンネルについて",
                    value="各受付内容のチャンネルに要件があればお願いします。\r__チャンネルの詳細、試験内容などは各ピン留めに貼り付けてます__\r\r以上です🍌\rよろしければ☑を押してください",
                )
                await embed.sendEmbed(
                    bottums=["☑"], seed="w2", greeting=f"{usr.mention}", dust=False
                )
        else:
            raise extentions.GetDatafromDiscordError(
                f"Nozokiロールオブジェクトの取得に失敗しました。\r登録しているIDを確認してください({self.role_nozoki_id})"
            )

    @Cog.listener()
    async def on_raw_reaction_add(self, rrae: RawReactionActionEvent):
        usr = self.bot.get_user(rrae.user_id)
        channel = TextChannel
        channel = self.bot.get_channel(rrae.channel_id)
        emoji = rrae.emoji
        if bool(channel) & bool(emoji) & bool(usr):
            if usr.bot:
                return
            message = Message
            message = await channel.fetch_message(id=rrae.message_id)
            if message.embeds:
                await self.embed_react_action(rrae.user_id, message, emoji)
            else:
                pass


def setup(bot):
    return bot.add_cog(ReactionEvent(bot))

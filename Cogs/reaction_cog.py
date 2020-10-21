from discord import (
    Embed,
    Member,
    Reaction,
    RawReactionActionEvent,
    TextChannel,
    Message,
    Emoji,
)
from discord.ext.commands import Cog, Bot, Context
from discord.abc import GuildChannel, PrivateChannel
from Cogs.app import table, extentions, make_embed as me

# from datetime import datetime
# from pytz import utc
# from Cogs.app.MakeEmbed import MakeEmbed


class ReactionEvent(Cog):
    """
    リアクションに対しての処理
    ear:embed_reaction_actionえ？それじゃeraじゃんて。そんなこたぁきにすんなって
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.funcs = {
            "w-1": self.ear_welcome1,
            "w-2": self.ear_welcome2,
            "e-c-h": self.ear_ech,
        }
        self.role_nozoki_id = int(self.bot.config["wkwm"]["nozoki_role_id"])

    async def embed_react_action(self, usr_id: int, ms: Message, react: Emoji, arg: list) -> bool:
        func = None
        # result = self.db_ms.tbselect(id=str(ms.id))
        # if result:
        # func = self.funcs.get(result[0].seed)
        # print(arg)
        if arg:
            func = self.funcs.get(arg[0])
        if func:
            ctx = await self.bot.get_context(ms)
            return await func(usr_id, ctx, react, arg)
        else:
            usr = self.bot.get_user(usr_id)
            if (str(react) == "🗑") & (usr in ms.mentions):
                await ms.delete()

    async def ear_ech(self, usr_id: int, ctx: Context, react: Emoji, arg: list):
        if str(react) == "🙆":
            ctx.prefix = arg[1][0]
            ctx.author = ctx.message.mentions[0]
            await ctx.send_help(arg[1][1:])
            await ctx.message.delete()
        elif str(react) == "🗑":
            await ctx.message.delete()

    async def ear_welcome1(self, usr_id: int, ctx: Context, react: Emoji, arg: list):
        nozoki_role = ctx.guild.get_role((self.role_nozoki_id))
        member = ctx.guild.get_member(usr_id)
        usr = self.bot.get_user(usr_id)
        embed = me.MyEmbed().setTarget(target=ctx.channel, bot=self.bot)
        if bool(nozoki_role) & bool(member):
            if str(react) == "🗑":
                if usr in ctx.message.mentions:
                    await member.add_roles(nozoki_role)
                    await ctx.message.delete()
                    await embed.default_embed(
                        header_icon=ctx.guild.icon_url,
                        header="公開チャンネルの説明です",
                        footer="ウェルカムメッセージ",
                        description="有難うございますd(ﾟДﾟ )\r公開チャンネルが見れるようになりました。",
                    )
                    embed.add(
                        name="> 各チャンネルについて",
                        value="各受付内容のチャンネルに要件があればお願いします。\r__チャンネルの詳細、試験内容などは各ピン留めに貼り付けてます__\r\r以上です🍌\rよろしければ☑を押してください",
                    )
                    await embed.sendEmbed(
                        bottums=["☑"],
                        footer_arg="w-2",
                        greeting=f"{usr.mention}",
                        dust=False,
                    )
        else:
            raise extentions.GetDatafromDiscordError(
                f"Nozokiロールオブジェクトの取得に失敗しました。\r登録しているIDを確認してください({self.role_nozoki_id})"
            )

    async def ear_welcome2(self, usr_id: int, ctx: Context, react: Emoji, arg: list):
        usr = self.bot.get_user(usr_id)
        if usr in ctx.message.mentions:
            if str(react) == "☑":
                await ctx.message.delete()

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
                # await self.embed_react_action(rrae.user_id, message, emoji)
                for embed in message.embeds:
                    await self.embed_react_action(
                        usr_id=rrae.user_id,
                        ms=message,
                        react=emoji,
                        arg=me.scan_footer(embed=embed),
                    )
            else:
                pass


def setup(bot):
    return bot.add_cog(ReactionEvent(bot))

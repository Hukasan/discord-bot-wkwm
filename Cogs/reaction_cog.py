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


class ReactionEvent(Cog, name="ReactionEvent"):
    """
    リアクションに対しての処理
    次に行う処理をbot.configにかんすごと保存し、ここで呼び出す
    識別はembedのフッターを利用している(make_embed.scan_footer)
    era:embed_reaction_action
    """

    qualified_name = "hide"

    def __init__(self, bot: Bot):
        self.bot = bot

    async def do_era(self, usr_id: int, ms: Message, react: Emoji, arg: list) -> bool:
        usr = self.bot.get_user(usr_id)
        func = None
        if (str(react) == "🗑") & (usr in ms.mentions):
            await ms.delete()
            return
        elif str(react) == "🔽":
            buttoms_sub = self.bot.config[str(ms.guild.id)]["bottoms_sub"].get(ms.id)
            if buttoms_sub:
                await ms.clear_reactions()
                for b in buttoms_sub:
                    await ms.add_reaction(b)
                await ms.add_reaction("🔼")
            else:
                await me.MyEmbed().setTarget(ms.channel, bot=self.bot).default_embed(
                    mention=ms.content,
                    header="🙏ごめんなさい",
                    title="ボタンの読み込みにしっぺいしました",
                    description="おそらくボットに再起動がかかり初期化された、もしくは内部エラーです",
                    dust=True,
                ).sendEmbed()
                await ms.clear_reaction("🔽")
            return
        elif str(react) == "🔼":
            await ms.clear_reactions()
            await ms.add_reaction("🔽")
            await ms.add_reaction("🗑")
            buttoms = self.bot.config[str(ms.guild.id)]["bottoms"].get(ms.id)
            if buttoms:
                for b in buttoms:
                    await ms.add_reaction(b)
            return
        elif arg:
            func = self.bot.config["funcs"].get(arg[0])
        if func:
            ctx = await self.bot.get_context(ms)
            return await func(self.bot, usr_id, ctx, react, arg)

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
                for embed in message.embeds:
                    await self.do_era(
                        usr_id=rrae.user_id,
                        ms=message,
                        react=emoji,
                        arg=me.scan_footer(embed=embed),
                    )
            else:
                pass


def setup(bot):
    return bot.add_cog(ReactionEvent(bot))

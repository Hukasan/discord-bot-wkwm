from discord import Embed, Member, Reaction, RawReactionActionEvent, TextChannel, Message, Emoji
from discord.ext.commands import Cog, Bot
from discord.abc import GuildChannel, PrivateChannel
from Cogs.app import table
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
        self.funcs = {"w": self.ear_welcome}

    async def embed_react_action(self, usr_id: int, ms: Message, react: Emoji) -> bool:
        result = self.db_ms.tbselect(id=str(ms.id))
        if result:
            func = self.funcs.get(result[0].seed)
            if func:
                return await func(usr_id, ms, react)
            else:
                pass

    async def ear_welcome(self, usr_id: int, ms: Message, react: Emoji):
        self.db_ms.tbdelete(id=str(ms.id))
        if ms.author.id == usr_id:
            await ms.delete()
            return True
        pass

    @ Cog.listener()
    async def on_raw_reaction_add(self, rrae: RawReactionActionEvent):
        print("リアクション検知")
        usr = self.bot.get_user(rrae.user_id)
        channel = TextChannel
        channel = self.bot.get_channel(rrae.channel_id)
        emoji = self.bot.get_emoji(rrae.emoji.id)
        if bool(channel) & bool(emoji) & bool(usr):
            if not(usr.bot):
                print("正規なリアクション")
                message = Message
                message = await channel.fetch_message(rrae.message_id)
                if message.embeds:
                    print("embedを検知")
                    await self.action_react(rrae.user_id, message, emoji)
                else:
                    pass


def setup(bot):
    return bot.add_cog(ReactionEvent(bot))

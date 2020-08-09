from discord import Embed, Member, Reaction, RawReactionActionEvent, TextChannel, Message, Emoji
from discord.ext import commands
from discord.abc import GuildChannel, PrivateChannel
# from datetime import datetime
# from pytz import utc
from Cogs.OptionalSetting import Option
from web import table


class ReactionEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db_ms = table.MsfRtb()
        self.funcs = {"w": self.ar_welcome}

    async def action_react(self, ms: Message, react: Emoji) -> bool:
        # try:
        result = self.db_ms.table
        result = self.db_ms.tbselect(id=str(ms.id))
        if result:
            func = self.funcs.get(result[0].seed)
            if func:
                return await func(ms, react)
            else:
                return False
        # except BaseException:
        # return False

    async def ar_welcome(self, ms: Message, react: Emoji) -> bool:
        await ms.delete()
        self.db_ms.tbdelete(id=str(ms.id))
        return True

    @ commands.Cog.listener()
    async def on_raw_reaction_add(self, rrae: RawReactionActionEvent):
        usr = self.bot.get_user(rrae.user_id)
        channel = TextChannel
        channel = self.bot.get_channel(rrae.channel_id)
        if isinstance(channel, TextChannel):
            if (usr):
                if usr.bot:
                    return
                message = Message
                message = await channel.fetch_message(rrae.message_id)
                await self.action_react(message, rrae.emoji)


def setup(bot):
    return bot.add_cog(ReactionEvent(bot))

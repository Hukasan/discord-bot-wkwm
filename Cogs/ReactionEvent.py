from discord import Embed, Member, Reaction, RawReactionActionEvent, TextChannel, Message, Emoji
from discord.ext.commands import Cog, Bot
from discord.abc import GuildChannel, PrivateChannel
# from datetime import datetime
# from pytz import utc
from Cogs.app.OptionalSetting import Option
from web import table


class ReactionEvent(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.db_ms = table.MsfRtb()
        self.funcs = {"w": self.ar_welcome}

    async def action_react(self, usr_id: int, ms: Message, react: Emoji) -> bool:
        # try:
        result = self.db_ms.table
        result = self.db_ms.tbselect(id=str(ms.id))
        if result:
            func = self.funcs.get(result[0].seed)
            if func:
                return await func(usr_id, ms, react)
            else:
                return False
        # except BaseException:
        # return False

    async def ar_welcome(self, usr_id: int, ms: Message, react: Emoji):
        self.db_ms.tbdelete(id=str(ms.id))
        if ms.author.id == usr_id:
            await ms.delete()
            return True
        pass

    @ Cog.listener()
    async def on_raw_reaction_add(self, rrae: RawReactionActionEvent):
        usr = self.bot.get_user(rrae.user_id)
        channel = TextChannel
        channel = self.bot.get_channel(rrae.channel_id)
        print(type(rrae.emoji))
        emoji = self.bot.get_emoji(rrae.emoji.id)
        if bool(channel) & bool(emoji):
            if usr:
                if usr.bot:
                    return
                message = Message
                message = await channel.fetch_message(rrae.message_id)
                await self.action_react(rrae.user_id, message, emoji)


def setup(bot):
    return bot.add_cog(ReactionEvent(bot))

from discord import Embed, Member, Reaction, RawReactionActionEvent, TextChannel, Message
from discord.ext import commands
from discord.abc import GuildChannel, PrivateChannel
from datetime import datetime
from pytz import utc
from Cogs.OptionalSetting import Option


class ReactionEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
                message = channel.fetch_message(rrae.message_id)
                if message.embeds:
                    if (len(message.embeds) == 1):

            else:
                print("pienn")


def setup(bot):
    return bot.add_cog(ReactionEvent(bot))

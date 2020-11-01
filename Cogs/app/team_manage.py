from discord import Message, VoiceChannel
from discord.ext.commands import Cog, Bot, Context, command
import re
from Cogs.app import make_embed as me, extentions

pattern = r".*?@(\d+)"
repatter = re.compile(pattern=pattern)


class TeamIO:
    """
    クラン戦募集あしすと
    """

    def __init__(self, bot: Bot):
        self.teams = {}
        self.bot = bot
        self.ctx = Context
        self.size = 5
        self.now = int()
        self.dembed = me.MyEmbed()
        self.cid = int()

    async def scan_message(self, message: Message, channel_id: int):
        self.ctx = self.dembed.ctx = await self.bot.get_context(message)
        self.cid = channel_id
        result = repatter.match(string=message.content)
        if result:
            self.now = self.size - int(result.group(1))
            self.now = self.now if (self.now >= 0) else 0
            await self.change_chname()
        pass

    async def change_chname(self):
        channel1 = self.bot.get_channel(self.bot.config["wkwm"]["fleet_1_id"])
        if channel1:
            if "," in channel1.name:
                string = channel1.name.split(",")[-2]
            else:
                string = channel1.name
            string = string + f",{self.now}/{self.size}"
            await channel1.edit(name=string)
            print(string)
        else:
            raise extentions.GetDatafromDiscordError("対象VCの取得に失敗しました")

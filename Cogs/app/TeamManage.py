from discord import Message
from discord.ext.commands import Cog, Bot, Context
import re
from Cogs.app.OptionalSetting import Option

# このプログラムはon_massage内で呼び出されることを前提としている

pattern = r'.*?@(\d+)'
repatter = re.compile(pattern=pattern)


class Team():
    def __init__(self, bot: Bot):
        self.teams = {}
        self.bot = bot
        self.ctx = Context
        self.size = int()
        self.opt = Option()
        self.cid = int()

    async def scan_message(self, message: Message, channel_id: int):
        self.ctx = self.opt.ctx = await self.bot.get_context(message)
        self.cid = channel_id if channel_id else self.ctx.channel
        result = repatter.match(string=message.content)
        if result:
            self.size = int(result.group(1))
            await self.create_team(name="Team")
        pass

    async def create_team(self, name: str) -> None:
        if self.size:
            self.teams[name] = {}
            for i in range(self.size):
                self.teams[name][i] = dict(name="", profile="", id=i)
            print(self.teams[name])
            await self.view_team(name)
        pass

    async def view_team(self, name: str) -> None:
        if self.teams[name]:
            content = ''.join([(f"{d[1].get('id')}: {d[1].get('name')}  {d[1].get('profile')}\r")
                               for d in self.teams[name].items()])
            embed = await self.opt.default_embed(
                title=name,
                footer="TeamManager",
                description=content)
            print(embed)
            await self.bot.get_channel(self.cid).send(embed=embed)
        pass

        # print(scan_message("クラン戦 @5"))

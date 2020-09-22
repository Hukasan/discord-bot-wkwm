from discord import Embed, TextChannel
from discord.ext.commands import Cog, Bot, Context
from Cogs.app import table
from os import linesep
from datetime import datetime

# from copy import copy


class MyEmbed:
    def __init__(self, ctx=None):
        self.ctx = ctx
        self.bot = ctx.bot if ctx else None
        self.target = ctx.channel if ctx else None
        self.embed = None
        self.db_ep = table.EmbedPages()
        self.db_ms = table.MsfRtb()
        self.descriptions = list()
        self.line_number = int(0)
        self.config = {}
        self.bot_info = None
        self.greeting = str()
        self.files = list()

    def setTarget(self, target):
        self.target = target
        return self

    def change_description(self, desc):
        if self.config:
            self.config["description"] = desc

    def setCtx(self, ctx):
        self.ctx = ctx
        return self

    def setBot(self, bot):
        self.bot = bot
        return self

    def __cut(self, obj: str):
        point = 50
        if isinstance(obj, str):
            if len(obj) > point:
                ex = f"{obj[:point+1]}\n"
                ex = ex + (self.cut(obj[point + 1 :]))
            else:
                ex = f"{obj}\n"
        else:
            ex = "TextError"
        return ex

    def __export_complist(self, obj):
        ex = list()
        lines = 0
        if isinstance(obj, str):
            obj = obj.splitlines()
        if isinstance(obj, list):
            temp = list()
            for o in obj:
                temp.extend(o.splitlines())
            obj = temp
            for o in obj:
                content = self.__cut(o)
                line = len(content)
                # print(f"{o},{line}")
                while line > 0:
                    if (line + lines) > 10:
                        if ex:
                            ex[-1] = ex[-1] + content[: 15 - lines + 1]
                        else:
                            ex.append(content[: 15 - lines + 1])
                        content = content[15 - lines + 1 :]
                        lines = 0
                        line = line - 15 + lines - 1
                    else:
                        if ex:
                            ex[-1] = ex[-1] + content
                        else:
                            ex.append(content)
                        line = 0
        return ex

    def add(
        self, name: str, value: str, inline=False, greeting=str(), description=str()
    ) -> None:
        if greeting:
            self.greeting = greeting
        if self.config:
            if description:
                self.config["description"] = description
            self.config["fields"].append(
                {"name": name, "value": value, "inline": inline}
            )

    async def sendEmbed(
        self, obj=None, greeting=str(), seed=None, bottums=list(), files=list()
    ):
        if self.config:
            if files:
                self.config["files"] = files
            if greeting:
                self.greeting = greeting
            self.embed = Embed()
            self.embed = Embed.from_dict(self.config)
            obj = obj[0] if isinstance(obj, list) else obj
            if obj:
                pass
            elif self.target:
                obj = self.target
            elif self.ctx:
                obj = self.ctx.channel
            if obj:
                ms = await obj.send(embed=self.embed, content=self.greeting)
                if self.descriptions:
                    self.db_ms.add(id=ms.id, content=self.descriptions, isnow=1)
                    await ms.add_reaction("➡")
                if seed:
                    self.db_ms.add(id=str(ms.id), cid=str(ms.channel.id), seed="w")
                if bottums:
                    for b in bottums:
                        if isinstance(b, str):
                            await ms.add_reaction(b)
            return ms
        else:
            return None

    async def default_embed(
        self,
        title=None,
        description=None,
        thumbnail=False,
        header=None,
        header_icon=None,
        footer=True,
        footer_url=None,
        time=True,
    ):
        config = {"title": title, "color": 0x00FF00, "fields": []}
        time_str = str()
        if description:
            self.descriptions = self.__export_complist(obj=description)
            config["description"] = self.descriptions.pop(0)
        if self.bot:
            self.bot_info = await self.bot.application_info()
            if thumbnail:
                config["thumnail"] = {"url": str(self.bot_info.icon_url)}
        if header:
            if isinstance(header_icon, bool) & bool(self.bot_info):
                config["author"] = {
                    "name": header,
                    "icon_url": str(self.bot_info.icon_url),
                }
            elif header_icon:
                config["author"] = {"name": header, "icon_url": str(header_icon)}
            else:
                config["author"] = {"name": header}
        if time:
            time_str = datetime.now().strftime("%m/%d %H:%M:%S")
            config["footer"] = {"text": time_str}
        if footer:
            if isinstance(footer, bool):
                if bool(self.ctx):
                    string = f"{self.ctx.prefix} {self.ctx.command}"
                    if self.ctx.invoked_subcommand:
                        string += f" {(self.ctx.invoked_subcommand).name}"
                    config["footer"] = {"text": f"{string}　[{time_str}]"}
            elif footer_url:
                config["footer"] = {
                    "text": f"{string}　[{time_str}]",
                    "icon_url": str(footer_url),
                }
            else:
                config["footer"] = {"text": f"{string}　[{time_str}]"}

        self.config = config

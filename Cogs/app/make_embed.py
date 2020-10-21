from discord import Embed, TextChannel, Message
from discord.ext.commands import Cog, Bot, Context
from os import linesep
from datetime import datetime

# from copy import copy


class MyEmbed:
    """
    embed生成
    """

    def __init__(self, ctx=None):
        self.ctx = ctx
        self.bot = ctx.bot if ctx else None
        self.target = ctx.channel if ctx else None
        self.obj = None
        self.title = str()
        self.color = None
        self.thumbnail = False
        self.footer = str()
        self.icon_url = str()
        self.header = None
        self.header_icon_url = str()
        self.fields = list()
        self.embed = None
        self.description = str()
        self.descriptions = list()
        self.line_number = int(0)
        self.bot_info = None
        self.greeting = str()
        self.files = list()
        self.time = False
        self.dust = False
        self.footer_arg = str()
        self.bottums = list()

    def setTarget(self, target, bot=None):
        self.target = target
        if bot:
            self.bot = bot
        return self

    def change_description(self, desc=str(), arg=str(), bottums=list()):
        self.description = desc
        if arg:
            self.footer_arg += arg
        if bottums:
            self.bottums.extend(bottums)

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

    async def default_embed(
        self,
        title=None,
        color=0x00FF00,
        description=None,
        thumbnail=False,
        header=str(),
        header_icon=None,
        footer=str(),
        footer_url=str(),
        time=True,
        greeting=str(),
        arg=str(),
    ):
        self.title = title
        self.color = color
        self.time = time
        self.footer = footer
        self.icon_url = footer_url if footer else str()
        self.header = header
        self.header_icon_url = header_icon if header else str()
        self.thumbnai = thumbnail
        self.greeting = greeting
        self.footer_arg = arg
        self.description = (self.__export_complist(obj=description)).pop() if description else None
        return self

    def add(self, name: str, value: str, inline=False, greeting=str(), description=str()) -> None:
        if greeting:
            self.greeting = greeting
        self.description = description if description else self.description
        self.fields.append({"name": name, "value": value, "inline": inline})

    async def sendEmbed(
        self,
        obj=None,
        greeting=str(),
        footer_arg=str(),
        bottums=list(),
        files=list(),
        dust=True,
    ) -> Message:
        if bool(self.footer_arg) or bool(footer_arg):
            self.footer_arg = f"@{self.footer_arg}{footer_arg}"
        self.greeting = greeting if bool(greeting) else self.greeting
        self.dust = dust if dust else self.dust
        if bottums:
            self.bottums.extend(bottums)
        config = dict()
        if (bool(self.footer)) or (bool(self.footer_arg)):
            time_str = str()
            if self.time:
                time_str = (datetime.now()).strftime("%m/%d %H:%M:%S")
            config["footer"] = {"text": f"{time_str}#{self.footer}{self.footer_arg}"}
            config["footer"]["icon_url"] = self.icon_url if self.icon_url else None

        if bool(self.bot) & bool(self.thumbnail):
            self.bot_info = await self.bot.application_info()
            config["thumbnail"] = {"url": str(self.bot_info.icon_url)}

        if self.header:
            config["author"] = {"name": self.header}
            if isinstance(self.header_icon_url, str):
                config["author"]["icon_url"] = str(self.header_icon_url)
            elif self.bot:
                bot_info = await self.bot.application_info()
                config["author"]["icon_url"] = str(bot_info.icon_url) if bot_info else None

        config["description"] = self.description if self.description else None
        config["files"] = files if files else None
        config["fields"] = self.fields

        self.embed = Embed()
        self.embed = Embed.from_dict(config)

        obj = obj[0] if isinstance(obj, list) else obj
        if (not (self.obj)) & bool(self.target):
            obj = self.target
        elif self.ctx:
            obj = self.ctx.channel
        if obj:
            ms = await obj.send(embed=self.embed, content=self.greeting)
            if self.dust:
                await ms.add_reaction("🗑")
            if self.bottums:
                for b in self.bottums:
                    if isinstance(b, str):
                        await ms.add_reaction(b)
        return ms


def scan_footer(embed: Embed) -> list:
    footer = str()
    arg = list()
    if embed:
        footer = (embed.to_dict()).get("footer")
        if footer:
            text = footer.get("text")
            if "@" in text:
                arg = text.split("@")[1]
                return arg.split(" ", 1)
    return list()

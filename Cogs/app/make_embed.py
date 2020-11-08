from discord import Embed, TextChannel, Message
from discord.ext.commands import Cog, Bot, Context
from os import linesep
from datetime import datetime
from Cogs.app.mymethods import dainyu
from copy import copy
from emoji import UNICODE_EMOJI

"""
    embed作成、送信
"""


class MyEmbed:
    """
    embed作成、送信
    """

    def __init__(self, ctx=None):

        self.ctx = ctx
        self.bot = ctx.bot if ctx else None
        self.target = ctx.channel if ctx else None
        self.obj = None
        self.mention = str()
        self.mention_author = bool()
        self.title = str()  # タイトル
        self.color = 0x00FF00  # 色
        self.thumbnail = False  # 大きめのアイコン画像を表示させるかどうか
        self.footer = str()  # フッター文
        self.icon_url = str()  # フッター画像url
        self.header = None  # ヘッダー文
        self.header_icon_url = str()  # ヘッダー画像url
        self.fields = list()
        self.embed = None
        self.description = str()
        self.descriptions = list()
        self.line_number = int(0)
        self.greeting = str()
        self.files = list()
        self.time = False
        self.dust = True
        self.footer_arg = str()
        self.bottums = list()
        self.bottums_sub = list()
        self.bottum_args = None

    def setTarget(self, target, bot=None):
        self.target = target
        if bot:
            self.bot = bot
        return self

    def change(
        self,
        color=None,
        title=str(),
        desc=str(),
        arg=str(),
        bottums=list(),
        bottums_sub=list(),
        bottum_args=None,
        greeting=str(),
        header=str(),
        header_icon_url=str(),
        thumbnail=bool(),
        footer=str(),
    ):
        """
        設定書き換え

        Args:
            title ([type], optional): [description]. Defaults to str().
            desc ([type], optional): [description]. Defaults to str().
            arg ([type], optional): [description]. Defaults to str().
            bottums ([type], optional): [description]. Defaults to list().
            greeting ([type], optional): [description]. Defaults to str().
            header ([type], optional): [description]. Defaults to str().
            header_icon_url ([type], optional): [description]. Defaults to str().
            thumbnail ([type], optional): [description]. Defaults to bool().
            footer ([type], optional): [description]. Defaults to str().
        """
        self.color = dainyu(color, self.color)
        self.thumbnail = dainyu(thumbnail, self.thumbnail)
        self.header = dainyu(header, self.header)
        self.header_icon_url = dainyu(header_icon_url, self.header_icon_url)
        self.footer = dainyu(footer, self.footer)
        self.title = dainyu(title, self.title)
        self.greeting = dainyu(greeting, self.greeting)
        self.description = desc
        if arg:
            self.footer_arg += arg
        self.bottums = dainyu(bottums, self.bottums)
        self.bottums_sub = dainyu(bottums_sub, self.bottums_sub)
        self.bottum_args = dainyu(bottum_args, self.bottum_args)

    def setCtx(self, ctx):
        self.ctx = dainyu(ctx, self.ctx)
        self.bot = dainyu(ctx.bot, self.bot)
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

    def default_embed(
        self,
        bot=None,
        mention=str(),
        mention_author=bool(),
        title=None,
        color=None,
        description=None,
        thumbnail=False,
        header=str(),
        header_icon=None,
        footer=str(),
        footer_url=str(),
        time=True,
        greeting=str(),
        footer_arg=str(),
        dust=True,
        bottum_args=None,
    ) -> classmethod:
        """
        embed初期化※必ず必要

        Args:
            title (str, optional): タイトル. Defaults to None.
            color (0x, optional): 色. Defaults to 0x00FF00.
            description (str, optional): 説明. Defaults to None.
            thumbnail (bool), optional): 大きめのアイコン画像を表示させるかどうか. Defaults to False.
            header (str, optional): ヘッダー文. Defaults to str().
            header_icon (str, optional): ヘッダーアイコンurl. Defaults to None.
            footer (str, optional): フッター文. Defaults to str().
            footer_url (str, optional): フッター画像url. Defaults to str().
            time (bool, optional): 時間を表示させるかどうか. Defaults to True.
            greeting (str, optional): embedの前につける文. Defaults to str().
            footer_arg (str, optional): embed識別コード. Defaults to str().

        Returns:
            [type]: [description]
        """
        self.mention = mention
        self.mention_author = mention_author
        self.title = title
        self.color = dainyu(color, self.color)
        self.time = time
        self.footer = footer
        self.icon_url = footer_url if footer else str()
        self.header = header
        self.header_icon_url = header_icon if header else str()
        self.thumbnai = thumbnail
        self.greeting = greeting
        self.footer_arg = footer_arg
        self.description = (
            (self.__export_complist(obj=description)).pop() if description else None
        )
        self.bottum_args = bottum_args
        return self

    def add(
        self, name: str, value: str, inline=False, greeting=str(), description=str()
    ) -> None:
        if greeting:
            self.greeting = greeting
        self.description = description if description else self.description
        self.fields.append({"name": name, "value": value, "inline": inline})

    def clone(self, ctx=None) -> classmethod:

        return (copy(self)).setCtx(ctx)

    async def sendEmbed(
        self,
        obj=None,
        mention_author=bool(),
        mention=str(),
        greeting=str(),
        footer_arg=str(),
        bottums=list(),
        bottums_sub=list(),
        bottum_args=None,
        files=list(),
        dust=bool(),
    ) -> Message:
        """
        embed送信

        Args:
            obj (object, optional): なんだっけこれ. Defaults to None.
            greeting (str, optional): えむベッドの前につける文. Defaults to str().
            footer_arg (str, optional): embed識別コード. Defaults to str().
            bottums (list, optional): 追加するリアクションのリスト. Defaults to list().
            files (list, optional): 添付ファイルのリスト. Defaults to list().
            dust (bool), optional): ゴミ箱リアクションをつけるかどうか. Defaults to True.

        Returns:
            Message: 送信したメッセージ
        """
        self.mention = dainyu(mention, self.mention)
        self.mention_author = dainyu(mention_author, self.mention_author)
        self.greeting = dainyu(greeting, self.greeting)
        if self.mention:
            self.greeting = self.mention + self.greeting
        elif bool(self.mention_author) & bool(self.ctx):
            self.greeting = self.ctx.author.mention + self.greeting
        self.dust = dainyu(dust, self.dust)
        if bool(self.footer_arg) or bool(footer_arg):
            self.footer_arg = f"@{self.footer_arg}{footer_arg}"
        self.bottums = dainyu(bottums, self.bottums)
        self.bottums_sub = dainyu(bottums_sub, self.bottums_sub)
        self.bottum_args = dainyu(bottum_args, self.bottum_args)
        config = dict()
        config["color"] = self.color
        config["title"] = dainyu(self.title)
        config["description"] = dainyu(self.description)
        config["files"] = dainyu(self.files)
        config["fields"] = self.fields

        if (bool(self.footer)) or (bool(self.footer_arg)):
            time_str = str()
            if self.time:
                time_str = (datetime.now()).strftime("%m/%d %H:%M:%S")
            config["footer"] = {"text": f"{time_str}#{self.footer}{self.footer_arg}"}
            config["footer"]["icon_url"] = dainyu(self.icon_url)

        bot_info = await self.bot.application_info()

        if ((bool(self.bot)) & self.thumbnail) & (bool(bot_info)):
            config["thumbnail"] = {"url": str(bot_info.icon_url)}

        if self.header:
            config["author"] = {"name": self.header}
            if isinstance(self.header_icon_url, str):
                config["author"]["icon_url"] = str(self.header_icon_url)
            elif bot_info:
                config["author"]["icon_url"] = str(bot_info.icon_url)

        self.embed = Embed()
        self.embed = Embed.from_dict(config)

        obj = obj[0] if isinstance(self.obj, list) else self.obj
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
                    if b in UNICODE_EMOJI:
                        await ms.add_reaction(b)
            if self.bottums_sub:
                await ms.add_reaction("🔽")
                self.bot.config[str(ms.guild.id)]["bottoms_sub"][
                    ms.id
                ] = self.bottums_sub
                self.bot.config[str(ms.guild.id)]["bottoms"][ms.id] = self.bottums
            if self.bottum_args:
                self.bot.config[str(ms.guild.id)]["bottom_args"][
                    ms.id
                ] = self.bottum_args
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

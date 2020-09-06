from discord import Embed, TextChannel
from web import table
from os import linesep
# from copy import copy


class MakeEmbed():
    def __init__(self, ctx=None, bot=None, target=None):
        self.ctx = ctx
        self.bot = ctx.bot if ctx else bot
        self.target = target
        self.embed = None
        self.db_ep = table.EmbedPages()
        self.descriptions = list()
        self.line_number = int(0)
        self.config = {}
        self.bot_info = None

    def cut(self, obj: str):
        point = 50
        if isinstance(obj, str):
            if len(obj) > point:
                ex = (f'{obj[:point+1]}\n')
                ex = ex + (self.cut(obj[point + 1:]))
            else:
                ex = (f'{obj}\n')
        else:
            ex = 'TextError'
        return ex

    def export_complist(self, obj):
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
                content = self.cut(o)
                line = len(content)
                # print(f"{o},{line}")
                while(line > 0):
                    if (line + lines) > 10:
                        if ex:
                            ex[-1] = ex[-1] + content[: 15 - lines + 1]
                        else:
                            ex.append(content[: 15 - lines + 1])
                        content = content[15 - lines + 1:]
                        lines = 0
                        line = line - 15 + lines - 1
                    else:
                        if ex:
                            ex[-1] = ex[-1] + content
                        else:
                            ex.append(content)
                        line = 0
        return ex

    def add(self, name: str, value: str, inline: bool) -> None:
        if self.config:
            self.config['fields'].append({
                'name': name,
                'value': value,
                'inline': inline})

    async def sendEmbed(self, obj=None, nomal=str()):
        self.embed = Embed()
        self.embed = Embed.from_dict(self.config)
        obj = (obj[0] if isinstance(obj, list) else obj)
        if self.target:
            obj = self.target
        elif not(obj):
            obj = self.ctx.channel
        if obj:
            ms = await obj.send(embed=self.embed, content=nomal)
            await ms.add_reaction("⬅")
            await ms.add_reaction("➡")
        # if isinstance(self.description, list):
        #     i = 1
        #     self.db_ep.add(
        #         id=ms.id,
        #         number=i,
        #         content=self.description.pop(0),
        #         isnow=True)
        #     for desc in self.description:
        # self.db_ep.add(id=ms.id, number=++i, content=desc, isnow=False)
            return ms
        else:
            pass

    async def default_embed(self, title=None, description=None, thumbnail=False, header=None, header_icon=None, footer=None, footer_url=None):
        config = {
            'title': title,
            'color': 0x00ff00,
            'fields': []
        }
        if description:
            self.descriptions = self.export_complist(obj=description)
            config['description'] = self.descriptions[0]
        if self.bot:
            self.bot_info = await self.bot.application_info()
            if thumbnail:
                config['thumnail'] = {'url': str(self.bot_info.icon_url)}
        if header:
            if isinstance(footer, bool) & bool(self.bot_info):
                config['author'] = {
                    "name": header,
                    "icon_url": str(self.bot_info.icon_url)}
            elif header_icon:
                config['author'] = {
                    "name": header, "icon_url": str(header_icon)}
            else:
                config['author'] = {"name": header}
        if footer:
            if isinstance(footer, bool) & bool(self.ctx):
                string = f"{self.ctx.prefix} {self.ctx.command}"
                if self.ctx.invoked_subcommand:
                    string += f" {(self.ctx.invoked_subcommand).name}"
                config['footer'] = {'text': string}
            elif footer_url:
                config['footer'] = {
                    'text': footer, 'icon_url': str(footer_url)}
            else:
                config['footer'] = {'text': footer}
        self.config = config

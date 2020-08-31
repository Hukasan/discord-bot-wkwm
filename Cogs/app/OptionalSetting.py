from discord import Embed, TextChannel
from discord.ext import commands
from web import table
from os import linesep
from copy import copy


class Option():
    def __init__(self, ctx=commands.Context):
        self.ctx = ctx
        self.embed = Embed()
        self.db_ep = table.EmbedPages()
        self.description = list()
        self.line_number = int(0)

    def get_ctx(self, ctx: commands.Context):
        self.ctx = ctx

    def export_complist(self, obj):
        exlist = list()
        if isinstance(obj, str):
            if len(obj) > 10:
                exlist.append(obj[:11])
                exlist.append(self.export_complist(obj[11:]))
                return exlist
            else:
                return obj
        elif isinstance(obj, list):
            for s in obj:
                a = self.export_complist(s)
                if isinstance(a, list):
                    exlist.extend(a)
                elif isinstance(a, str):
                    exlist.append(a)
            return exlist

    async def default_embed(self, title=None, description=None, thumbnail=False, header=None, header_icon=None, footer=None, footer_url=None):
        config = {
            'color': 0x00ff00,
        }
        if title:
            config['title'] = title
        if description:
            if isinstance(description, list):
                lines = list()
                for desc in description:
                    lines.append(
                        self.export_complist(desc.splitlines()))
                if len(lines[0]) <= 15:
                    config['description'] = '\r'.join(lines)
                    self.description = lines
                else:
                    lines[1] = list
                    lines.e
            else:
                config['description'] = description
        self.embed = Embed()
        self.embed = Embed.from_dict(config)
        if thumbnail:
            self.bot_info = await self.ctx.bot.application_info()
            self.embed = self.embed.set_thumbnail(

                url=str(self.bot_info.icon_url))
        if header:
            if isinstance(footer, bool):
                self.bot_info = await self.ctx.bot.application_info()
                self.embed.set_author(name=header, icon_url=str(
                    self.bot_info.icon_url))
            elif header_icon:
                self.embed.set_author(name=header, icon_url=str(header_icon))
            else:
                self.embed.set_author(name=header)
        if footer:
            if footer_url:
                self.embed.set_footer(text=footer, icon_url=str(footer_url))
            if isinstance(footer, bool):
                string = f"{self.ctx.prefix} {self.ctx.command}"
                if self.ctx.invoked_subcommand:
                    string += f" {(self.ctx.invoked_subcommand).name}"
                self.embed.set_footer(text=string)
            else:
                self.embed.set_footer(text=f"{footer}")
        self.description = description

    def add(self, name: str, value: str, inline: bool) -> None:
        self.embed.add_field(name=name, value=value, inline=inline)

    async def sendEmbed(self, obj=None):
        obj = (obj[0] if isinstance(obj, list) else obj)
        obj = (obj if obj else self.ctx)
        ms = await obj.channel.send(embed=self.embed)
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

from discord import Embed
from discord.ext import commands


class Option():
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def default_embed(self, title=None, description=None, thumbnail=False, header=None, header_icon=None, footer=None, footer_url=None):
        config = {
            'color': 0x00ff00,
        }
        if title:
            config['title'] = title
        if description:
            config['description'] = description
        embed = Embed()
        embed = Embed.from_dict(config)
        if thumbnail:
            self.bot_info = await self.bot.application_info()
            embed = embed.set_thumbnail(url=str(self.bot_info.icon_url))
        if header:
            if header_icon == "default":
                embed.set_author(name=header, icon_url=str(
                    self.bot_info.icon_url))
            elif header_icon:
                embed.set_author(name=header, icon_url=str(header_icon))
            else:
                embed.set_author(name=header)
        if footer:
            if footer_url:
                embed.set_footer(text=footer, icon_url=str(footer_url))
            else:
                embed.set_footer(text=f"{footer}")

        return embed

import discord
from discord.ext.commands import (
    Cog,
    Bot,
    Context,
    HelpCommand,
    command,
    is_owner,
    Group,
    Command,
)
from Cogs.app import table, make_embed as me


class Setting(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @is_owner()
    @command(aliases=["re", "lode", "l"], description="プログラムを再読み込み")
    async def load(self, ctx: Context):
        for extension in list(self.bot.extensions):
            self.bot.reload_extension(f"{extension}")
            print(f"{extension}_is_reloted")
        print("再読み込み完了")
        await ctx.message.add_reaction("☑")


def setup(bot: Bot):
    return bot.add_cog(Setting(bot))

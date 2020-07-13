import discord
from discord.ext import commands
from collections import OrderedDict
import json
import sys

# from box import Box  # noqa

# from json_io import json_box_io  # noqa


class TalkIO(commands.Cog, name='TalkIO'):
    """会話系のコマンド群です
    """

    def __init__(self, bot):
        self.bot = bot
        self.jpop()

    def jpop(self):
        try:
            with open("../jsons/Hangar.json", mode='r') as f:
                self.jf = json.load(f)
        except BaseException:
            print("Could not load Hangar.json for pop")
            print("EXIT")
            sys.exit(1)
        self.st = self.jf["TalkState"]
        self.jreact = self.jf["cats"]

    def jpush(self):
        try:
            with open("../jsons/Hangar.json", mode='w', encoding='utf-8') as f:
                f.write(json.dumps(self.jf))
        except BaseException:
            print("Could not load Hangar.json for push")
            print("EXIT")
            sys.exit(1)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        self.jpop()
        cmd = str()
        cmd = ((str(error)).split('"', maxsplit=2))[1]
        # if cmd self.jreact[]

    @commands.group(description="コマンドに関するコマンド群")
    async def cmd(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがいるよ 例:\r$add cmd -> コマンドを追加")

    @cmd.command(aliases=["ca"], description="コマンドを追加したい(希望)")
    async def add(self, ctx, key, value):
        """コマンドを追加します
        """
        await ctx.send("OK")

    @commands.group(description="リアクションに関するコマンド群")
    async def react(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがいるよ 例:\r$react cmd -> コマンドを追加")

    @react.command(aliases=["ra"], description="リアクションを追加したい(無謀)")
    async def add(self, ctx):
        await ctx.send("OOK")

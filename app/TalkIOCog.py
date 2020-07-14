import discord
from discord.ext import commands
from collections import OrderedDict
import json
import sys


class TalkIO(commands.Cog, name='TalkIO'):
    """会話系のコマンド群です
    """

    def __init__(self, bot):
        self.bot = bot
        self.jpop()

    def jpop(self):
        try:
            with open("./jsons/Hangar.json", mode='r', encoding='utf-8') as f:
                self.jf = json.load(f)
        except BaseException:
            print("Could not load Hangar.json for pop")
            print("EXIT")
            sys.exit(1)
        self.jreact = self.jf["cats"]
        self.jcmd = self.jf["Cmds"]

    def jpush(self):
        try:
            with open("../jsons/Hangar.json", mode='w',  encoding='utf-8') as f:
                f.write(json.dumps(self.jf, ensure_ascii=False))
        except BaseException:
            print("Could not load Hangar.json for push")
            print("EXIT")
            sys.exit(1)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        self.jpop()
        cmd = str()
        try:
            cmd = ((str(error)).split('"', maxsplit=2))[1]
            if cmd in self.jcmd:
                await ctx.send(self.jcmd[cmd]["react"])
            else:
                await ctx.send("こまんどいずのっとふぁうんどcheck $help")
        except IndexError:
            if str(error) == "trigger is a required argument that is missing.":
                await ctx.send("入力する値の数が足りてません")
            else:
                await ctx.send("管轄外エラー:" + str(error))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        content = message.content
        self.jpop()
        print(content)
        for key in self.jreact:
            if key in content:
                await message.channel.send(self.jreact[key]["react"])
                return
        pass

    @commands.is_owner()
    @commands.group(description="コマンド管理コマンド")
    async def cmd(self, ctx):
        """[※管理者のみ]
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがいるよ 例:\r$add cmd -> コマンドを追加")

    @cmd.command(aliases=["ca"], description="コマンド追加")
    async def add(self, ctx, key, reaction):
        """反応することばを追加します
            $cmd add key reaction
        Args:
            key : 追加するコマンド[${key}]
            reaction : keyに対するリアクション
        """
        await ctx.send("OK")

    @add.error
    async def add_error(self, ctx, error):
        print(type(error))
        if isinstance(error, commands.BadArgument):
            await ctx.send('入力する値の数が足りてません　例:\r$cat add くさ こいつ草とかいってます->「くさ」で「こいつ草とかいってます」')

    @commands.group(description="リアクション管理コマンド")
    async def cat(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがいるよ 例:\r$cat view -> 一覧を表示")

    @commands.is_owner()
    @cat.command(aliases=["ra"], description=("リアクション追加"))
    async def add(self, ctx, trigger, reaction):
        try:
            self.jreact[trigger] = {"react": reaction}
            self.jpush()
            await ctx.send("さくせす")
        except BaseException:
            await ctx.send("なぞかきこみえらー in cat add")

    @ cat.command(aliases=["v"], description="一覧表示")
    async def view(self, ctx):
        """反応することばを出力します
        """
        maped_list = map(str, list(self.jreact.keys())[1:])  # mapで要素すべてを文字列に
        mojiretu = ','.join(maped_list)
        embed = discord.Embed(title="Catcalls",
                              description=self.jreact["desc"], color=0x00ff00)
        embed.add_field(name="CommandList：",
                        value=mojiretu.replace(',', '\r'))  # noqa
        await ctx.send(embed=embed)
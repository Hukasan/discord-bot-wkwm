import discord
from discord.ext import commands
from web import table
from dispander import dispand
from Cogs.OptionalSetting import Option


class TalkIO(commands.Cog, name='会話'):
    """会話系のコマンド群です
    """

    def __init__(self, bot):
        self.bot = bot
        self.db_cmd = table.Cmdtb()
        self.db_cat = table.Cattb()
        self.opt = Option(self.bot)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        cmd = str()
        try:
            cmd = ((str(error)).split('"', maxsplit=2))[1]
            result = self.db_cmd.tbselect(cmd)
            if result:
                await ctx.send(result[0].body)
            else:
                await ctx.send(str(error))
        except IndexError:
            if str(error) == "trigger is a required argument that is missing.":
                await ctx.send("入力する値の数が足りてません")
            else:
                await ctx.send(f"管轄外エラー:on_message\r```{str(error)}```")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        await dispand(message)
        content = message.content
        ex_content = str()
        print(f"->{content}")
        for query in self.db_cat.tbselect():
            if query.id in content:
                ex_content += query.body
        if ex_content:
            await message.channel.send(ex_content)
            return
        pass

    @commands.is_owner()
    @commands.group(description="コマンド管理")
    async def cmd(self, ctx):
        """[※管理者のみ]
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがいるよ 例:\r$cmd add -> コマンドを追加")

    @commands.is_owner()
    @cmd.command(aliases=["うんち"], description="コマンド追加")
    async def add(self, ctx, key, reaction):
        """反応することばを追加します
            $cmd add key reaction
        Args:
            key: 追加するコマンド[${key}]
            reaction: keyに対するリアクション
        """
        try:
            self.db_cmd.add(title=key, body=reaction)
            await ctx.send("さくせす")
        except BaseException:
            await ctx.send("なぞかきこみえらー in cat add")

    @add.error
    async def add_error(self, ctx, error):
        print(type(error))
        if isinstance(error, commands.BadArgument):
            await ctx.send('入力する値の数が足りてません　例:\r$cat add くさ こいつ草とかいってます->「くさ」で「こいつ草とかいってます」')

    @commands.group(description="リアクション管理コマンド", pass_context=True)
    async def cat(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがいるよ 例:\r$cat view -> 一覧を表示")

    @commands.is_owner()
    @cat.command(aliases=["うんちっち"], description=("リアクション追加"))
    async def add(self, ctx, trigger, reaction):
        # try:
        self.db_cat.add(id=trigger, body=reaction)
        await ctx.send("さくせす")
        # except BaseException:
        #     await ctx.send("なぞかきこみえらー in cat add")

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('入力する値の数が足りてません　例:\r$cat add くさ こいつ草とかいってます->「くさ」で「こいつ草とかいってます」')
        await ctx.send(f"なぞかきこみえらー : cat add```python{error}```")

    async def view_titles_toembed(self, t, title: str) -> discord.Embed:
        content = str()
        qlist = t.tbselect()
        for q in qlist:
            content += f"・{q.id}\n"
        embed = await self.opt.default_embed(title=title)
        embed.add_field(name="__List__",
                        value=f"```{content}```")  # noqa
        return embed

    @ cat.command(aliases=["v"], description="一覧表示")
    async def view(self, ctx):
        """反応することば一覧を出力します
        """
        await ctx.send(embed=await self.view_titles_toembed(t=self.db_cat, title="リアクション"))

    @commands.command(description="追加された,会話コマンド,リアクションを全部表示します")
    async def view(self, ctx):  # noqa
        await ctx.send(embed=await self.view_titles_toembed(t=self.db_cat, title="リアクション"))
        await ctx.send(embed=await self.view_titles_toembed(t=self.db_cmd, title="チャットコマンド"))


def setup(bot):
    return bot.add_cog(TalkIO(bot))

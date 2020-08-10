import discord
from discord.ext import commands
from web import table
from dispander import dispand
from Cogs.OptionalSetting import Option


class TalkIO(commands.Cog, name='Talk'):
    """会話系のコマンド群です
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db_cmd = table.Cmdtb()
        self.db_cat = table.Cattb()
        self.opt = Option()
    # def check_role_is_upper(self):
    #     def predicate(ctx: commands.Context):
    #         self.botctx.author

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        cmd = str()
        try:
            cmd = ((str(error)).split('"', maxsplit=2))[1]
            dubleq = str(error).split("\"")
            result = self.db_cmd.tbselect(cmd)
            if result:
                await ctx.send(result[0].body)
            elif dubleq:
                print(dubleq)
                if dubleq[0] == "Command " and dubleq[2] == " is not found":
                    await ctx.send(f"こまんどに　\" {dubleq[1]} \"　はないみたいです")
                else:
                    await ctx.send(f"コマンドエラー:\r```{str(error)}```")
            else:
                await ctx.send(f"コマンドエラー:\r```{str(error)}```")
        except IndexError:
            if str(error) == "trigger is a required argument that is missing.":
                await ctx.send("入力する値の数が足りてません")
            else:
                await ctx.send(f"内部エラー:on_message\r```{str(error)}```")

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

    @commands.is_owner()
    @commands.group(aliases=["cm", "コマンド", "こまんど"], description="コマンド管理")
    async def cmds(self, ctx):
        """[※管理者のみ]
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがいるよ 例:\r$cmd add -> コマンド追加")

    @commands.is_owner()
    @cmds.command(aliases=["a", "ついか", "追加"], description="コマンド追加")
    async def cmdadd(self, ctx, key, reaction):
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

    @cmdadd.error
    async def cmdadd_error(self, ctx, error):
        print(type(error))
        if isinstance(error, commands.BadArgument):
            await ctx.send('入力する値の数が足りてません　例:\r$cat add くさ こいつ草とかいってます->「くさ」で「こいつ草とかいってます」')

    @commands.group(aliases=["c", "ｃ", "ｃａｔ", "りあくしょん",
                             "リアクション", "キャッツ", "きゃっつ"], description="リアクション管理")
    async def cats(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがいるよ 例:\r$cat view -> 一覧を表示")

    @cats.command(aliases=["add", "a", "ついか", "追加"], description=("リアクション追加"))
    async def catadd(self, ctx, trigger, reaction):
        # try:
        self.db_cat.add(id=trigger, body=reaction)
        await ctx.send("さくせす")
        # except BaseException:
        #     await ctx.send("なぞかきこみえらー in cat add")

    @catadd.error
    async def catadd_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('入力する値の数が足りてません　例:\r$cat add くさ こいつ草とかいってます->「くさ」で「こいつ草とかいってます」')
        await ctx.send(f"なぞかきこみえらー : cat add```python{error}```")

    async def view_titles_toembed(self, t, title=str(), embed=discord.Embed()) -> discord.Embed:
        content = str()
        qlist = t.tbselect()
        for q in qlist:
            content += f"・{q.id}\n"
        if not(embed):
            embed = await self.opt.default_embed(footer=True)
        embed.add_field(name=f"**{title}**", value=f"```{content}```")  # noqa
        return embed

    @ cats.command(aliases=["v",
                            "ｖｉｅｗ",
                            "ｖ",
                            "ビュー",
                            "びゅー",
                            "一覧",
                            "いちらん"],
                   description="追加されたリアクションを表示")
    async def catview(self, ctx):
        """反応することば一覧を出力します
        """
        self.opt.get_ctx(ctx)
        await ctx.send(embed=await self.view_titles_toembed(t=self.db_cat, title="リアクション"))

    @commands.group(aliases=["v",
                             "ｖｉｅｗ",
                             "ｖ",
                             "ビュー",
                             "びゅー",
                             "一覧",
                             "いちらん"], description="コマンド、リアクション一覧")
    async def view(self, ctx):  # noqa
        self.opt.get_ctx(ctx)
        em = await self.view_titles_toembed(t=self.db_cat, title="リアクション")
        await ctx.send(embed=await self.view_titles_toembed(t=self.db_cmd, title="コマンド", embed=em))

    @view.command()
    async def cat(self, ctx):
        pass


def setup(bot):
    return bot.add_cog(TalkIO(bot))

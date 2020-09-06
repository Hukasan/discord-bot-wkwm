from discord import Guild
from discord.ext import commands
from web import table
from dispander import dispand, compose_embed
from Cogs.app.OptionalSetting import Option
from Cogs.app.TeamManage import Team
from gc import collect


class TalkIO(commands.Cog, name='Talk'):
    """会話系のコマンド群です
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db_cmd = table.Cmdtb()
        self.db_cat = table.Cattb()
        self.opt = Option()
        self.team = Team(bot)
        self.room_id = int(self.bot.config['wkwm']['room_id'])

    def check_role_is_upper(self):
        def predicate(ctx: commands.Context):
            self.ctx.author

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     cmd = str()
    #     try:
    #         cmd = ((str(error)).split('"', maxsplit=2))[1]
    #         dubleq = str(error).split("\"")
    #         result = self.db_cmd.tbselect(cmd)
    #         if result:
    #             await ctx.send(result[0].body)
    #         elif dubleq:
    #             if dubleq[0] == "Command " and dubleq[2] == " is not found":
    #                 await ctx.send(f"こまんどに　\" {dubleq[1]} \"　はないみたいです")
    #             else:
    #                 await ctx.send(f"コマンドエラー:\r```{str(error)}```")
    #         else:
    #             await ctx.send(f"コマンドエラー:\r```{str(error)}```")
    #     except IndexError:
    #         if str(error) == "trigger is a required argument that is missing.":
    #             await ctx.send("入力する値の数が足りてません")
    #         else:
    #             await ctx.send(f"内部エラー:on_message\r```{str(error)}```")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        await dispand(message)  # もしもdiscord内のメッセージリンクだったばあいそれをプレビュ
        await self.team.scan_message(message, self.room_id)
        content = message.content
        ex_content = str()
        # print(f"->{content}")
        for query in self.db_cat.tbselect():
            if query.id in content:
                ex_content += query.body
        if ex_content:
            await message.channel.send(ex_content)
            return
        collect()

    @commands.command(aliases=["ピン留め", "ピン", "ぴんどめ"], description="ぴんどめ表示")
    async def pins(self, ctx: commands.Context):
        for ms in await ctx.channel.pins():
            await ctx.send(embed=(compose_embed(ms)))

    @commands.command(aliases=["ロールメンバー", "ろーるめんばー",
                               "rm"], description="ロールメンバ表示")
    async def rolemember(self, ctx: commands.Context, name: str):
        g = Guild
        g = ctx.guild
        opt = Option(ctx)
        await opt.default_embed(title=f"SerchRole\"{name}\"")
        i = 0
        context = str()
        for role in await g.fetch_roles():
            if role.name == name:
                for m in role.members:
                    i += 1
                    context += f"{i} : {m.mention}\r"
                break
        if context:
            opt.add(name="Result", value=context, inline=False)
        else:
            opt.add(name="Result", value="見つかりませんでしたてへ。", inline=False)
        await opt.sendEmbed(None)

    @commands.is_owner()
    @commands.group(aliases=["cm", "コマンド", "こまんど"], description="コマンド管理")
    async def cmds(self, ctx):
        """[※管理者のみ]
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがいるよ 例:\r$cmd add -> コマンド追加")

    @commands.is_owner()
    @cmds.command(aliases=["a", "ついか", "追加"], description="コマンド追加")
    async def cmdsadd(self, ctx, key, reaction):
        self.db_cmd.add(id=key, body=reaction)
        await ctx.send("追加いず、さくせすъ(ﾟДﾟ)")

    @cmdsadd.error
    async def cmdsadd_error(self, ctx, error):
        print(type(error))
        if isinstance(error, commands.BadArgument):
            await ctx.send('入力する値の数が足りてません　例:\r$cat add くさ こいつ草とかいってます->「くさ」で「こいつ草とかいってます」')

    @cmds.command(aliases=["delete", "d", "削除", "さくじょ"],
                  description=("コマンド削除"))
    async def cmdsdelete(self, ctx, key):
        self.db_cmd.tbdelete(id=str(key))
        await ctx.send(f"さくせす {key} の削除に成功しましたぁ")

    @commands.is_owner()
    @commands.group(aliases=["c", "ｃ", "ｃａｔ", "りあくしょん",
                             "リアクション", "キャッツ", "きゃっつ"], description="リアクション管理")
    async def cats(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがいるよ 例:\r$cat view -> 一覧を表示")

    @cats.command(aliases=["add", "a", "ついか", "追加"], description=("リアクション追加"))
    async def catsadd(self, ctx, trigger, reaction):
        self.db_cat.add(id=trigger, body=reaction)
        await ctx.send("さくせす")

    @catsadd.error
    async def catsadd_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('入力する値の数が足りてません　例:\r$cat add くさ こいつ草とかいってます->「くさ」で「こいつ草とかいってます」')
        else:
            await ctx.send(f"なぞかきこみえらー : in cat add```python{error}```")

    @cats.command(aliases=["delete", "d", "削除", "さくじょ"],
                  description=("リアクション削除"))
    async def catsdelete(self, ctx, key):
        self.db_cat.tbdelete(id=str(key))
        await ctx.send(f"さくせす {key} の削除に成功しました💩")

    @ commands.group(aliases=["v",
                              "ｖｉｅｗ",
                              "ｖ",
                              "ビュー",
                              "びゅー",
                              "一覧",
                              "いちらん"], description="コマンド、リアクション一覧")
    async def view(self, ctx):  # noqa
        self.opt.get_ctx(ctx)
        await self.view_titles_toembed(t=self.db_cat, title="リアクション")
        await self.view_titles_toembed(t=self.db_cmd, title="コマンド")
        await self.opt.sendEmbed(None)

    @ view.command(aliases=["リアクション", "り", "りあくしょん", "reaction", "react"],
                   description="追加されたリアクションを表示")
    async def catview(self, ctx):
        """反応することば一覧を出力します
        """
        self.opt.get_ctx(ctx)
        await self.view_titles_toembed(t=self.db_cat,
                                       title="リアクション")
        await self.opt.sendEmbed()

    async def view_titles_toembed(self, t, title=str()):
        content = str()
        qlist = t.tbselect()
        for q in qlist:
            content += f"・{q.id}\n"
        if not(self.opt.embed):
            await self.opt.default_embed(footer=True)
        self.opt.add(name=f"**{title}**", value=f"```{content}```")  # noqa


def setup(bot):
    return bot.add_cog(TalkIO(bot))

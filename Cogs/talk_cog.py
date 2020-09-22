from discord import Guild
from discord.ext import commands
from dispander import dispand, compose_embed
from Cogs.app import table, make_embed as me
from gc import collect


class Talk(commands.Cog):
    """会話系のコマンド群"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db_cmd = table.Cmdtb()
        self.db_cat = table.Cattb()
        # self.team = Team(bot)
        self.room_id = int(self.bot.config["wkwm"]["room_id"])

    def check_role_is_upper(self):
        def predicate(ctx: commands.Context):
            self.ctx.author

    @commands.Cog.listener()
    async def on_message(self, message):
        # print(f'ms->[{message.content}]')
        if message.author.bot:
            return
        await dispand(message)  # もしもdiscord内のメッセージリンクだったばあいそれをプレビュ
        # await self.team.scan_message(message, self.room_id)
        content = message.content
        ex_content = str()
        for query in self.db_cat.tbselect():
            if query.id in content:
                ex_content += query.body
        if ex_content:
            await message.channel.send(ex_content)
            return
        # collect()

    @commands.is_owner()
    @commands.group(aliases=["c", "ｃ", "コマンド", "こまんど", "command"], description="コマンド管理")
    async def cmd(self, ctx):
        """[※管理者のみ]"""
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドがいるよ 例:\r$cmd add -> コマンド追加")

    @commands.is_owner()
    @cmd.command(aliases=["a", "ついか", "追加"], description="追加")
    async def cmd_add(self, ctx, key, reaction):
        self.db_cmd.add(id=key, body=reaction)
        await ctx.send("追加いず、さくせすъ(ﾟДﾟ)")

    @cmd.command(aliases=["delete", "d", "削除", "さくじょ"], description=("削除"))
    async def cmd_delete(self, ctx, key):
        self.db_cmd.tbdelete(id=str(key))
        await ctx.send(f"さくせす {key} の削除に成功しましたぁ")

    @commands.is_owner()
    @commands.group(
        aliases=["r", "ｒ", "react", "reaction", "りあくしょん", "リアクション"],
        description="リアクション管理",
    )
    async def cat(self, ctx):
        """
        ※このコマンドは親コマンドです、サブコマンドを指定してください。
        """
        if ctx.invoked_subcommand is None:
            raise Exception("trigger is a required argument that is missing.")

    @cat.group(aliases=["add", "a", "ついか", "追加"], description=("追加"))
    async def cat_add(self, ctx, trigger, reaction):
        """
        リアクションを追加します。
            trigger 　: 反応する言葉
            reaction　: リアクション
        > ? cat add てすと うんち
        で、会話内の「てすと」に対して「うんち」といいます
        """
        if ctx.invoked_subcommand is None:
            self.db_cat.add(id=trigger, body=reaction)
            await ctx.send("さくせす")

    @cat_add.command(aliases=["r", "react", "ｒ"])
    async def cat_add_react(self, ctx, _, trigger, reaction):
        self.db_cat.add(id=trigger, body=reaction, isreact=True)
        await ctx.send("さくせすx")

    @cat.command(aliases=["delete", "d", "削除", "さくじょ"], description=("削除"))
    async def cat_delete(self, ctx, key):
        self.db_cat.tbdelete(id=str(key))
        await ctx.send(f"さくせす {key} の削除に成功しました💩")

    @commands.group(
        aliases=["v", "ｖｉｅｗ", "ｖ", "ビュー", "びゅー", "一覧", "いちらん"], description="一覧表示"
    )
    async def view(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = me.MyEmbed(ctx)
            await self.view_titles_toembed(embed, t=self.db_cat, title="リアクション")
            await self.view_titles_toembed(embed, t=self.db_cmd, title="コマンド")
            await embed.sendEmbed()

    @view.command(
        aliases=["リアクション", "りあくしょん", "reaction", "react", "r"], description="リアクション一覧"
    )
    async def view_cat(self, ctx):
        embed = me.MyEmbed(ctx)
        await self.view_titles_toembed(embed, t=self.db_cat, title="リアクション")
        await embed.sendEmbed()

    @view.command(aliases=["コマンド", "こまんど", "cmd", "command", "c"], description="コマンド一覧")
    async def view_cmd(self, ctx):
        """"""
        embed = me.MyEmbed(ctx)
        await self.view_titles_toembed(embed, t=self.db_cmd, title="コマンド")
        await embed.sendEmbed()

    async def view_titles_toembed(self, embed: me.MyEmbed, t, title=str()):
        content = str()
        qlist = t.tbselect()
        for q in qlist:
            content += f"・{q.id}\n"
        if not (embed.config):
            await embed.default_embed(footer=True)
        embed.add(name=f"**{title}**", value=f"```{content}```", inline=True)  # noqa


def setup(bot):
    return bot.add_cog(Talk(bot))

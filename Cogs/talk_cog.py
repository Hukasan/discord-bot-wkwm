from discord import Guild, Message
from discord.ext.commands import Context
from discord.ext import commands
from dispander import dispand, compose_embed
from Cogs.app import (
    table,
    make_embed as me,
    extentions,
    role_checker as ac,
    team_manage as tm,
)
from gc import collect
from emoji import UNICODE_EMOJI


class Talk(commands.Cog):
    """会話系のコマンド"""

    qualified_name = "会話に横槍"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db_cmd = table.Cmdtb()
        self.db_cat = table.Cattb()
        self.teamio = tm.TeamIO(bot)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        # print(f'ms->[{message.content}]')
        if message.author.bot:
            return
        await dispand(message)  # もしもdiscord内のメッセージリンクだったばあいそれをプレビュ
        # await self.teamio.scan_message(message, self.room_id)
        content = message.content
        ex_content = str()
        for query in self.db_cat.tbselect():
            if query.id in content:
                if query.isreact:
                    await message.add_reaction(query.body)
                else:
                    ex_content += query.body

        if ex_content:
            await message.channel.send(ex_content)
            return
        # collect()

    @commands.group(aliases=["フレーズ", "ふれーず", "ふれ", "ph"], description="フレーズ管理")
    @ac.check_role_is_upper_member()
    async def phrase(self, ctx):
        if ctx.invoked_subcommand is None:
            raise Exception("trigger is a required argument that is missing.")

    @phrase.command(aliases=["a", "add", "ついか", "追加"], description="追加")
    async def phrase_add(self, ctx, key, reaction):
        self.db_cmd.add(id=key, body=reaction)
        await ctx.send("追加いず、さくせすъ(ﾟДﾟ)")

    @phrase.command(aliases=["delete", "d", "削除", "さくじょ"], description=("削除"))
    async def phrase_delete(self, ctx, key):
        self.db_cmd.tbdelete(id=str(key))
        await ctx.send(f"さくせす {key} の削除に成功しましたぁ")

    @commands.group(
        aliases=[
            "r",
            "ｒ",
            "react",
            "reaction",
            "りあくしょん",
            "リアクション",
            "ｃ",
            "c",
            "きゃっと",
            "キャット",
        ],
        description="リアクション管理",
    )
    async def cat(self, ctx):
        """
        特定のワードを会話の中に見つけると決められた言葉を喋りだす機能の設定を行うコマンドです、追加されている組み合わせは\r?viewで確認できます
        """
        if ctx.invoked_subcommand is None:
            raise Exception("trigger is a required argument that is missing.")

    @cat.command(aliases=["add", "a", "ついか", "追加", "つ", "あ"], description=("追加"))
    async def cat_add(self, ctx: Context, trigger, reaction):
        """
        trigger --- 反応させる言葉
        reaction --- しゃべる内容
        「?cat add てすと うんち」
        とすると、会話内の「てすと」に\r「うんち」と喋るよう設定されます
        """
        if ctx.invoked_subcommand is None:
            self.db_cat.add(id=trigger, body=reaction)
            await ctx.message.add_reaction("💮")
            await ctx.send("追加いず、さくせすъ(ﾟДﾟ)")

    @cat.command(aliases=["r", "react", "ｒ"], description=("追加※絵文字"))
    async def cat_add_react(self, ctx: Context, trigger, reaction):
        if reaction in UNICODE_EMOJI:
            self.db_cat.add(id=trigger, body=reaction, isreact=True)
            await ctx.message.add_reaction("💮")
            await ctx.send("追加いず、さくせすъ(ﾟДﾟ)")
        else:
            raise extentions.InputError(
                "このコマンドは、絵文字リアクション追加です\rリアクションに、絵文字を指定してください\r(例)?cat add_react うんち 💩"
            )

    @cat.command(aliases=["delete", "d", "削除", "さくじょ"], description=("削除"))
    async def cat_delete(self, ctx, key):
        for query in self.db_cat.tbselect():
            if query.id == key:
                self.db_cat.tbdelete(id=str(key))
                await ctx.message.add_reaction("💮")
                await ctx.send(f"さくせす {key} の削除に成功しました💩")
                return
        await ctx.message.add_reaction("😢")
        await ctx.send(f"ぴえん。 {key} の削除に失敗しました。\r入力を確認してください\r> [?view r]\rで一覧が表示できます")

    @commands.group(
        aliases=["v", "ｖｉｅｗ", "ｖ", "ビュー", "びゅー", "一覧", "いちらん"], description="一覧表示"
    )
    async def view(self, ctx: Context):
        """
        登録されている語句が表示されます
        """
        if ctx.invoked_subcommand is None:
            embed = me.MyEmbed(ctx)
            self.view_titles_toembed(embed, t=self.db_cat, title="YokoYari")
            self.view_titles_toembed(embed, t=self.db_cmd, title="Phrase")
            await embed.sendEmbed(mention=ctx.author.mention)

    @view.command(
        aliases=["リアクション", "りあくしょん", "ふ", "reaction", "react", "r", "cat", "c"],
        description="リアクションの表示",
    )
    async def view_cat(self, ctx):
        embed = me.MyEmbed(ctx)
        await self.view_titles_toembed(embed, t=self.db_cat, title="Reaction")
        await embed.sendEmbed(greeting=ctx.author.mention)

    @view.command(aliases=["フレーズ", "ふれーず", "phrase", "p"], description="フレーズの表示")
    async def view_phrase(self, ctx):
        embed = me.MyEmbed(ctx).default_embed(header="トリガープレビュー")
        await self.view_titles_toembed(embed, t=self.db_cmd, title="phrase")
        await embed.sendEmbed(greeting=ctx.author.mention)

    def view_titles_toembed(self, embed: me.MyEmbed, t, title=str()):
        content = str()
        qlist = t.tbselect()
        count = 0
        for q in qlist:
            content += f"・{q.id}\n"
            count += 1
            if count > 15:
                embed.add(name=f"**{title}**", value=f"```{content}```", inline=True)
                content = str()
                count = 0
        if content:
            embed.add(name=f"**{title}**", value=f"```{content}```", inline=True)


def setup(bot):
    return bot.add_cog(Talk(bot))

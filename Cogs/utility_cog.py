from discord.ext.commands import Cog, Bot, command, Context

# from dispander import dispand, compose_embed
from Cogs.app import make_embed as me, mymethods as mm


class Utilitys(Cog):
    """
    ちょっとした便利機能
    """

    qualified_name = "おまけ機能"

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=["ピン留め", "ピン", "ぴんどめ"], description="ぴんどめ表示")
    async def pins(self, ctx: Context):
        myembed = me.MyEmbed(ctx)
        myembed.default_embed(mention_author=True, dust=False)
        pins = await ctx.channel.pins()
        if pins:
            count = 1
            for ms in pins:
                image_url = str()
                if ms.embeds:
                    for embed in ms.embeds:
                        myembed.import_embed(embed)
                        myembed.change(
                            footer=f"📌ピン留め表示 {count}/{len(pins)}",
                        )
                        await myembed.sendEmbed()
                else:
                    if ms.attachments and ms.attachments[0].proxy_url:
                        image_url = ms.attachments[0].proxy_url
                    myembed.default_embed(
                        footer=f"📌ピン留め表示 {count}/{len(pins)}",
                        header=f"{ms.author.display_name}",
                        header_icon=str(ms.author.avatar_url),
                        time=ms.created_at,
                        image_url=image_url,
                        description=ms.content,
                    )
                    await myembed.sendEmbed()
                count += 1
        else:
            myembed = me.MyEmbed(ctx)
            myembed.default_embed(
                footer="📌ピン留め表示",
                title="ピン留めが見つかりませんでした",
                description="**このチャンネルにピン留めは無い様(*ﾟ∀ﾟ)ゞﾃﾞｼ**",
                mention_author=True,
                time=False,
            )
            await myembed.sendEmbed()

    @command(
        aliases=["rs", "ろーるさーち", "ロールサーチ", "ロール検索", "ろーる検索"], description="ロールメンバ表示"
    )
    async def serch(self, ctx: Context, name: str):
        g = ctx.guild
        opt = me.MyEmbed(ctx)
        opt.default_embed(mention_author=True, footer="🔎ロール検索")
        i = 0
        context = str()
        for (role, lastone) in mm.lastone(await g.fetch_roles()):
            if role.name == name:
                for m in role.members:
                    i += 1
                    context += f"{i} : {m.mention}\r"
                if context:
                    opt.add(name=f"🧻 {name} の猿ども", value=context, inline=False)
                else:
                    opt.add(name=f"🧻 {name} の猿ども", value="は、居ませんでした😢", inline=False)
            elif lastone:
                opt.add(name=f"🧻 {name} なんてなかった", value="そんなロールはござらん", inline=False)
        await opt.sendEmbed()


def setup(bot):
    return bot.add_cog(Utilitys(bot))

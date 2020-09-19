from discord import Guild
from discord.ext.commands import Cog, Bot, command, Context
from dispander import dispand, compose_embed
from Cogs.app import table, make_embed as me


class Utility(Cog):
    """
    ちょっとした便利機能
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=["ピン留め", "ピン", "ぴんどめ"], description="ぴんどめ表示")
    async def pins(self, ctx: Context):
        pins = await ctx.channel.pins()
        if pins:
            for ms in pins:
                await ctx.send(embed=(compose_embed(ms)))
        else:
            myembed = me.MyEmbed(ctx)
            myembed.default_embed(title='ピン留め表示',
                                  description="**このチャンネルにピン留めは無い様(*ﾟ∀ﾟ)ゞﾃﾞｼ**")

    @command(aliases=["ロールメンバー", "ろーるめんばー",
                      "rm"], description="ロールメンバ表示")
    async def rolemember(self, ctx: Context, name: str):
        g = ctx.guild
        opt = me.MyEmbed(ctx)
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


def setup(bot):
    return bot.add_cog(Utility(bot))

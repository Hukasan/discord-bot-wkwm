from discord import Guild
from discord.ext.commands import Cog, Bot, command, Context
from dispander import dispand, compose_embed
from Cogs.app.MakeEmbed import MakeEmbed


class Utility(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=["ピン留め", "ピン", "ぴんどめ"], description="ぴんどめ表示")
    async def pins(self, ctx: Context):
        for ms in await ctx.channel.pins():
            await ctx.send(embed=(compose_embed(ms)))

    @command(aliases=["ロールメンバー", "ろーるめんばー",
                      "rm"], description="ロールメンバ表示")
    async def rolemember(self, ctx: Context, name: str):
        g = Guild
        g = ctx.guild
        opt = MakeEmbed(ctx)
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

from discord import Guild, CategoryChannel, VoiceChannel
from discord.ext.tasks import loop
from discord.ext.commands import Cog, Bot, command, Context, group
from dispander import dispand, compose_embed
from Cogs.app import table, make_embed as me, mymethods as mm, role_checker as ac
import re


class Utilitys(Cog):
    """
    ちょっとした便利機能
    """

    qualified_name = "おまけ機能"

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
            myembed.default_embed(
                title="ピン留め表示", description="**このチャンネルにピン留めは無い様(*ﾟ∀ﾟ)ゞﾃﾞｼ**"
            )

    @command(aliases=["s", "さーち", "サーチ", "ロール検索"], description="ロールメンバ表示")
    async def serch(self, ctx: Context, name: str):
        g = ctx.guild
        opt = me.MyEmbed(ctx)
        opt.default_embed(title=f'SerchRole"{name}"', mention_author=True)
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
    return bot.add_cog(Utilitys(bot))

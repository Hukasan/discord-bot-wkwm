from discord import Embed, Member, AuditLogAction, User, Message, Emoji
from discord.ext.commands import Cog, Bot, Context
from Cogs.app import table, make_embed as me, extentions

EMBED1_IDENTIFIER = "W_CONCENT"
EMBED2_IDENTIFIER = "W_THANKS"


class Welcome(Cog):
    qualified_name = "ウェルカムメッセージ"

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        if member.bot:
            return
        welcome_room = self.bot.get_channel(
            int(self.bot.config[str(member.guild.id)]["channel_ids"]["welcome"])
        )
        if welcome_room:
            opt = me.MyEmbed().setTarget(target=welcome_room, bot=self.bot)
            oyakusoku = (
                "```無許可の宣伝‍\r他人を傷付ける発言```は禁止です他でおやりなさい🙅‍\r同意されたら↓貴方のBananaをpush!"
            )
            opt.default_embed(
                header="はじめまして、ボットです",
                header_icon=True,
                description="ようこそ猿sのディスコード鯖へ🍌",
                footer="入る前に",
                footer_arg=EMBED1_IDENTIFIER,
            )
            opt.add(name="注意事項🤞", value=oyakusoku)
            await opt.sendEmbed(
                greeting="ようこそ！",
                mention=str(member.mention),
                dust=False,
                bottoms="🍌",
            )
        else:
            raise extentions.GetDatafromDiscordError(
                f"Welcomeチャンネルオブジェクトの取得に失敗しました。\r登録しているIDを確認してください({self.welcome_room_id})"
            )


async def era_welcome1(bot: Bot, usr_id: int, ctx: Context, react: Emoji, arg: list):
    nozoki_role = ctx.guild.get_role(
        (int(bot.config[str(ctx.guild.id)]["role_ids"]["nozoki"]))
    )
    member = ctx.guild.get_member(usr_id)
    usr = bot.get_user(usr_id)
    embed = me.MyEmbed().setTarget(target=ctx.channel, bot=bot)
    if bool(nozoki_role) & bool(member):
        if str(react) == "🍌":
            if usr in ctx.message.mentions:
                await member.add_roles(nozoki_role)
                await ctx.message.delete()
                invite = bot.config[str(ctx.guild.id)].get("rules_channel")
                desc_r = str()
                if invite:
                    desc_r = f"サーバの詳細はこちらで確認ください\r{invite}"
                embed.default_embed(
                    header_icon=ctx.guild.icon_url,
                    header="有難うございますd(ﾟДﾟ )",
                    footer="ありがとうめっせいじ",
                    footer_arg=EMBED2_IDENTIFIER,
                    description=f"\r公開チャンネルが見れるようになりました\r☆-(ノﾟДﾟ)八(ﾟДﾟ　)ノｲｴｰｲ\r{desc_r}",
                )
                await embed.sendEmbed(
                    bottoms=["☑"],
                    greeting=f"{usr.mention}",
                    dust=False,
                )
    else:
        raise extentions.GetDatafromDiscordError(
            f"Nozokiロールオブジェクトの取得に失敗しました。\r登録しているIDを確認してください({int(bot.config[str(ctx.guild.id)]['role_ids']['nozoki'])})"
        )


async def era_welcome2(bot: Bot, usr_id: int, ctx: Context, react: Emoji, arg: list):
    usr = bot.get_user(usr_id)
    if usr in ctx.message.mentions:
        if str(react) == "☑":
            await ctx.message.delete()


def setup(bot):
    bot.config["funcs"].update(
        {
            EMBED1_IDENTIFIER: era_welcome1,
            EMBED2_IDENTIFIER: era_welcome2,
        }
    )
    return bot.add_cog(Welcome(bot))

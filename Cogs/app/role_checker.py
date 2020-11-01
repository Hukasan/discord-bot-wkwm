from discord import (
    Embed,
    Member,
    Reaction,
    RawReactionActionEvent,
    TextChannel,
    Message,
    Emoji,
    Guild,
    Role,
    User,
)
from discord.ext.commands import Cog, Bot, Context, check
from discord.abc import GuildChannel, PrivateChannel


async def isroleupper(role_id: int, user: User, ignore_same=True) -> bool:
    """
    check
    ユーザがそのロールを超えるロールを持っているかどうかを判断します
    """
    guild = Guild
    guild = user.guild
    member = guild.get_member(user_id=int(user.id))
    comp_role = guild.get_role(int(role_id))
    guild_role_list = list()
    guild_role_list = await guild.fetch_roles()
    comp_index = guild_role_list.index(comp_role)
    print(comp_index, guild_role_list.index(member.top_role))
    print(comp_role, member.top_role)
    if comp_index < guild_role_list.index(member.top_role):
        return True
    elif (comp_index == guild_role_list.index(member.top_role)) & (bool(ignore_same)):
        return True
    else:
        return False


def check_role_is_upper_member():
    """
    権限ロール以上のロールをユーザが持っているかを判定
    """

    async def predicate(ctx: Context):
        return await isroleupper(role_id=ctx.bot.config["wkwm"]["ministar_role_id"], user=ctx.author)

    return check(predicate)

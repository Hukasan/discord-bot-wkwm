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
from discord.ext.commands import Cog, Bot, Context
from discord.abc import GuildChannel, PrivateChannel


async def isroleupper(role_id: int, user: User, ignore_same=True) -> bool:
    """
    check
    ユーザがそのロールを超えるロールを持っているかどうかを判断します
    """
    guild = Guild
    guild = user.guild
    print(user.id)
    member = guild.get_member(user_id=int(user.id))
    print(member)
    comp_role = guild.get_role(int(role_id))
    guild_role_list = list()
    guild_role_list = await guild.fetch_roles()
    comp_index = guild_role_list.index(comp_role)
    if (comp_index <= guild_role_list.index(member.top_role)) & (bool(ignore_same)):
        return True
    elif (comp_index < guild_role_list.index(member.top_role)) & (not (bool(ignore_same))):
        return True

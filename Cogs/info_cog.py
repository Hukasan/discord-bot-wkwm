from discord.ext.tasks import loop
from discord import Guild, utils
from discord.ext.commands import (
    Cog,
    Bot,
    Context,
    command,
    is_owner,
    Group,
    Command,
    group,
)
from Cogs.app import table, make_embed as me, role_checker as ac, mymethods as mm
import re


class DispInfo_Settings(Cog):
    """
    ServerInfoカテゴリに表示
    """

    qualified_name = "サーバ情報表示"

    def __init__(self, bot: Bot):
        self.bot = bot
        self.channel_name_all = "全体人数"
        self.repatter_all = re.compile(pattern=f"{self.channel_name_all}:.*")

    @group(description="サーバ情報表示設定")
    @ac.check_role_is_upper_member()
    async def info(self, ctx):
        """
        サーバ情報をチャンネル名として表示するカテゴリを生成、更新します
        """
        if ctx.invoked_subcommand is None:
            raise Exception("trigger is a required argument that is missing.")

    @info.command(aliases=["update", "u", "あっぷでーと"])
    async def info_update(self, ctx):
        await self.update()

    @info.command()
    async def addrole(self, ctx: Context, id):
        if ctx.guild.get_role(int(id)):
            roles = list()
            roles = self.bot.config[str(ctx.guild.id)]["role_ids"]["server_info_scopes"]
            if roles:
                roles.append(int(id))
                self.bot.config[str(ctx.guild.id)]["role_ids"][
                    "server_info_scopes"
                ] = roles
            else:
                self.bot.config[str(ctx.guild.id)]["role_ids"]["server_info_scopes"] = [
                    int(id)
                ]
            await ctx.send("追加いず、さくせすъ(ﾟДﾟ)")

        await self.update()

    async def loop_start(self):
        await self.loop_update.start()

    @loop(seconds=10.0)
    async def loop_update(self):
        await self.update()

    async def update(self):
        server = Guild
        # category = CategoryChannel
        # channel = VoiceChannel
        category = None
        scope_roles = dict()
        category_name = "SERVER_INFO"
        reason = "server_info_setup"
        servers = self.bot.guilds

        for server in servers:
            channel_name_all = f"{self.channel_name_all}: {server._member_count} 人"
            config = self.bot.config.get(str(server.id))
            if config:
                role_ids = config.get("role_ids")
                nozoki_role_id = role_ids.get("nozoki")
                if nozoki_role_id:
                    nozoki_role_id = int(nozoki_role_id)
                    if server.get_role(nozoki_role_id):
                        scope_roles.update({(server.get_role(nozoki_role_id)): "👀"})
                member_role_id = role_ids.get("member")
                if member_role_id:
                    member_role_id = int(member_role_id)
                    if server.get_role(member_role_id):
                        scope_roles.update({(server.get_role(member_role_id)): "🐒"})
                ministar_role_id = role_ids.get("ministar")
                if ministar_role_id:
                    ministar_role_id = int(ministar_role_id)
                    if server.get_role(ministar_role_id):
                        scope_roles.update({(server.get_role(ministar_role_id)): "🌟"})
                scopes = role_ids.get("server_info_scopes")
                if scopes:
                    for scope_role_id in scopes:
                        if server.get_role(int(scope_role_id)):
                            scope_roles.update(
                                {(server.get_role(int(scope_role_id))): "🧻"}
                            )
            for temp in server.by_category():
                if temp[0]:
                    if temp[0].name == category_name:
                        category = temp[0]
                        break
            flag_all = False
            flag_roles = dict()
            if category:
                for channel, islast in mm.lastone(category.voice_channels):
                    if flag_all:
                        pass
                    elif bool(channel):
                        if self.repatter_all.match(string=channel.name):
                            await channel.edit(name=channel_name_all)
                            flag_all = True
                    if (not (bool(flag_all))) & islast:
                        await server.create_voice_channel(
                            category=category, name=channel_name_all, reason=reason
                        )
                    for scope_role in scope_roles.keys():
                        channel_name_role = f"{scope_roles.get(scope_role)}{scope_role.name}: {len(scope_role.members)} 人"
                        repatter_role = re.compile(
                            pattern=f"{scope_roles.get(scope_role)}{scope_role.name}:.*"
                        )
                        if flag_roles.get(scope_role.id):
                            pass
                        elif bool(channel):
                            if repatter_role.match(string=channel.name):
                                await channel.edit(name=channel_name_role)
                                flag_roles.update({scope_role.id: True})
                        if islast & (not (bool(flag_roles.get(scope_role.id)))):
                            await server.create_voice_channel(
                                category=category, name=channel_name_role, reason=reason
                            )
            else:
                await server.create_category(
                    name=category_name, reason=reason, position=1
                )
        pass


def setup(bot):
    return bot.add_cog(DispInfo_Settings(bot))

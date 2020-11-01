from discord import Guild, CategoryChannel, VoiceChannel
from discord.ext.tasks import loop
from discord.ext.commands import Cog, Bot, command, Context, group
from dispander import dispand, compose_embed
from Cogs.app import table, make_embed as me, mymethods as mm, role_checker as ac
import re


class Utility(Cog):
    """
    ちょっとした便利機能
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.channel_name_all = "全体人数"
        self.repatter_all = re.compile(pattern=f"{self.channel_name_all}:.*")

    @Cog.listener()
    async def on_ready(self):
        await self.loop_info_update.start()

    @group()
    @ac.check_role_is_upper_member()
    async def info(self, ctx):
        """
        ・親コマンドです、サブコマンドを指定してください。
        ・指定ロール以上のみ使えます。※設定は、
        **?help setting**　で確認ください
        """
        if ctx.invoked_subcommand is None:
            raise Exception("trigger is a required argument that is missing.")

    @info.command()
    async def add_role(self, ctx: Context, id):
        if ctx.guild.get_role(int(id)):
            roles = list()
            roles = self.bot.config[str(ctx.guild.id)]["server_info_scope_role_ids"]
            if roles:
                self.bot.config[str(ctx.guild.id)]["server_info_scope_role_ids"] = roles.append(int(id))
            else:
                self.bot.config[str(ctx.guild.id)]["server_info_scope_role_ids"] = [int(id)]
            await ctx.send("追加いず、さくせすъ(ﾟДﾟ)")
        await self.update_server_info()

    @loop(minutes=60.0)
    async def loop_info_update(self):
        await self.update_server_info()

    async def update_server_info(self):
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
            if self.bot.config.get(str(server.id)):
                member_role_id = int(self.bot.config[str(server.id)].get("member_role_id"))
                nozoki_role_id = int(self.bot.config[str(server.id)].get("nozoki_role_id"))
                ministar_role_id = int(self.bot.config[str(server.id)].get("ministar_role_id"))
                scope_role_ids = self.bot.config[str(server.id)].get("server_info_scope_role_ids")
                if nozoki_role_id:
                    if server.get_role(nozoki_role_id):
                        scope_roles.update({(server.get_role(nozoki_role_id)): "👀"})
                if member_role_id:
                    if server.get_role(member_role_id):
                        scope_roles.update({(server.get_role(member_role_id)): "🐒"})
                if ministar_role_id:
                    if server.get_role(ministar_role_id):
                        scope_roles.update({(server.get_role(ministar_role_id)): "🌟"})
                if scope_role_ids:
                    for scope_role_id in scope_role_ids:
                        if server.get_role(int(scope_role_id)):
                            scope_roles.update({(server.get_role(int(scope_role_id))): "🧻"})

            for temp in server.by_category():
                if temp[0]:
                    if temp[0].name == category_name:
                        category = temp[0]
                        break
            if category:
                flag_all = False
                flag_roles = dict()
                for channel, islast in mm.lastone(category.voice_channels):
                    if flag_all:
                        pass
                    elif bool(channel):
                        if self.repatter_all.match(string=channel.name):
                            await channel.edit(name=channel_name_all)
                            flag_all = True
                    if (not (bool(flag_all))) & islast:
                        await server.create_voice_channel(category=category, name=channel_name_all, reason=reason)
                    for scope_role in scope_roles.keys():
                        channel_name_role = (
                            f"{scope_roles.get(scope_role)}{scope_role.name}: {len(scope_role.members)} 人"
                        )
                        repatter_role = re.compile(pattern=f"{scope_roles.get(scope_role)}{scope_role.name}:.*")
                        if flag_roles.get(scope_role.id):
                            pass
                        elif bool(channel):
                            if repatter_role.match(string=channel.name):
                                await channel.edit(name=channel_name_role)
                                flag_roles.update({scope_role.id: True})
                        if islast & (not (bool(flag_roles.get(scope_role.id)))):
                            await server.create_voice_channel(category=category, name=channel_name_role, reason=reason)
            else:
                await server.create_category(name=category_name, reason=reason, position=1)
        pass

    @command(aliases=["ピン留め", "ピン", "ぴんどめ"], description="ぴんどめ表示")
    async def pins(self, ctx: Context):
        pins = await ctx.channel.pins()
        if pins:
            for ms in pins:
                await ctx.send(embed=(compose_embed(ms)))
        else:
            myembed = me.MyEmbed(ctx)
            myembed.default_embed(title="ピン留め表示", description="**このチャンネルにピン留めは無い様(*ﾟ∀ﾟ)ゞﾃﾞｼ**")

    @command(aliases=["s", "さーち", "サーチ", "ロール検索"], description="ロールメンバ表示")
    async def serch(self, ctx: Context, name: str):
        g = ctx.guild
        opt = me.MyEmbed(ctx)
        await opt.default_embed(title=f'SerchRole"{name}"')
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

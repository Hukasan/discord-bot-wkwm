import discord
from discord.ext.commands import Cog, Bot, Context, HelpCommand, command, is_owner, Group, Command
from Cogs.app.MakeEmbed import MakeEmbed


@is_owner()
@command(aliases=["re", "lode", "l"], description="プログラムを再読み込み")
async def load(ctx: Context):
    bot = ctx.bot
    for extension in list(bot.extensions):
        print(f"{extension}　is　reloted")
        bot.reload_extension(f"{extension}")
    print("再読み込み完了")
    await ctx.message.add_reaction("☑")


class Help(HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category = "Main"
        self.command_attrs["description"] = "このメッセージを表示"
        self.command_attrs["help"] = "このBOTのヘルプコマンドです。"
        self.command_attrs["aliases"] = ["ヘルプ", "へるぷ", 'h', 'ｈ']

    async def create_category_tree_method(self, cmd, index=0) -> str:
        """
        再帰関数。groupの最下層までを探索する
        """
        try:
            await cmd.can_run(self.context)
        except BaseException:
            print(f"例外:{cmd.name}")
            return''
        content = str()
        temp = str()
        underber_p = int()
        name = str()
        if 0 >= index:
            pass
        else:
            indent = (index) * "\t"
            underber_p = cmd.name.rfind('_')
            if underber_p:
                name = cmd.name[underber_p + 1:]
            content = f"{indent}**{name}** : {cmd.description}\n"
        if isinstance(cmd, Group):
            for subcmd in cmd.walk_commands():
                if not(subcmd.name == temp):
                    content += await self.create_category_tree_method(
                        cmd=subcmd, index=(index + 1))
                temp = subcmd.name
            return content
        elif isinstance(cmd, Command):
            return content

    async def send_bot_help(self, mapping):
        opt = MakeEmbed(self.context)
        await opt.default_embed(header_icon=True, header='Command List', footer=True)
        if self.context.bot.description:
            opt.config['description'] = f"{self.context.bot.description}"
        for cog in mapping:
            if cog:
                cog_name = cog.qualified_name
            else:
                cog_name = self.no_category

            command_list = await self.filter_commands(mapping[cog], sort=True)
            content = str()
            if command_list:
                command_list = set(command_list)
                for cmd in command_list:
                    content += f"**{self.context.prefix}{cmd.name}**\n--{cmd.description}\n"
                opt.add(name=f"> {cog_name}", value=content,
                        inline=False)
        await opt.sendEmbed()

    async def send_cog_help(self, cog: Cog):
        mem = MakeEmbed(self.context)
        temp = str()
        await mem.default_embed(title=f"{cog.qualified_name}カテゴリ",
                                description=f"{cog.description}", footer=True)
        for cmd in cog.walk_commands():
            if (temp != cmd.name) & (not (cmd.root_parent)):
                temp = cmd.name
                mem.add(name=f"> ${cmd.name}", value=f"{cmd.description}\r{await self.create_category_tree_method(cmd=cmd)}")
        await mem.sendEmbed()

    async def send_group_help(self, group):
        mem = MakeEmbed(self.context)
        await mem.default_embed(
            title=f"{self.context.prefix}{group.qualified_name}",
            description=group.description, footer=True)
        if group.aliases:
            mem.add(name="__別の呼び出し方__", value="`" +
                    "`, `".join(group.aliases) + "`", inline=False)
        if group.help:
            mem.add(name="__詳細__",
                    value=group.help, inline=False)
        mem.add(name="> サブコマンド :", value=await self.create_category_tree(group, "```"), inline=False)
        await mem.sendEmbed()

    async def send_command_help(self, command):
        params = "} {".join(command.clean_params.keys())
        params = '{' + params + '}'
        embed = discord.Embed(
            title=f"{self.context.prefix}{command.qualified_name} {params}",
            description=command.description,
            color=0x00ff00)
        if command.aliases:
            embed.add_field(name="__別の呼び出し方__", value="`" +
                            "`, `".join(command.aliases) + "`", inline=False)
        if command.help:
            embed.add_field(name="__詳細__",
                            value=command.help, inline=False)
        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(
            title="ヘルプ表示エラー", description=error, color=0xff0000)
        await self.get_destination().send(embed=embed)

    async def command_not_found(self, string):
        return f"{string} というコマンドは存在しません。"

    def subcommand_not_found(self, command, string):
        if isinstance(
                command, Group) and len(
                command.all_commands) > 0:
            # もし、そのコマンドにサブコマンドが存在しているなら
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"


def setup(bot: Bot):
    bot.help_command = Help()
    bot.add_command(load)

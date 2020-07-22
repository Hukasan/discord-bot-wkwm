import discord
from discord.ext import commands


@commands.command(description="プログラムを再読み込みします")
async def relode(ctx: commands.Context):
    bot = ctx.bot
    for extension in list(bot.extensions):
        print(f"{extension}isreloted")
        bot.reload_extension(f"{extension}")
    await ctx.send("再読み込み完了")


class Help(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category = "基本コマンド"
        self.command_attrs["description"] = "このメッセージを表示します。"
        self.command_attrs["help"] = "このBOTのヘルプコマンドです。"

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
        if 0 == index:
            content = f"${cmd.name}:{cmd.description}\n"
        else:
            indent = (index+1)*"\t"
            content = f"{indent}- {cmd.name}:{cmd.description}\n"
        if isinstance(cmd, commands.Group):
            for subcmd in cmd.walk_commands():
                if not(subcmd.name == temp):
                    content += await self.create_category_tree_method(
                        cmd=subcmd, index=(index + 1))
                temp = subcmd.name
            return content
        elif isinstance(cmd, commands.Command):
            return content

    async def create_category_tree(self, category, enclosure):
        """
        コマンドの集まり（Group、Cog）から木の枝状のコマンドリスト文字列を生成する。
        生成した文字列は enlosure 引数に渡された文字列で囲われる。
        """

        content = ""
        parent = "NULL"
        command_list = list(category.walk_commands())
        for cmd in command_list:
            if not(cmd.root_parent):
                content += await self.create_category_tree_method(cmd=cmd)
        min_level = float("inf")
        adjusted_content = ""

        for line in content.split("\n"):
            # 各行のインデントを、最も浅いレベルまで削る
            if not line:
                # 空行は削る必要がないので、無視
                continue
            level = 0  # その行のインデントレベル
            for char in line:
                if char == "\t":
                    level += 1
                else:
                    break
            if level < min_level:
                min_level = level
        if min_level == 0:
            # 無駄なインデントは無かったので、削る必要もない
            adjusted_content = content
        else:
            for line in content.split("\n"):
                if not line.startswith("\t"):
                    adjusted_content += line + "\n"
                    continue
                adjusted_content += "".join(line.split("\t" *
                                                       min_level)[1:]) + "\n"
        return enclosure + adjusted_content + enclosure

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="コマンド一覧", color=0x00ff00)
        if self.context.bot.description:
            # もしBOTに description 属性が定義されているなら、それも埋め込みに追加する
            embed.description = self.context.bot.description
        for cog in mapping:
            if cog:
                cog_name = cog.qualified_name
            else:
                # mappingのキーはNoneになる可能性もある
                # もしキーがNoneなら、自身のno_category属性を参照する
                cog_name = self.no_category

            command_list = await self.filter_commands(mapping[cog], sort=True)
            content = ""
            for cmd in command_list:
                content += f"`{self.context.prefix}{cmd.name}`\n {cmd.description}\n"
            embed.add_field(name=cog_name, value=content, inline=False)

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.qualified_name,
                              description=cog.description, color=0x00ff00)
        embed.add_field(name="__CommandList__", value=await self.create_category_tree(cog, "```"))
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=f"{self.context.prefix}{group.qualified_name}",
                              description=group.description, color=0x00ff00)
        if group.aliases:
            embed.add_field(name="__AnotherCall__", value="`" +
                            "`, `".join(group.aliases) + "`", inline=False)
        if group.help:
            embed.add_field(name="__HelpText__",
                            value=group.help, inline=False)
        embed.add_field(name="*サブコマンド:*", value=await self.create_category_tree(group, "```"), inline=False)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        params = " ".join(command.clean_params.keys())
        embed = discord.Embed(title=f"__{self.context.prefix}{command.qualified_name} {params}__",
                              description=command.description, color=0x00ff00)
        if command.aliases:
            embed.add_field(name="__AnotherCall__", value="`" +
                            "`, `".join(command.aliases) + "`", inline=False)
        if command.help:
            embed.add_field(name="__HelpText__",
                            value=command.help, inline=False)
        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(
            title="ヘルプ表示エラー", description=error, color=0xff0000)
        await self.get_destination().send(embed=embed)

    async def command_not_found(self, string):
        await self.get_destination().send(embed=embed)  # noqa

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            # もし、そのコマンドにサブコマンドが存在しているなら
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"


def setup(bot: commands.Bot):
    bot.help_command = Help()
    bot.add_command(relode)

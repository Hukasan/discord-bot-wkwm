import discord
from discord.ext import commands
from TalkIOCog import TalkIO  # noqa
# from test import MusicCog


class Help(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category = "カテゴリ未設定"
        self.command_attrs["description"] = "このメッセージを表示します。"
        self.command_attrs["help"] = "このBOTのヘルプコマンドです。"

    def export_map_byindex(self, index):
        pass

    async def create_category_tree(self, category, enclosure):
        """
        コマンドの集まり（Group、Cog）から木の枝状のコマンドリスト文字列を生成する。
        生成した文字列は enlosure 引数に渡された文字列で囲われる。
        """
        content = ""
        cmddict = {}
        parent = "NULL"
        indexs = []
        command_list = category.walk_commands()
        for cmd in command_list:
            if cmd.root_parent:
                index = cmd.parents.index(cmd.root_parent)
                if ((index + 1) * '\t'):
                    if cmd.root_parent.name in cmddict.keys():
                        if index in cmddict[cmd.root_parent.name]["subcmds"].keys():
                            cmddict[cmd.root_parent.name]["subcmds"][index].update({
                                cmd.name: cmd.description})
                        else:
                            cmddict[cmd.root_parent.name]["subcmds"].update({index: {
                                cmd.name: cmd.description}})
                    else:
                        cmddict[cmd.root_parent.name] = {"subcmds": {index: {
                            cmd.name: cmd.description}}}
                else:
                    if cmd.name in cmddict.keys():
                        cmddict[cmd.name]["desc"] = cmd.description
                    else:
                        cmddict[cmd.name] = {"desc": cmd.description}
            else:
                if cmd.name in cmddict.keys():
                    cmddict[cmd.name]["desc"] = cmd.description
                else:
                    cmddict[cmd.name] = {
                        "desc": cmd.description, "subcmds": {}}
        for parent in cmddict.keys():
            content += f"{self.context.prefix}{parent} / {cmddict[parent]['desc']}\n"
            if "subcmds" in cmddict[parent].keys():
                a = sorted(cmddict[parent]["subcmds"].items(),
                           key=lambda x: x[0])
                for b in a:
                    indexs.append(b[0])
                if indexs:
                    for i in range(len(indexs)):
                        subcmds = sorted(
                            cmddict[parent]["subcmds"][indexs[i]].items(), key=lambda x: x[0])
                        for subcmd in subcmds:
                            indent = "\t" * (indexs[i])
                            content += f"{indent} - {subcmd[0]} / {subcmd[1]}\n"
            indexs = []
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
        print(enclosure + adjusted_content + enclosure)
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
        embed.add_field(name="CommandList：", value=await self.create_category_tree(cog, "```"))
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=f"{self.context.prefix}{group.qualified_name}",
                              description=group.description, color=0x00ff00)
        if group.aliases:
            embed.add_field(name="AnotherCall：", value="`" +
                            "`, `".join(group.aliases) + "`", inline=False)
        if group.help:
            embed.add_field(name="HelpText：", value=group.help, inline=False)
        embed.add_field(name="SubCommandText：", value=await self.create_category_tree(group, "```"), inline=False)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        params = " ".join(command.clean_params.keys())
        embed = discord.Embed(title=f"{self.context.prefix}{command.qualified_name} {params}",
                              description=command.description, color=0x00ff00)
        if command.aliases:
            embed.add_field(name="AnotherCall：", value="`" +
                            "`, `".join(command.aliases) + "`", inline=False)
        if command.help:
            embed.add_field(name="HelpText：", value=command.help, inline=False)
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


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="$", help_command=Help(),
                       description="試験用botです")
    # bot.add_cog(AddminCog(bot))
    # bot.add_cog(MusicCog(bot))
    bot.add_cog(TalkIO(bot))
    bot.run("NzEyMTk4NDE2MjY4MjYzNDg1.XtYkiA.ZiJsdgSV_a6GQneweEOrmuj8BF8")

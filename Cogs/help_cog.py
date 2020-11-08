from discord import Embed
from discord.ext.commands import (
    Cog,
    Bot,
    Context,
    HelpCommand,
    is_owner,
    Group,
    Command,
)
from Cogs.app import table, make_embed as me


class Help(HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category_name = "Help"  # カテゴリが見つからなかった場合のカテゴリ
        self.command_attrs["description"] = "このメッセージを表示"
        self.command_attrs["help"] = "このBOTのヘルプコマンドです。"
        self.command_attrs["aliases"] = ["ヘルプ", "へるぷ", "h", "ｈ", "コマンド", "こまんど", "cmd"]
        self.dfembed = me.MyEmbed().default_embed(
            mention_author=True,
            header_icon=True,
            footer="操作ガイド",
            footer_arg="h-p",
            time=False,
        )
        self.counts = [
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟",
        ]

    async def create_category_tree(self, cmd, index=int(0)) -> str:
        """
        再帰関数。groupの最下層までを探索する
        """
        try:
            await cmd.can_run(self.context)
        except BaseException:
            print(f"例外:{cmd.name}")
            return ""
        content = str()
        temp = str()
        underber_p = int()
        name = str()
        if 0 >= index:
            pass
        else:
            indent = (index) * "\t"
            underber_p = cmd.name.rfind("_")
            if underber_p:
                name = cmd.name[(underber_p + 1) :]
            content = f"{indent}**{name}** : {cmd.description}\n"
        if isinstance(cmd, Group):
            for subcmd in cmd.walk_commands():
                if not (subcmd.name == temp):
                    content += await self.create_category_tree(
                        cmd=subcmd, index=(index + 1)
                    )
                temp = subcmd.name
            return content
        elif isinstance(cmd, Command):
            return content

    async def send_bot_help(self, mapping):
        content = str()
        count = 1
        for cog in mapping:
            cog_name = cog.qualified_name if cog else self.no_category_name
            if (cog_name == "Help") | (cog_name == "hide"):
                continue
            # command_list = await self.filter_commands(mapping[cog], sort=True)
            # content = str()
            # if command_list:
            #     command_list = set(command_list)
            #     for cmd in command_list:
            #         content += (
            #             f"**{self.context.prefix}{cmd.name}**\n--{cmd.description}\n"
            #         )
            # for temp in cog.walk_commands():
            #     opt.add(
            #         name=f":{str(counts.pop(-1))}:{cog_name}",
            #         value=cog.description,
            #         inline=False,
            #     )
            #     break
            # content += f"> :{str(counts.pop(-1))}:**{cog_name}**\r"
            content += f"**{str(count)}.{cog_name}**\r"
            count += 1
        # opt = me.MyEmbed
        opt = self.dfembed.clone(self.context)
        opt.change(
            header="ℹ機能説明",
            thumbnail=True,
            desc=(
                f"{self.context.bot.description}\n"
                f"**{self.context.prefix}help**\n--{self.command_attrs['description']}\n"
            ),
            bottums_sub=self.counts[: (count - 1)],
        )
        opt.description = opt.description + content
        await opt.sendEmbed()

    async def send_cog_help(self, cog: Cog):
        embed = me.MyEmbed(self.context)
        temp = str()
        embed.default_embed(
            title=f"{cog.qualified_name}",
            description=f"{cog.description}",
            time=False,
        )
        for cmd in cog.walk_commands():
            if (temp != cmd.name) & (not (cmd.root_parent)):
                temp = cmd.name
                embed.add(
                    name=f"> ${cmd.name}",
                    value=f"{cmd.description}\r{await self.create_category_tree(cmd=cmd)}",
                )
        await embed.sendEmbed()

    async def send_group_help(self, group):
        embed = me.MyEmbed(self.context)
        await embed.default_embed(
            title=f"{self.context.prefix}{group.qualified_name}",
            description=group.description,
            footer="#ヘルプ",
            time=False,
        )
        if group.aliases:
            embed.add(
                name="__別の呼び出し方__",
                value="`" + "`, `".join(group.aliases) + "`",
                inline=False,
            )
        if group.help:
            embed.add(name="__詳細__", value=group.help, inline=False)
        embed.add(
            name="__サブコマンド__",
            value=await self.create_category_tree(group),
            inline=False,
        )
        await embed.sendEmbed(greeting=f"{self.context.author.mention}")

    async def send_command_help(self, command):
        params = "} {".join(command.clean_params.keys())
        params = "{" + params + "}"
        embed = me.MyEmbed(self.context)
        desc = str()
        if params:
            desc = "{}内は要素指定です。"
        await embed.default_embed(
            title="コマンドヘルプ",
            description="**" + command.name + "**",
            time=False,
            footer=f"[{self.context.prefix}help send_command_help] {command.qualified_name}",
        )
        embed.add(
            name="__利用方法__",
            value=(
                f"**{self.context.prefix}{command.qualified_name} {params}**\r" + desc
            ),
        )
        if command.help:
            embed.add(name="__詳細__", value=command.help, inline=False)
        if command.aliases:
            embed.add(
                name="__別の呼び出し方__",
                value="`" + "`, `".join(command.aliases) + "`",
                inline=False,
            )
        await embed.sendEmbed(greeting=f"{self.context.author.mention}")

    async def send_error_message(self, error):
        embed = me.MyEmbed(self.context)
        embed.default_embed(
            header="ヘルプエラー", title="help対象が見つかりませんでした", description="入力を確認してもう一度お試しあれ"
        )
        await embed.sendEmbed(greeting=f"{self.context.author.mention}")

    def subcommand_not_found(self, command, string):
        if isinstance(command, Group) and len(command.all_commands) > 0:
            # もし、そのコマンドにサブコマンドが存在しているなら
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"


def setup(bot: Bot):
    bot.help_command = Help()

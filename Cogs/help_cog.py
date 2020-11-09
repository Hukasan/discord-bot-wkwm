from discord import Embed, User
from discord.ext.commands import (
    Cog,
    Bot,
    Context,
    HelpCommand,
    is_owner,
    Group,
    Command,
)
from Cogs.app import table, make_embed as me, mymethods as mm


class Help(HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category_name = "Help"  # カテゴリが見つからなかった場合のカテゴリ
        self.command_attrs["description"] = "このメッセージを表示"
        self.command_attrs["help"] = "このBOTのヘルプコマンドです。"
        self.command_attrs["aliases"] = [
            "ヘルプ",
            "へるぷ",
            "h",
            "ｈ",
            "コマンド",
            "こまんど",
            "cmd",
            "へ",
        ]
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
            indent = (index) * "--"
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
        cog_name_list = list()
        cog = Cog
        for cog in mapping:
            cog_name = cog.qualified_name if cog else self.no_category_name
            if (cog_name == "Help") | (cog_name == "hide"):
                continue
            content += f"**{str(count)}.{cog_name}**\r"
            count += 1
            cog_name_list.append(cog.__class__.__name__)
        # opt = me.MyEmbed
        opt = self.dfembed.clone(self.context)
        opt.change(
            header="ℹ機能説明",
            thumbnail=True,
            desc=(
                f"{self.context.bot.description}\n"
                f"先頭文字は **{str(self.context.bot.command_prefix[0])}** です\n"
                f"**{self.context.prefix}help**\n--{self.command_attrs['description']}\n{content}"
            ),
            bottoms_sub=self.counts[: (count - 1)],
            bottom_args=cog_name_list,
        )
        await opt.sendEmbed()

    async def send_cog_help(self, cog: Cog):
        # embed = me.MyEmbed
        embed = self.dfembed.clone(ctx=self.context)
        temp = str()
        mention = str()
        command_name_list = list()
        count = 1
        for cmd in cog.walk_commands():
            if (temp != cmd.name) & (not (cmd.root_parent)):
                temp = cmd.name
                embed.add(
                    name=f"> {count} ${cmd.name}",
                    value=f"{cmd.description}\r{await self.create_category_tree(cmd=cmd)}",
                )
                command_name_list.append(temp)
                count += 1
        embed.change(
            header="ℹカテゴリ説明",
            title=f"{cog.qualified_name}",
            desc=f"{cog.description}",
            bottoms_sub=self.counts[: len(command_name_list)],
            bottom_args=command_name_list,
        )
        botid = (await self.context.bot.application_info()).id
        if self.context.author.id == botid:
            if self.context.bot.config[str(self.context.guild.id)]["help_author"].get(
                self.context.channel.id
            ):
                mention = (
                    self.context.bot.config[str(self.context.guild.id)]["help_author"]
                    .get(self.context.channel.id)
                    .get(cog.__class__.__name__)
                )
        await embed.sendEmbed(mention=mention)

    async def send_group_help(self, group: Group):
        embed = me.MyEmbed
        embed = self.dfembed.clone(ctx=self.context)
        mention = str()
        # value = "`" + "`, `".join(group.aliases) + "`"
        tab = "|"
        value = "以下の言葉でも呼び出し可能です"
        count = 0
        for a, lastone in mm.lastone(group.aliases):
            if lastone:
                value += f"{tab}{a}```"
            elif count % 4 == 0:
                if count == 0:
                    value += f"```{a}"
                    count += 1
                else:
                    value += f"{tab}{a}\r"
            elif count % 4 == 1:
                value += a
            else:
                value += tab + a
            count += 1
        if group.help:
            embed.add(name="詳細", value="```" + group.help + "```", inline=False)
        content = await self.create_category_tree(group)
        print(content)
        embed.add(
            name="> subcommands",
            value=content,
            inline=True,
        )
        if group.aliases:
            embed.add(
                name="> othercall",
                value=value,
                inline=True,
            )
        prefix = (
            self.context.prefix
            if self.context.prefix
            else self.context.bot.command_prefix[0]
        )
        embed.change(
            header="ℹコマンド(親)ヘルプ",
            title=f"{prefix} {group.name} コマンド",
            desc="__親cmdです、サブcmdが必要です__",
        )
        botid = (await self.context.bot.application_info()).id
        if self.context.author.id == botid:
            if self.context.bot.config[str(self.context.guild.id)]["help_author"].get(
                self.context.channel.id
            ):
                mention = (
                    self.context.bot.config[str(self.context.guild.id)]["help_author"]
                    .get(self.context.channel.id)
                    .get(group.name)
                )
        await embed.sendEmbed(mention=mention)

    async def send_command_help(self, command: Command):
        params = "} {".join(command.clean_params.keys())
        params = "{ " + params + " }"
        embed = me.MyEmbed
        embed = self.dfembed.clone(ctx=self.context)
        mention = str()
        desc = str()
        prefix = (
            self.context.prefix
            if self.context.prefix
            else self.context.bot.command_prefix[0]
        )
        embed.change(
            header="コマンドヘルプ",
            title=f"**{prefix}{command.name}**",
        )
        if params:
            desc = "{}の部分に設定したい語句を入れてください"
        embed.add(
            name="・ 利用方法",
            value=(
                f"**{self.context.prefix}{command.qualified_name} {params}**\r" + desc
            ),
        )
        if command.help:
            embed.add(name="・詳細", value=command.help, inline=False)
        if command.aliases:
            embed.add(
                name="> 別の呼び出し方",
                value="`" + "`, `".join(command.aliases) + "`",
                inline=False,
            )
        botid = (await self.context.bot.application_info()).id
        print(self.context.bot.config[str(self.context.guild.id)]["help_author"])
        if self.context.author.id == botid:
            if self.context.bot.config[str(self.context.guild.id)]["help_author"].get(
                self.context.channel.id
            ):
                print("hi")
                mention = (
                    self.context.bot.config[str(self.context.guild.id)]["help_author"]
                    .get(self.context.channel.id)
                    .get(f"{command.full_parent_name} {command.name}")
                )
                print(
                    self.context.bot.config[str(self.context.guild.id)][
                        "help_author"
                    ].get(self.context.channel.id)
                )
        await embed.sendEmbed(mention=mention)

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

"""
このプログラムは完成例です。
"""

import discord
from discord.ext import commands


class Help(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category = "カテゴリ未設定"
        self.command_attrs["description"] = "このメッセージを表示します。"
        self.command_attrs["help"] = "このBOTのヘルプコマンドです。"

    async def create_category_tree(self, category, enclosure):
        """
        コマンドの集まり（Group、Cog）から木の枝状のコマンドリスト文字列を生成する。
        生成した文字列は enlosure 引数に渡された文字列で囲われる。
        """
        content = ""
        command_list = category.walk_commands()
        for cmd in await self.filter_commands(command_list, sort=True):
            if cmd.root_parent:
                # cmd.root_parent は「根」なので、根からの距離に応じてインデントを増やす
                index = cmd.parents.index(cmd.root_parent)
                indent = "\t" * (index + 1)
                if indent:
                    content += f"{indent}- {cmd.name} / {cmd.description}\n"
                else:
                    # インデントが入らない、つまり木の中で最も浅く表示されるのでprefixを付加
                    content += f"{self.context.prefix}{cmd.name} / {cmd.description}\n"
            else:
                # 親を持たないコマンドなので、木の中で最も浅く表示する。prefixを付加
                content += f"{self.context.prefix}{cmd.name} / {cmd.description}\n"

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
        embed = discord.Embed(title="helpコマンド", color=0x00ff00)
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
        embed.add_field(name="コマンドリスト：", value=await self.create_category_tree(cog, "```"))
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=f"{self.context.prefix}{group.qualified_name}",
                              description=group.description, color=0x00ff00)
        if group.aliases:
            embed.add_field(name="有効なエイリアス：", value="`" +
                            "`, `".join(group.aliases) + "`", inline=False)
        if group.help:
            embed.add_field(name="ヘルプテキスト：", value=group.help, inline=False)
        embed.add_field(name="サブコマンドリスト：", value=await self.create_category_tree(group, "```"), inline=False)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        params = " ".join(command.clean_params.keys())
        embed = discord.Embed(title=f"{self.context.prefix}{command.qualified_name} {params}",
                              description=command.description, color=0x00ff00)
        if command.aliases:
            embed.add_field(name="有効なエイリアス：", value="`" +
                            "`, `".join(command.aliases) + "`", inline=False)
        if command.help:
            embed.add_field(name="ヘルプテキスト：", value=command.help, inline=False)
        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(
            title="ヘルプ表示のエラー", description=error, color=0xff0000)
        await self.get_destination().send(embed=embed)

    def command_not_found(self, string):
        return f"{string} というコマンドは存在しません。"

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            # もし、そのコマンドにサブコマンドが存在しているなら
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"


class MusicCog(commands.Cog, name="音楽"):
    """
    音楽機能のカテゴリです。
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(description="BOTをボイスチャンネルに参加させます。")
    async def join(self, ctx, channel: discord.VoiceChannel = None):
        """
        このコマンドを実行すると、実行者のボイスチャンネルにBOTが接続します。
        同じサーバー内の他のボイスチャンネルに既に接続している場合は、BOTが移動します。
        引数にはチャンネル名を渡すことができます。その名前のボイスチャンネルにBOTが接続します。
        """
        pass

    @join.command(aliases=["bye", "dc", "leave"], description="BOTをボイスチャンネルから切断します。")
    async def disconnect(self, ctx):
        """
        BOTの音楽再生を停止し、ボイスチャンネルへの接続を切断するコマンドです。
        このコマンドを実行すると、そのサーバー内のボイスチャンネルにBOTが既に接続していれば、
        そのチャンネルから切断します。
        """
        pass

    @commands.group(aliases=["p"], description="音楽を再生します。")
    async def play(self, ctx):
        """
        音楽を再生するコマンド群です。
        ただし、playのみでは音楽を再生できません。
        youtube もしくは soundcloud サブコマンドを利用してください。
        """
        if ctx.invoked_subcommand is None:
            return

    @play.command(description="youtubeからURLで音楽を再生します。")
    async def youtube(self, ctx, url):
        """
        引数に渡したURLでYoutubeから音楽を再生します。
        動画が見つからなければ、再生できません。
        また、1時間を超える動画も再生できません。
        """
        pass

    @play.command(description="soundcloudから曲名で音楽を再生します。")
    async def soundcloud(self, ctx, title):
        """
        引数に渡したタイトルsoundcloudから音楽を再生します。
        実行すると、検索結果が最大10件まで表示されます。表示された番号を送信して楽曲を選択してください。
        """
        pass


class AdminCog(commands.Cog, name="管理者用"):
    """
    管理者用の機能です。
    管理者権限が無ければ使えません。
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="eval", description="任意のPythonプログラムを実行します。")
    async def eval_(self, ctx, *, cmd):
        """
        BOTの管理者以外はセキュリティ上の問題で使用することができません。
        引数に渡したPythonプログラムを実行します。実行に失敗した場合は例外を出力します。
        """
        pass

    @commands.is_owner()
    @commands.command(aliases=["echo"], description="任意の文章を送信します。")
    async def say(self, ctx, *, word):
        """
        引数に渡した文章を同じチャンネル内に送信します。
        """
        pass


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="!", help_command=Help(),
                       description="ヘルプコマンドの説明用bot")
    bot.add_cog(MusicCog(bot))
    bot.add_cog(AdminCog(bot))

    bot.run("NzEyMTk4NDE2MjY4MjYzNDg1.XtYkiA.ZiJsdgSV_a6GQneweEOrmuj8BF8")

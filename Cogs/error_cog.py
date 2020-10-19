import discord
from discord.ext.commands import (
    Cog,
    Bot,
    Context,
    HelpCommand,
    command,
    is_owner,
    Group,
    Command,
)
from Cogs.app import table, make_embed as me


class OutputError(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner = None
        self.db_cmd = table.Cmdtb()
        self.__error_title = "コマンドエラー"
        self.__error_fotter = ""
        self.__undefine_error_title = "予期せぬエラー"
        self.__notice_owner_message = "おぉん　エラーってるんですけどぉ↓↓"
        self.__missing_arg_message = "そのコマンドに必要な要素指定が足りていません\r" "コマンドの詳細を表示しますか？"
        self.__permission_message = "😢指定されたコマンドを実行する権限が貴方にありません\r必要があれば、管理者まで問い合わせください"

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if not (self.owner):
            self.owner = self.bot.get_user(self.bot.owner_id)
            if self.owner:
                self.__notice_owner_message = self.owner.mention + self.__notice_owner_message
        cmd = str()
        embed = me.MyEmbed(ctx)
        try:
            cmd = ((str(error)).split('"', maxsplit=2))[1]
            result = self.db_cmd.tbselect(cmd)
            if result:
                await ctx.send(result[0].body)
                return
            else:
                dubleq = str(error).split('"')
                await embed.default_embed(footer=self.__error_fotter, title=self.__error_title)
                if dubleq:
                    if dubleq[0] == "Command " and dubleq[2] == " is not found":
                        embed.add(
                            name="無効なコマンド",
                            value=f'コマンドに " {dubleq[1]} " はありませんでした。\r？help コマンドで確認することができます',
                        )
                    else:
                        embed.add(
                            name=self.__undefine_error_title,
                            value=f"```{str(error)}```",
                            greeting=self.__notice_owner_message,
                        )
                else:
                    embed.add(
                        name=self.__undefine_error_title,
                        value=f"```{str(error)}```",
                        greeting=self.__notice_owner_message,
                    )
        except IndexError:
            await embed.default_embed(
                footer=self.__error_fotter,
                title=self.__error_title,
                greeting=f"{ctx.author.mention}",
                time=False,
            )
            if "required argument that is missing." in str(error):
                string = f"{ctx.prefix}{ctx.command}"
                if ctx.invoked_subcommand:
                    string += f" {(ctx.invoked_subcommand).name}"
                embed.change_description(
                    desc=self.__missing_arg_message,
                    arg=f"e-c-h {string}",
                    bottums=["🙆"],
                )
            elif "You do not own this bot." in str(error):
                embed.change_description(self.__permission_message)
            elif "The check functions for command cmd failed." in str(error):
                embed.change_description(self.__permission_message)
            else:
                embed.add(
                    name=self.__undefine_error_title,
                    value=f"```{str(error)}```",
                    greeting=self.__notice_owner_message,
                )
        await embed.sendEmbed()


def setup(bot):
    # return bot.add_cog(OutputError(bot))
    pass

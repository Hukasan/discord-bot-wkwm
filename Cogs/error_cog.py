from discord import Emoji
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

EMBED_IDENTIFIER = "ERROR_CMD_HELP"
E_CH_REACTION_ACCEPT = "🙆"


async def era_e_ch(bot: Bot, usr_id: int, ctx: Context, react: Emoji, arg: list):
    if str(react) == E_CH_REACTION_ACCEPT:
        usr = bot.get_user(usr_id)
        target = arg[1]
        bot.config[str(ctx.guild.id)]["help_author"].update(
            {ctx.channel.id: {target: usr.mention}}
        )
        await ctx.send_help(target)
        await ctx.message.delete()
    else:
        pass


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
                self.__notice_owner_message = (
                    self.owner.mention + self.__notice_owner_message
                )
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
                embed.default_embed(
                    footer=self.__error_fotter, title=self.__error_title
                )
                if dubleq:
                    if dubleq[0] == "Command " and dubleq[2] == " is not found":
                        # await ctx.message.add_reaction("‍🙅‍")
                        await ctx.message.add_reaction("❔")
                        return
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
            embed.default_embed(
                footer=self.__error_fotter,
                title=self.__error_title,
                greeting=f"{ctx.author.mention}",
                time=False,
            )
            if "required argument that is missing." in str(error):
                string = f"{ctx.command}"
                # if ctx.invoked_subcommand:
                #     string = (ctx.invoked_subcommand).name
                # else:
                #     string = f"{ctx.command}"
                embed.change(
                    description=self.__missing_arg_message,
                    footer_arg=f"{EMBED_IDENTIFIER} {string}",
                    bottoms=[E_CH_REACTION_ACCEPT],
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
    bot.config["funcs"].update(
        {
            EMBED_IDENTIFIER: era_e_ch,
        }
    )
    return bot.add_cog(OutputError(bot))
    pass

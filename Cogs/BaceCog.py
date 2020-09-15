import discord
from discord.ext.commands import Cog, Bot, Context, HelpCommand, command, is_owner, Group, Command
from Cogs.app.MakeEmbed import MakeEmbed


class Bace(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.owner = discord.User
        self.owner = self.bot.get_user(self.bot.owner_id)

    @is_owner()
    @command(aliases=["re", "lode", "l"], description="プログラムを再読み込み")
    async def load(self, ctx: Context):
        bot = ctx.bot
        for extension in list(bot.extensions):
            bot.reload_extension(f"{extension}")
            print(f"{extension}_is_reloted")
        print("再読み込み完了")
        await ctx.message.add_reaction("☑")

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        cmd = str()
        mem = MakeEmbed(ctx)
        try:
            cmd = ((str(error)).split('"', maxsplit=2))[1]
            dubleq = str(error).split("\"")
            result = self.db_cmd.tbselect(cmd)
            if result:
                await ctx.send(result[0].body)
            else:
                await mem.default_embed(footer="On_Command_Error", title='コマンドエラー')
                if dubleq:
                    if dubleq[0] == "Command " and dubleq[2] == " is not found":
                        mem.add(
                            name="無効なコマンド",
                            value=f"コマンドに \" {dubleq[1]} \" はありませんでした。\r？help コマンドで確認することができます")
                    else:
                        mem.add(name='予期せぬエラー', value=f":\r```{str(error)}```")
                        mem.greeting = f"{self.owner.mention}エラーってるんですけどぉ"
                else:
                    mem.add(name='予期せぬエラー', value=f":\r```{str(error)}```")
                    mem.greeting = f"{self.owner.mention}エラーってるんですけどぉ"
        except IndexError:
            if "trigger is a required argument that is missing." in str(error):
                await ctx.send("入力する値の数が足りてません\rヘルプを表示します")
                if ctx.invoked_subcommand:
                    await ctx.send_help(ctx.invoked_subcommand)
                elif ctx.command:
                    await ctx.send_help(ctx.command)
            else:
                await mem.default_embed(footer="On_Command_Error", title='コマンドエラー')
                mem.add(name='予期せぬエラー', value=f"```{str(error)}```")
                mem.greeting = f"{self.owner.mention}エラーってるんですけどぉ"
        await mem.sendEmbed()


def setup(bot):
    return Bace(bot)

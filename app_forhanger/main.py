import discord
from discord.ext import commands
import BaseOverwriteCog as boc
from TalkIOCog import TalkIO
import locale

BOTTOKEN = "NzEyMTk4NDE2MjY4MjYzNDg1.XtYkiA.ZiJsdgSV_a6GQneweEOrmuj8BF8"
if __name__ == '__main__':
    print(locale.getpreferredencoding())
    bot = commands.Bot(command_prefix="$", help_command=boc.Help(),
                       description="猿sのバナナ農園の精霊")
    bot.add_cog(TalkIO(bot))
    bot.run(BOTTOKEN)

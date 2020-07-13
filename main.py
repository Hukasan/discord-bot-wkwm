import discord
from discord.ext import commands

import sys
sys.path.append("./app/")
from app.TalkIOCog import TalkIO  # noqa # nopep
from app.BaseOverwriteCog import Help  # noqa # nopep

BOTTOKEN = "NzEyMTk4NDE2MjY4MjYzNDg1.XtYkiA.ZiJsdgSV_a6GQneweEOrmuj8BF8"

if __name__ == '__main__':
    bot = commands.Bot(command_prefix="$", help_command=Help(),
                       description="猿sのバナナ農園の精霊")
    bot.add_cog(TalkIO(bot))
    bot.run(BOTTOKEN)

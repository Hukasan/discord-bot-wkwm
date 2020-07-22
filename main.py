from os import environ
from discord.ext import commands

TOKEN = environ['BOT_ACCESS_TOKEN']  # 環境変数から取得
extensions = []
extensions.append('BaseOverwriteCog')
extensions.append('TalkIOCog')

if __name__ == '__main__':
    bot = commands.Bot(command_prefix="$",
                       description="猿sのバナナ農園の精霊")
    for extension in extensions:
        bot.load_extension(f"app.{extension}")
    bot.run(TOKEN)

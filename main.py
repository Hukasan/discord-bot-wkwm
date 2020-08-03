from os import environ
from discord.ext import commands
import logging

config = {
    'wkwm': {
    }
}

extensions = []
extensions.append('BaseOverwriteCog')
extensions.append('TalKIOCog2')
extensions.append("EventCog")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot = commands.Bot(command_prefix="$",
                       description="猿sのバナナ農園の精霊")
    config["wkwm"]["room_id"] = environ['ROOM_ID']
    bot.config = config
    TOKEN = environ['BOT_ACCESS_TOKEN']  # 環境変数から取得
    for extension in extensions:
        bot.load_extension(f"Cogs.{extension}")
    bot.run(TOKEN)

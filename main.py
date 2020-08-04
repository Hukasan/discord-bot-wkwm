from os import environ
from discord.ext import commands
import logging

config = {
    'wkwm': {
        'welcome_message': '入隊希望などその他申請は各チャンネルへお願いします。\r各受付チャンネルのピン留めに詳細が有ります。\rリアクションを押すとこのチャットは消去されます'
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
    config["wkwm"]["room_id"] = environ['BOT_ROOM_ID']
    config['wkwm']['welcome_room_id'] = 710732615879229481
    config['wkwm']['leave_notice_room_id'] = 714408152061182033
    config['wkwm']['role_nozoki_id'] = 709225085575364650
    bot.config = config
    TOKEN = environ['BOT_ACCESS_TOKEN']  # 環境変数から取得
    for extension in extensions:
        bot.load_extension(f"Cogs.{extension}")
    bot.run(TOKEN)

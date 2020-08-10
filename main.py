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
extensions.append("ReactionEvent")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot = commands.Bot(
        command_prefix=[
            '$',
            '＄',
            '?',
            '？'],
        case_insensitive=True,
        description="Saru's Wakewakaran Bot Project")
    config["wkwm"]["room_id"] = 742001514771382313
    config['wkwm']['welcome_room_id'] = 742001514771382313
    config['wkwm']['leave_notice_room_id'] = 742001514771382313
    config['wkwm']['nozoki_role_id'] = 712526833995743252
    TOKEN = "NzQyMDA0MDk5MjU1NjMxOTA0.Xy_zKw.rRCRiqoZcWnqQy9h3pajl8KWLzs"
    # config["wkwm"]["room_id"] = environ['BOT_ROOM_ID']
    # config['wkwm']['welcome_room_id'] = environ['WELCOME_ROOM_ID']
    # config['wkwm']['leave_notice_room_id'] = environ['LEAVE_NOTICE_ROOM_ID']
    # config['wkwm']['nozoki_role_id'] = environ['NOZOKI_ROLE_ID']
    # TOKEN = environ['BOT_ACCESS_TOKEN']  # 環境変数から取得
    bot.config = config
    for extension in extensions:
        bot.load_extension(f"Cogs.{extension}")
    bot.run(TOKEN)

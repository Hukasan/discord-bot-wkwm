from discord.ext import commands
from os import environ, listdir, path
# import logging
# logging.basicConfig(filename='log/logger.log', level=logging.ERROR)
# logger = logging.getLogger(__name__)

config = {
    'wkwm': {
        'welcome_message': [
            "入隊希望などその他申請は各チャンネルへお願いします。",
            "各受付チャンネルのピン留めに詳細が有ります。"]}}

p = 'Cogs'
files = listdir(p)
extensions = [path.splitext(f)[0]
              for f in files if path.isfile(path.join(p, f))]


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    bot = commands.Bot(
        command_prefix=[
            '$',
            '＄',
            '?',
            '？'],
        case_insensitive=True,
        description="Saru's Wakewakaran Bot Project")
    config["wkwm"]["room_id"] = environ['BOT_ROOM_ID']
    config['wkwm']['welcome_room_id'] = environ['WELCOME_ROOM_ID']
    config['wkwm']['leave_notice_room_id'] = environ['LEAVE_NOTICE_ROOM_ID']
    config['wkwm']['nozoki_role_id'] = environ['NOZOKI_ROLE_ID']
    TOKEN = environ['BOT_ACCESS_TOKEN']  # 環境変数から取得
    bot.config = config
    for extension in extensions:
        bot.load_extension(f"Cogs.{extension}")
    bot.run(TOKEN)

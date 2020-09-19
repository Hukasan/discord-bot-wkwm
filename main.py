from os import environ, listdir, path
from discord.ext.commands import Bot
# import logging
# logging.basicConfig(filename='log/logger.log', level=logging.ERROR)
# logger = logging.getLogger(__name__)

config = {
    'wkwm': {
        'welcome_message': [
            "入隊希望などの申請は各チャンネルへお願いします。",
            "各チャンネルのピン留めに募集詳細が有ります。"]}}

p = '/home/hukasan/discord-bot-id/Cogs'
files = listdir(p)
extensions = [path.splitext(f)[0]
              for f in files if path.isfile(path.join(p, f))]
if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    bot = Bot(
        command_prefix=[
            '$',
            '＄',
            '?',
            '？'],
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

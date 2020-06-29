import discord
import logging
from datetime import datetime
import random

import sys
sys.path.append("./app/")
from app.json_io import json_io  # noqa # nopep
from app.talk_io import talk_io  # noqa # nopep

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


fc, f = json_io("./jsons/profile.json").get()
delete_log_channel_id = f.profile.delete_log_channel_id
room_id = f.profile.room_id
TOKEN = f.profile.token

talksc, talks = json_io("./jsons/Hangar.json").get()
gamelist = talks.status.game
talk = talk_io()
client = discord.Client()


@ client.event
async def on_ready():  # 起動時に動作する処理
    room_channel = client.get_channel(room_id)
    await room_channel.send(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "ログインしました")
    await client.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist) - 1)]))


@ client.event  # gemestatus変更
async def on_raw_message_edit(payload):
    await client.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist) - 1)]))


@ client.event  # メッセージ応答系
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    else:
        exs = talk.enter(message=message, content=message.content)
        if exs:
            if isinstance(exs[0], list):
                for ex in exs:
                    if not (ex in [None, "NULL", ' ', '　']):
                        await message.channel.send(ex)
            else:
                await message.channel.send(''.join(exs))

# @ client.event  # 削除監視機能
# async def on_message_delete(message):
#     export_channel = client.get_channel(delete_log_channel_id)
# await export_channel.send("["+datetime.now().strftime('%Y-%m-%d
# %H:%M:%S')+"|削除]\n"+message.author.mention+"\n"+"#"+message.channel.name+"
# \n"+message.content)

# Botの起動とDiscordサーバーへの接続
if __name__ == "__main__":
    client.run(TOKEN)

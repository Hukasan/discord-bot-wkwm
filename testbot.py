import discord
import logging
from datetime import datetime
import random
import json
from collections import OrderedDict
from box import Box


with open('profile.json', 'r', encoding="utf-8_sig") as f:
    res_j = json.load(f)

gamelist = res_j["statuses"][0]["game"]
delete_log_channel_id = res_j["profile"]["delete_log_channel_id"]
room_id = res_j["profile"]["room_id"]
TOKEN = res_j["profile"]["token"]


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# 起動時に動作する処理

client = discord.Client()


@ client.event
async def on_ready():
    # ターミナル出力
    print('ログインしました-')
    await client.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist)-1)]))
    # room = client.get_channel(room_id)


@client.event  # gemestatus変更
async def on_raw_message_edit(payload):
    await client.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist)-1)]))


@ client.event  # メッセージ応答系
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send(res_j["comands"][0]["reaction"])
    if 'わけわかめ' in message.content:
        await message.channel.send('わけわかめを検出しました')
    if '草' in message.content:
        await message.channel.send('こいつ草とかいってます')


@ client.event  # 削除監視機能
async def on_message_delete(message):
    export_channel = client.get_channel(delete_log_channel_id)
    await export_channel.send("["+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|削除]\n"+message.author.mention+"\n"+"#"+message.channel.name+" \n"+message.content)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
print("\r終了します")

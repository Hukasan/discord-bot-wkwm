import discord
import logging
from datetime import datetime
import random

delete_log_channel_id = 718354659592634430  # 削除履歴チャンネルID

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = "NzEyMTk4NDE2MjY4MjYzNDg1.XtYkiA.ZiJsdgSV_a6GQneweEOrmuj8BF8"

client = discord.Client()
# 起動時に動作する処理
gamelist = ["現実逃避", "シャドウバース", "荒野行動", "大富豪オンライン", "バトロワチーミング", "苗ちん", "親フラ"]


@ client.event
async def on_ready():
    # ターミナル出力
    print('ログインしました-')
    await client.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist)-1)]))


@client.event
async def on_raw_message_edit(payload):
    await client.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist)-1)]))
# メッセージ応答系


@ client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
    if 'わけわかめ' in message.content:
        await message.channel.send('わけわかめを検出しました')
        # 削除監視機能


@ client.event
async def on_message_delete(message):
    export_channel = client.get_channel(delete_log_channel_id)
    await export_channel.send("["+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|削除]\n"+message.author.mention+"\n"+"#"+message.channel.name+" \n"+message.content)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

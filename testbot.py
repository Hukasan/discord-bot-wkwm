import discord
import logging
from datetime import datetime
import random

delete_log_channel_id = 718354659592634430  # 削除履歴チャンネルID
bot_room_id = 718354659592634430

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

# async def role_comment_check():
#     for message in bot_room.history(limit=100):
#         if message.author == client.user:
#             if message.content == "暇ですか":
#                 await return 1
#     await retun 0


@ client.event
async def on_ready():
    # ターミナル出力
    print('ログインしました-')
    await client.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist)-1)]))
    bot_room = client.get_channel(bot_room_id)


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
        await message.channel.send('にゃーん')
    if 'わけわかめ' in message.content:
        await message.channel.send('わけわかめを検出しました')
    if '草' in message.content:
        await message.channel.send('こいつ草とかいってます')


@ client.event  # 削除監視機能
async def on_message_delete(message):
    export_channel = client.get_channel(delete_log_channel_id)
    await export_channel.send("["+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|削除]\n"+message.author.mention+"\n"+"#"+message.channel.name+" \n"+message.content)


# @ client.event
# async def on_raw_reaction_add(payload):

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

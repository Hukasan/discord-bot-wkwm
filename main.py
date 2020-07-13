import discord
from discord.ext import commands
import logging
from datetime import datetime
import random
from functools import partial

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
prefix = '&'
bot = commands.Bot(command_prefix='&',
                   description='猿sのバナナ農園の妖精')
talk.st.talk.cmd_checked = False


@ bot.event
async def on_ready():  # 起動時に動作する処理
    room_channel = bot.get_channel(room_id)
    await room_channel.send(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "ログインしました")
    await bot.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist) - 1)]))


@ bot.event  # gemestatus変更
async def on_raw_message_edit(payload):
    await bot.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist) - 1)]))


@bot.command(description="勝手に反応する文言を追加します")
async def add(ctx):
    talk.st.talk.fend2 = True
    talk.stc.write()
    talk.method2 = partial(
        talk.add_json,
        bc=talksc,
        b=talks.cats
    )


@ bot.event  # メッセージ応答系
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    else:
        if not (message.content[0] == prefix):
            exs = talk.enter(message=message, content=message.content)
            if exs:
                if isinstance(exs[0], list):
                    for ex in exs:
                        if not (ex in [None, "NULL", ' ', '　']):
                            await message.channel.send(ex)
                else:
                    await message.channel.send(''.join(exs))
        await bot.process_commands(message)  # bot.command共存に必須
# @ bot.event  # 削除監視機能
# async def on_message_delete(message):
#     export_channel = bot.get_channel(delete_log_channel_id)
# await export_channel.send("["+datetime.now().strftime('%Y-%m-%d
# %H:%M:%S')+"|削除]\n"+message.author.mention+"\n"+"#"+message.channel.name+"
# \n"+message.content)

# Botの起動とDiscordサーバーへの接続
if __name__ == "__main__":
    bot.run(TOKEN)

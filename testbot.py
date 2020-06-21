import discord
import logging
from datetime import datetime
import random
from json_io import json_io
from box import Box


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def yes_no_input(choice):
    if choice in ['Y', 'y', 'ye', 'yes', 'Ｙ', 'ｙ']:
        return True
    else:
        return False


def state_init(fp: Box):
    fp.cr = {}
    fp.cr.name = False
    fp.cr.react = False
    fp.cr.com = False
    fp.cr.catcall = False
    fp.cr.change = False
    fp.cr.end = False
    fp.cr.content = []


def json_io_load(name: str) -> (json_io, Box):
    if name == 'profile':
        jc, f = json_io().get("Z:/Github/discord-bot-id/profile.json")
    elif name == 'state':
        jc, f = json_io().get("Z:/Github/discord-bot-id/status.json")
    return jc, f


fc, f = json_io_load('profile')
gamelist = f.status.game
delete_log_channel_id = f.profile.delete_log_channel_id
room_id = f.profile.room_id
TOKEN = f.profile.token

pc, fp = json_io_load('state')
state_init(fp)
cr = fp.cr
pc.write()


# 起動時に動作する処理

client = discord.Client()


@ client.event
async def on_ready():
    room_channel = client.get_channel(room_id)
    await room_channel.send(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"ログインしました")
    await client.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist)-1)]))


@ client.event  # gemestatus変更
async def on_raw_message_edit(payload):
    await client.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist)-1)]))


@ client.event  # メッセージ応答系
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    else:
        global fp, f, pc, jc
        jc, f = json_io().get("Z:/Github/discord-bot-id/profile.json")
        pc, fp = json_io().get("Z:/Github/discord-bot-id/status.json")
        cd = f.commands.to_dict()
        reactd = f.catcalls.to_dict()
        if fp.cr.change:
            if yes_no_input(message.content):
                fp.cr.change = False
                fp.cr.react = True
                pc.write()
                await message.channel.send("返答は?")
                return
            else:
                fp.cr.end = True
        if message.content == 'q' or fp.cr.end:
            state_init(fp)
            await message.channel.send("取り消し")
        elif fp.cr.name:
            if (fp.cr.com and message.content in cd) or (fp.cr.catcall and message.content in reactd):
                await message.channel.send("もう追加されてるよ,変更する？(Y/N)")
                fp.cr.change = True
                fp.cr.name = False
                fp.cr.content = message.content
            else:
                fp.cr.content = message.content
                await message.channel.send("返答は？")
                fp.cr.react = True
                fp.cr.name = False
        elif fp.cr.react:
            if fp.cr.com:
                cd[fp.cr.content] = {'reaction': message.content}
                f.commands = cd
            elif fp.cr.catcall:
                reactd[fp.cr.content] = {'reaction': message.content}
                f.catcalls = reactd
            await message.channel.send("追加かんりょう")
            jc.write()
            state_init(fp)

        elif message.content[0] == '/':
            command = message.content[1:]
            if command == 'command_add':
                fp.cr.name = True
                fp.cr.com = True
                await message.channel.send("追加コマンドをドウゾ(キャンセル : ｑ)")
            elif command == 'react_add':
                fp.cr.name = True
                fp.cr.catcall = True
                await message.channel.send("追加リアクションをドウゾ(キャンセル : ｑ)")
            elif command in cd:
                await message.channel.send(cd.get(command).get('reaction'))
        else:
            for react in reactd:
                if react in message.content:
                    await message.channel.send(reactd.get(react).get('reaction'))
                    break
        print(fp.to_dict())
        pc.write()


# @ client.event  # 削除監視機能
# async def on_message_delete(message):
#     export_channel = client.get_channel(delete_log_channel_id)
    # await export_channel.send("["+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|削除]\n"+message.author.mention+"\n"+"#"+message.channel.name+" \n"+message.content)


# Botの起動とDiscordサーバーへの接続
if __name__ == "__main__":

    client.run(TOKEN)
    print("\r終了します")

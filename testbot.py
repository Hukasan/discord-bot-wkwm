import discord
import logging
from datetime import datetime
import random
from json_io import json_io
from box import Box

jc, f = json_io().get("Z:/Github/discord-bot-id/profile.json")
pc, fp = json_io().get("Z:/Github/discord-bot-id/status.json")

gamelist = f.status.game
delete_log_channel_id = f.profile.delete_log_channel_id
room_id = f.profile.room_id
TOKEN = f.profile.token

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def yes_no_input(choice):
    if choice in ['y', 'ye', 'yes']:
        return True
    else:
        return False


def state_init(fp: Box):
    fp.cr.name = False
    fp.cr.react = False
    fp.cr.com = False
    fp.cr.catcall = False
    fp.cr.change = False
    fp.cr.content = []


jc, f = json_io().get("Z:/Github/discord-bot-id/profile.json")
pc, fp = json_io().get("Z:/Github/discord-bot-id/status.json")

fp.cr = {}
state_init(fp)
pc.write()

# 起動時に動作する処理

client = discord.Client()


@ client.event
async def on_ready():
    # ターミナル出力
    print('ログインしました-')
    room_channel = client.get_channel(room_id)
    await room_channel.send(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"ログインしました")
    # await client.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist)-1)]))


@ client.event  # gemestatus変更
async def on_raw_message_edit(payload):
    await client.change_presence(activity=discord.Game(gamelist[random.randint(0, len(gamelist)-1)]))


@ client.event  # メッセージ応答系
async def on_message(message):
    global fp, f, pc, jc
    jc, f = json_io().get("Z:/Github/discord-bot-id/profile.json")
    pc, fp = json_io().get("Z:/Github/discord-bot-id/status.json")
    cd = f.commands.to_dict()
    reactd = f.catcalls.to_dict()
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    elif fp.cr.name:
        if message.content == 'q':
            state_init(fp)
            await message.channel.send("取り消し")
        if fp.cr.change:
            if yes_no_input(message.content):
                fp.cr.change = True
            else:
                fp.cr.name = False
        else:
            fp.cr.content = message.content

        if fp.cr.com and message.content in cd:
            await message.channel.send("もう追加されてるよ,変更する？")
            fp.cr.change = 1
            fp.cr.name = 0
        elif fp.cr.catcall and message.content in reactd:
            await message.channel.send("もう追加されてるよ,変更する？(Y/N)")
            fp.cr.change = 1
            fp.cr.name = 0
        await message.channel.send("返答は？")
        fp.cr.react = True
        fp.cr.name = False
    elif fp.cr.react == True:
        if fp.cr.com == True:
            cd[fp.cr.content] = {'reaction': message.content}
            f.commands = cd
        elif fp.cr.catcall == True:
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
    pc.write()


# @ client.event  # 削除監視機能
# async def on_message_delete(message):
#     export_channel = client.get_channel(delete_log_channel_id)
    # await export_channel.send("["+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"|削除]\n"+message.author.mention+"\n"+"#"+message.channel.name+" \n"+message.content)


# Botの起動とDiscordサーバーへの接続
if __name__ == "__main__":

    client.run(TOKEN)
    print("\r終了します")

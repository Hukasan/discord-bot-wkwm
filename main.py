import discord
from discord.ext import commands

import sys
sys.path.append("./app/")
from app.TalkIOCog import TalkIO  # noqa # nopep
from app.BaseOverwriteCog import Help  # noqa # nopep

BOTTOKEN = "NzEyMTk4NDE2MjY4MjYzNDg1.XtYkiA.ZiJsdgSV_a6GQneweEOrmuj8BF8"

<<<<<<< HEAD

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
=======
if __name__ == '__main__':
    bot = commands.Bot(command_prefix="$", help_command=Help(),
                       description="猿sのバナナ農園の精霊")
    bot.add_cog(TalkIO(bot))
    bot.run(BOTTOKEN)
>>>>>>> a2c1353ecccb15de4d454c1e5b1e7cea0f2d0def

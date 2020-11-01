from os import environ, listdir, path
from discord.ext.commands import Bot
from discord import Intents


p = "Cogs"
files = listdir(p)
extensions = [path.splitext(f)[0] for f in files if path.isfile(path.join(p, f))]
intents = Intents.all()
if __name__ == "__main__":
    bot = Bot(
        command_prefix=["$", "＄", "?", "？"], description="Saru's Wakewakaran Bot Project\rえすだぶりゅびてぃ", intents=intents
    )
    config = {}
    config["room_id"] = environ["BOT_ROOM_ID"]
    config["welcome_room_id"] = environ["WELCOME_ROOM_ID"]
    config["leave_notice_room_id"] = environ["LEAVE_NOTICE_ROOM_ID"]
    config["nozoki_role_id"] = environ["NOZOKI_ROLE_ID"]
    config["ministar_role_id"] = environ["MINISTAR_ROLE_ID"]
    config["member_role_id"] = environ["MEMBER_ROLE_ID"]
    TOKEN = environ["BOT_ACCESS_TOKEN"]  # 環境変数から取得
    bot.config = {"wkwm": config}
    for extension in extensions:
        bot.load_extension(f"Cogs.{extension}")
    bot.run(TOKEN)

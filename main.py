from os import environ, listdir, path
from discord.ext.commands import Bot


files = listdir("Cogs")
extensions = [path.splitext(f)[0] for f in files if path.isfile(path.join(p, f))]
if __name__ == "__main__":
    bot = Bot(
        command_prefix=["$", "＄", "?", "？"],
        description="Saru's Wakewakaran Bot Project",
    )
    config = {}
    config["wkwm"] = {}
    config["wkwm"]["room_id"] = environ["BOT_ROOM_ID"]
    config["wkwm"]["welcome_room_id"] = environ["WELCOME_ROOM_ID"]
    config["wkwm"]["leave_notice_room_id"] = environ["LEAVE_NOTICE_ROOM_ID"]
    config["wkwm"]["nozoki_role_id"] = environ["NOZOKI_ROLE_ID"]
    TOKEN = environ["BOT_ACCESS_TOKEN"]  # 環境変数から取得
    bot.config = config
    for extension in extensions:
        bot.load_extension(f"Cogs.{extension}")
    bot.run(TOKEN)

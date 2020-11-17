from os import environ, listdir, path
from discord.ext.commands import Bot
from discord import Intents


p = "Cogs"
files = listdir(p)
extensions = [path.splitext(f)[0] for f in files if path.isfile(path.join(p, f))]
intents = Intents
intents = Intents.all()
intents.typing = False
intents.bans = False
intents.webhooks = False
intents.invites = False
intents.voice_states = False
intents.dm_messages = False
intents.dm_reactions = False


desc = "_Sarus'WakewakaranBotProject_\r猿sクランサーバ専門,惰性で作れしお粗末bot"

if __name__ == "__main__":
    bot = Bot(
        command_prefix=["?", "？"],
        description=desc,
        intents=intents,
        case_insensitive=True,
    )
    home_config = {}
    home_config["channel_ids"] = {
        "room": environ["BOT_ROOM_ID"],
        "welcome": environ["WELCOME_ROOM_ID"],
        "leave_notice": environ["LEAVE_NOTICE_ROOM_ID"],
    }
    home_config.update(
        {
            "bottoms": {},
            "bottoms_sub": {},
            "bottom_args": {},
            "help_author": {},
        }
    )
    home_config["role_ids"] = {
        "nozoki": environ["NOZOKI_ROLE_ID"],
        "member": environ["MEMBER_ROLE_ID"],
        "ministar": environ["MINISTAR_ROLE_ID"],
        "server_info_scopes": [707125794404565002],
    }
    TOKEN = environ["BOT_ACCESS_TOKEN"]  # 環境変数から取得
    bot.config = {
        "funcs": {},
        "wkwm": home_config,
        "707027737335955476": home_config,
    }

    @bot.listen()
    async def on_ready():
        for g in bot.guilds:
            if g.rules_channel:
                bot.config[str(g.id)].update(
                    {"rules_channel": f"{g.rules_channel.mention}"}
                )

    for extension in extensions:
        bot.load_extension(f"Cogs.{extension}")
    bot.run(TOKEN)

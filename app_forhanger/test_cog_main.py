from discord.ext import commands
import traceback


class TestBot(commands.Bot):
    def __init__(self, command_prefix, description=None, **options):
        super().__init__(command_prefix,
                         description=description, **options)
        try:
            self.load_extension("test_cog")
        except Exception:
            traceback.print_exc()

    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')


if __name__ == '__main__':
    # command_prefixはコマンドの最初の文字として使うもの。 e.g. !ping
    bot = TestBot(command_prefix='$')
    bot.run("NzEyMTk4NDE2MjY4MjYzNDg1.XtYkiA.ZiJsdgSV_a6GQneweEOrmuj8BF8")  # Botのトークン

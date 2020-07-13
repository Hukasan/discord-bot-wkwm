from discord.ext import commands
from box import Box


class talk(commands.Cog, name='基本会話介入系',):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx):
        await ctx.send("あどぉー？")

    def get(self):
        try:
            self.jf = Box.from_json(filename=self.fname)
        except BaseException:
            print(self.fname + "ERROR : file_open_error")

    def write(self):
        try:
            self.jf.to_json(self.fname)
        except BaseException:
            print("ERROR : file_export_error[" + self.fname + ']')


def setup(bot):
    bot.add_cog(talk(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。

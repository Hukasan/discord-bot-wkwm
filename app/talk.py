from box import Box
from json_io import json_io
import discord


class talk:
    message = discord.message
    st = Box
    stc = json_io
    st.content = []
    talk = Box
    talkc = json_io

    def __init__(self):
        self.stc, temp = json_io().get("./json/state.json")
        self.st = temp.cr
        self.reset()
        self.talkc, self.talk = json_io().get("./json/talks.json")

    def enter(self, message: discord.message, mode):
        self.message = message

    def reset(self):
        self.st = {
            "name": False,
            "react": False,
            "com": False,
            "catcall": False,
            "change": False,
            "end": False,
            "content": []
        }

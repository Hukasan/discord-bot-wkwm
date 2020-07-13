from box import Box
import discord
from functools import partial
import pprint
from json_io import json_io  # noqa


class talk_io:
    message = discord.message
    content = "NULL"
    st = talks = Box
    stc = talksc = json_io
    method1 = method2 = None

    def __init__(self):
        self.stc, self.st = json_io("./jsons/state.json").get()
        self.talksc, self.talks = json_io("./jsons/Hangar.json").get()
        self.st.talk = "NULL"
        self.reset()

    def relode(self):
        self.stc, self.st = self.stc.get()
        self.talksc, self.talks = self.talksc.get()

    def enter(self, message: discord.message, content: str) -> list:
        self.relode()
        self.message = message
        self.content = content
        return self.analysis()

    def reset(self):
        self.cmd_checked = False
        self.st.talk = Box({
            "ins": ["NULL"] * 5,
            "name": "NULL",
            "key": "NULL",
            "fname": False,
            "freact": False,
            "fend1": False,
            "fend2": False,
        })
        self.stc.write()

    def analysis(self):
        st = self.st.talk
        if st.fend1:
            return self.method1()
        elif st.fend2:
            return self.method2()
        else:
            ex = []
            for react in self.talks.cats:
                if react in self.content:
                    ex.append(self.talks.cats[react].react)
            return ex

    def req_yn(self, comment: str):
        con = self.content
        st = self.st.talk
        st.fend1 = False
        self.stc.write()
        if not(con in ['Y', 'y', 'ye', 'yes', 'Ｙ', 'ｙ']):
            return 'キャンセルします'
        return comment

    def add_json(self, bc: json_io, b: Box) -> str:
        st = self.st.talk
        con = self.content
        ex = [None, "key?", (st.key + '?'), "すでに追加されているよ、変更する？", "登録完了", ]
        if st.freact:
            b[st.name] = {st.key: con}
            bc.write()
            self.reset()
            ex_num = 5
        elif st.fname:
            st.name = con
            st.fname = False
            if st.name in b:
                st.fend1 = True
                self.method1 = partial(self.req_yn, comment=ex[2])  # Y/N関数呼び出し
                ex_num = 3
            else:
                ex_num = 2
            st.freact = True
        else:
            st.key = "react"
            st.fname = True
            ex_num = 1
        self.stc.write()
        return ex[ex_num]

    def alldelete_key(self, a, target_key):
        delete_key_list = []
        for key, value in a.items():
            if (key == target_key) or (key in target_key):
                delete_key_list.append(key)
            elif isinstance(value, dict):
                self.alldelete_key(value, target_key)
        for dkey in delete_key_list:
            del a[dkey]

    def felp_view(self, mode: str):
        if mode == 'cmd':
            temp = self.talks.MonCmds.to_dict()
        elif mode == 'react':
            temp = self.talks.cats.to_dict()
        else:
            temp = self.talks.to_dict()
        self.alldelete_key(temp, ['react', 'status', 'desc'])
        exs = pprint.pformat(temp, width=33, sort_dicts=False)
        self.reset()
        return exs.replace('{', ' ').replace('}', '').replace('  \'desc\':', '').replace('\'', ' ').replace(',', '')


if __name__ == "__main__":
    c = talk_io()
    # print(c.enter(message=None, content="/help cmd"))
    # print(c.enter(message=None, content="test"))
    # print(c.enter(message=None, content="y"))
    # print(c.enter(message=None, content="testdesu"))
    # print(c.enter(message=None, content="/help"))

    # def do_cmd(self, subcmds: str):
    #     st = self.st.talk
    #     st.fend2 = True
    #     self.stc.write()

    #     if subcmds[0] == 'help':
    #         return self.felp_view(mode=subcmds[1])
    #     elif subcmds[0] in self.talks.MonCmds:
    #         ex = self.talks.MonCmds[subcmds[0]].react
    #         self.reset()
    #         return ex
    #     else:
    #         self.reset()
    #         return "NULL"

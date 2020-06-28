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
    method1 = None
    method2 = None

    def __init__(self):
        self.stc, self.st = json_io("./jsons/state.json").get()
        self.st.talk = "NULL"
        self.reset()
        self.talksc, self.talks = json_io("./jsons/Hangar.json").get()

    def enter(self, message: discord.message, content: str) -> str:
        self.message = message
        self.content = content
        return self.eval_cmd()

    def reset(self):
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

    def eval_cmd(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        con = self.content
        st = self.st.talk
        if st.fend1:
            return self.method1()
        elif st.fend2:
            return self.method2()
        elif con[0] == '/':
            st.fend2 = True
            for i in range(len(st.ins)):
                con = con[1:]
                num = con.find(' ')
                if num > (0):
                    st.ins[i] = (con[:num])
                    con = con[num:]
                else:
                    st.ins[i] = con
                    break
            self.stc.write()
            return self.do_cmd(i + 1)
        else:
            ex = []
            for react in self.talks.cats:
                if react in self.content:
                    ex.append(self.talks.cats[react].react)
            return ex

    def do_cmd(self, size: int):
        st = self.st.talk
        cmd = st.ins
        if cmd[0] == "add":
            if cmd[1] == "cmd":
                self.method2 = partial(
                    self.add_json,
                    bc=self.talksc,
                    b=self.talks.cmds,
                    size=size)
                return self.method2()
            elif cmd[1] == "react":
                self.method2 = partial(
                    self.add_json,
                    bc=self.talksc,
                    b=self.talks.cats,
                    size=size)
                return self.method2()
        elif cmd[0] == 'help':
            return self.felp_view(mode=cmd[1])
        elif cmd[0] in self.talks.cmds:
            ex = self.talks.cmds[cmd[0]].react
            self.reset()
            return ex
        else:
            self.reset()
            return "NULL"

    def req_yn(self, comment: str):
        con = self.content
        st = self.st.talk
        st.fend1 = False
        self.stc.write()
        if not(con in ['Y', 'y', 'ye', 'yes', 'Ｙ', 'ｙ']):
            return 'キャンセルします'
        return comment

    def add_json(self, bc: json_io, b: Box, size: int) -> str:
        st = self.st.talk
        con = self.content
        ex = [None, "コマンドは？", "返答は？", "すでに追加されているよ、変更する？",
              "説明をﾄﾞｰｿﾞ( *'∀')っ", "登録完了", ]
        ex_num = 0
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
                self.method1 = partial(self.req_yn, comment=ex[2])
                ex_num = 3
            else:
                ex_num = 2
            st.freact = True
        else:
            if st.ins[2][0] == '!':
                st.key = st.ins[2][1:]
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
        exs = []
        if mode == 'NULL':
            mode = 'all'
        if mode == 'all':
            temp = self.talks.to_dict()
            self.alldelete_key(temp, ['react', 'status'])
            exs = pprint.pformat(temp)
        elif mode == 'cmd':
            exs = pprint.pformat(self.talks.cmds.to_dict(), )
        elif mode == 'react':
            exs = pprint.pformat(self.talks.cats.to_dict(), )
        self.reset()
        return exs.replace('{', ' ').replace('}', '').replace('  \'desc\':', '').replace('\'',' ').replace(',','')
        # return  exs

if __name__ == "__main__":
    c = talk_io()
    print(c.enter(message=None, content="/help"))
    # print(c.enter(message=None, content="test"))
    # print(c.enter(message=None, content="y"))
    # print(c.enter(message=None, content="testdesu"))
    # print(c.enter(message=None, content="/help"))

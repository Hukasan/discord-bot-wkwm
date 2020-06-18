from box import Box


class json_io:
    fname = []
    jf = Box

    def __init__(self):
        pass

    def get(self, file_path: str):
        self.fname = file_path
        try:
            self.jf = Box.from_json(filename=self.fname)
            return self, self.jf
        except:
            print("ERROR : file_open_error")

    def write(self):
        try:
            self.jf.to_json(self.fname)
        except:
            print("ERROR : file_export_error")


if __name__ == "__main__":
    file_path = "Z:/Github/discord-bot-id/profile.json"
    jc, f = json_io().get(file_path)
    f.profile.name = "test4"
    jc.write()

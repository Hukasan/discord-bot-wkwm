from box import Box


class json_io:
    def __init__(self, file_path: str):
        self.fname = file_path
        self.jf = Box

    def get(self):
        try:
            self.jf = Box.from_json(filename=self.fname)
            return self, self.jf
        except:
            print(self.fname+"ERROR : file_open_error")

    def write(self):
        try:
            self.jf.to_json(self.fname)
        except:
            print("ERROR : file_export_error["+self.fname+']')


if __name__ == "__main__":
    file_path = "./jsons/state.json"
    jc, f = json_io(file_path).get()
    name = "test"
    f[name] = "test!"
    jc.write()

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Column, Table
from sqlalchemy.types import Integer, String, Boolean
from os import environ as getpath, listdir, path
import sqlcsv
import csvkit
import subprocess

# from logging import getLogger
# logger = getLogger(__name__)


db_uri = str(getpath["DATABASE_URL"])
# db_uri = "postgresql://wkwm:kkkk@localhost/wkwm"

engine = create_engine(db_uri)
Model = declarative_base()

SessionClass = sessionmaker(engine)  # セッションを作るクラスを作成
session = SessionClass()


class DBIO:
    """
    データベース管理
    """

    def __init__(self):
        self.table = Model

    def tbview(self):
        print(session.query(self.table).all())

    def tbselect(self, id=str()):
        # try:
        result = self.table
        if id:
            result = session.query(self.table).filter(self.table.id == id).all()
            return result
        else:
            results = session.query(self.table).all()
            return results
        # except BaseExceptio

    def tbdelete(self, id=str()):
        if id:
            session.query(self.table).filter(self.table.id == id).delete()
            session.commit()
        session.close()


class Cmdtb(DBIO):
    def __init__(self):
        self.table = self.Cmd

    class Cmd(Model):
        __tablename__ = "cmds"
        id = Column(String(), nullable=False, primary_key=True)
        body = Column(String(), nullable=False)

    def add(self, id: str, body: str):
        """
        コマンド追加

        Args:
            title (str): コマンド
            body (str): 返答
        """
        t = self.table()
        if not (self.tbdelete(id=id)):
            t.id = id
            t.body = body
            session.add(t)
        else:
            t.query.filter(t.id == id).first()
            t.body = body
        session.commit()
        session.close()


class Clantb(DBIO):
    def __init__(self):
        self.table = self.Clan

    class Clan(Model):
        __tablename__ = "clans"
        id = Column(Integer(), primary_key=True)
        body = Column(String(), nullable=False)

    def add(self, id: int, body: str):
        """
        クラン追加

        Args:
            title (int): クランNo
            body (str): 返答
        """
        t = self.table()
        if not (self.tbdelete(id=id)):
            t.id = id
            t.body = body
            session.add(t)
        else:
            t.query.filter(t.id == id).first()
            t.body = body
        session.commit()
        session.close()


class Cattb(DBIO):
    def __init__(self):
        self.table = self.Cat

    class Cat(Model):
        __tablename__ = "cats"
        id = Column(String(), nullable=False, primary_key=True)
        body = Column(String(), nullable=False)
        isreact = Column(Boolean(), nullable=True)

    def add(self, id: str, body: str, isreact=False):
        """
        リアクション追加

        Args:
            title (str): トリガー
            body (str): 返答
        """
        t = self.table()
        if not (self.tbdelete(id=id)):
            t.id = id
            t.body = body
            t.isreact = isreact
            session.add(t)
        else:
            t.query.filter(t.id == id).first()
            t.body = body
            t.isreact = isreact
        session.commit()
        session.close()


if __name__ == "__main__":
    type_dict = {"VARCHAR": "str", "BOOLEAN": "str", "INTEGER": "int"}
    table_names = Model.metadata.tables.keys()
    # p = "/home/hukasan/discord-bot-id/db_backup"
    for table_name in table_names:
        s = f"sqlcsv --db-url {db_uri} select \
  --sql 'SELECT * FROM {table_name}'"
        proc = subprocess.run(
            s, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        print(proc.stdout)
    if table_names:
        Model.metadata.drop_all(engine)
        print("初期化しました、ファイルを読み込みます..")
        Model.metadata.create_all(engine)
        print("生成完了")
        p = "db_new"
        for f in listdir(p):
            if path.isfile(path.join(p, f)):
                for table_name in table_names:
                    if (path.splitext(f)[0]) == table_name:
                        table = Model.metadata.tables[table_name]
                        column_names = list()
                        value_names = list()
                        type_names = list()
                        nullables = list()
                        for c in table.columns:
                            column_names.append(c.description)
                            value_names.append("%s")
                            type_names.append(type_dict.get(str(c.type)))
                            nullables.append("true")

                        s = f"sqlcsv --db-url {db_uri} insert \
  --sql 'INSERT INTO {table_name}({','.join(column_names)}) VALUES ({','.join(value_names)})' \
  --types {','.join(type_names)} --infile {p}/{table_name}.csv --nullables {','.join(nullables)}"
                        print(s)
                        proc = subprocess.run(
                            s,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                        )

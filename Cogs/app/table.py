from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Boolean
from os import environ as getpath

# from logging import getLogger
# logger = getLogger(__name__)


db_uri = str(getpath["DATABASE_URL"])
# db_uri = "postgresql://wkwm:kkkk@localhost/wkwm"

engine = create_engine(db_uri)
Model = declarative_base()

SessionClass = sessionmaker(engine)  # セッションを作るクラスを作成
session = SessionClass()


class DBIO:
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


class Cattb(DBIO):
    def __init__(self):
        self.table = self.Cat

    class Cat(Model):
        __tablename__ = "cats"
        id = Column(String(), nullable=False, primary_key=True)
        body = Column(String(), nullable=False)

    def add(self, id: str, body: str):
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
            session.add(t)
        else:
            t.query.filter(t.id == id).first()
            t.body = body
        session.commit()
        session.close()


class MsfRtb(DBIO):
    def __init__(self):
        self.table = self.MsforReact

    class MsforReact(Model):
        __tablename__ = "msforreact"
        id = Column(String(), nullable=False, primary_key=True)
        cid = Column(String(), nullable=False)
        seed = Column(String(), nullable=True)

    def add(self, id: str, cid: str, seed: str):
        t = self.table()
        if not (self.tbdelete(id=id)):
            t.id = id
            t.cid = cid
            t.seed = seed
            session.add(t)
        session.commit()
        session.close()


class EmbedPages(DBIO):
    def __init__(self):
        self.table = self.Page

    class Page(Model):
        __tablename__ = "embedpages"
        id = Column(String(), nullable=False, primary_key=True)
        number = Column(Integer, nullable=False)
        content = Column(String(), nullable=False)
        isnow = Column(Boolean(), nullable=False)

    def add(self, id: str, number: int, content: str, isnow: bool):
        t = self.table()
        if not (self.tbdelete(id=id)):
            t.id = id
            t.number = number
            t.content = content
            t.isnow = isnow
            session.add(t)
        session.commit()
        session.close()

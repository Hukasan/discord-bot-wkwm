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
        id = Column(Integer, primary_key=True)
        body = Column(String(), nullable=False)


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
    Model.metadata.create_all(engine)

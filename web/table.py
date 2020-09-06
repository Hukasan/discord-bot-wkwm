from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.datastructures import ImmutableDict
from hamlish_jinja import HamlishExtension
from os import environ as getpath
# from logging import getLogger
# logger = getLogger(__name__)


class FlaskwithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=[HamlishExtension]
    )


app = FlaskwithHamlish(__name__)

db_uri = str(getpath['DATABASE_URL'])
# db_uri = "postgresql://wkwm:kkkk@localhost/wkwm"

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


db = SQLAlchemy(app)


class DBIO():
    def __init__(self):
        self.table = db.Model

    def tbview(self):
        print(self.table.query.all())

    def tbselect(self, id=str()):
        # try:
        result = self.table
        if id:
            result = self.table.query. \
                filter(self.table.id == id). \
                all()
            return result
        else:
            results = self.table.query.all()
            return results
        # except BaseExceptio

    def tbdelete(self, id=str()):
        if id:
            self.table.query. \
                filter(self.table.id == id). \
                delete()
            db.session.commit()
        db.session.close()


class Cmdtb(DBIO):
    def __init__(self):
        self.table = self.Cmd

    class Cmd(db.Model):
        __tablename__ = "cmds"
        id = db.Column(db.String(), nullable=False, primary_key=True)
        body = db.Column(db.String(), nullable=False)

    def add(self, id: str, body: str):
        """
        コマンド追加

        Args:
            title (str): コマンド
            body (str): 返答
        """
        t = self.table()
        if not(self.tbdelete(id=id)):
            t.id = id
            t.body = body
            db.session.add(t)
        else:
            t.query. \
                filter(t.id == id). \
                first()
            t.body = body
        db.session.commit()
        db.session.close()


class Cattb(DBIO):
    def __init__(self):
        self.table = self.Cat

    class Cat(db.Model):
        __tablename__ = "cats"
        id = db.Column(db.String(), nullable=False, primary_key=True)
        body = db.Column(db.String(), nullable=False)

    def add(self, id: str, body: str):
        """
        リアクション追加

        Args:
            title (str): トリガー
            body (str): 返答
        """
        t = self.table()
        if not(self.tbdelete(id=id)):
            t.id = id
            t.body = body
            db.session.add(t)
        else:
            t.query. \
                filter(t.id == id). \
                first()
            t.body = body
        db.session.commit()
        db.session.close()


class MsfRtb(DBIO):
    def __init__(self):
        self.table = self.MsforReact

    class MsforReact(db.Model):
        __tablename__ = "msforreact"
        id = db.Column(db.String(), nullable=False, primary_key=True)
        cid = db.Column(db.String(), nullable=False)
        seed = db.Column(db.String(), nullable=True)

    def add(self, id: str, cid: str, seed: str):
        t = self.table()
        if not(self.tbdelete(id=id)):
            t.id = id
            t.cid = cid
            t.seed = seed
            db.session.add(t)
        db.session.commit()
        db.session.close()


class EmbedPages(DBIO):
    def __init__(self):
        self.table = self.Page

    class Page(db.Model):
        __tablename__ = "embedpages"
        id = db.Column(db.String(), nullable=False, primary_key=True)
        number = db.Column(db.Integer, nullable=False)
        content = db.Column(db.String(), nullable=False)
        isnow = db.Column(db.Boolean(), nullable=False)

    def add(self, id: str, number: int, content: str, isnow: bool):
        t = self.table()
        if not(self.tbdelete(id=id)):
            t.id = id
            t.number = number
            t.content = content
            t.isnow = isnow
            db.session.add(t)
        db.session.commit()
        db.session.close()

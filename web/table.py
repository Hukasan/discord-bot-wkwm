from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.datastructures import ImmutableDict
from hamlish_jinja import HamlishExtension
from os import environ as getpath


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

    def tbselect(self, id):
        result = self.table
        if id:
            result = self.table.query. \
                filter(self.table.id == id). \
                all()
            return result
        else:
            results = self.table.query.all()
            return results


class Cmdtb(DBIO):
    def __init__(self):
        self.table = self.Cmd

    class Cmd(db.Model):
        __tablename__ = "cmds"
        title = db.Column(db.String(), nullable=False, primary_key=True)
        body = db.Column(db.String(), nullable=False)

    def add(self, id: str, body: str):
        """
        コマンド追加

        Args:
            title (str): コマンド
            body (str): 返答
        """
        t = self.table()
        t.id = id
        t.body = body
        db.session.add(t)
        db.session.commit()


class MsfRtb(DBIO):
    def __init__(self):
        self.table = self.MsforReact

    class MsforReact(db.Model):
        __tablename__ = "msforreact"
        mid = db.Column(db.Integer(), nullable=False, primary_key=True)
        cid = db.Column(db.Integer(), nullable=False)
        seed = db.Column(db.String(), nullable=True)

    def add(self, message_id, channel_id, seed):
        t = self.table
        t.mid = message_id
        t.cid = channel_id
        t.seed = seed
        db.session.add(t)
        db.session.commit()


class Cattb(DBIO):
    def __init__(self):
        self.table = self.Cat

    class Cat(db.Model):
        __tablename__ = "cats"
        title = db.Column(db.String(), nullable=False, primary_key=True)
        body = db.Column(db.String(), nullable=False)

    def add(self, title: str, body: str):
        """
        リアクション追加

        Args:
            title (str): トリガー
            body (str): 返答
        """
        t = self.table()
        t.title = title
        t.body = body
        db.session.add(t)
        db.session.commit()

# def view():
#     for cmd in Cmd.query.all():
#         print(f"{cmd.title}|{cmd.body}")


# @app.route('/')
# def hello_world():
#     entries = Entry_cmd.query.all()
#     return render_template('index.haml', entries=entries)


# @app.route('/post', methods=['POST'])
# def add_entry():
#     entry = Entry_cmd()
#     entry.title = request.form['title']
#     entry.body = request.form['body']
#     db.session.add(entry)
#     db.session.commit()
#     return redirect(url_for('hello_world'))

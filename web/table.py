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

    def tbselect(self, title=str()):
        results = []
        result = self.table
        if title:
            result = self.table.query. \
                filter(self.table.title == title). \
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

    def add(self, title: str, body: str):
        """
        コマンド追加

        Args:
            title (str): コマンド
            body (str): 返答
        """
        t = self.table()
        t.title = title
        t.body = body
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

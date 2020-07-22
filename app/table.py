import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from hamlish_jinja import HamlishExtension
from werkzeug.datastructures import ImmutableDict


class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=[HamlishExtension]
    )


app = Flask(__name__)

db_uri = os.environ.get('DATABASE_URL')
print(db_uri)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()


@app.route('/')
def hello_world():
    entries = Entry.query.all()
    return render_template('index.haml', entries=entries)  # 変更


class Entry(db.Model):
    """
    テーブルを定義
    Args:
    """
    # テーブル名を定義
    __tablename__ = "entries"

    # カラムを定義
    id = db.Column(db.Integer, primary_key=True)  # 追加
    title = db.Column(db.String(), nullable=False)  # 追加
    body = db.Column(db.String(), nullable=False)  # 追加

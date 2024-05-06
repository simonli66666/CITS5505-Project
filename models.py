import datetime

from bbs.extensions import db
from flask_login import UserMixin

class User(db.Model):
    __tablename__ = 't_user'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, index=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, index=True, unique=True, comment='user name')
    nickname = db.Column(db.String(40), nullable=False, unique=True, comment='user nick name')
    password = db.Column(db.String(256), comment='user password')
    create_time = db.Column(db.DATETIME, default=datetime.datetime.now)



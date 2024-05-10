import datetime
from sqlalchemy.ext.hybrid import hybrid_property

from bbs.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 't_user'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, index=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, index=True, unique=True, comment='user name')
    nickname = db.Column(db.String(40), nullable=False, unique=True, comment='user nick name')
    password = db.Column(db.String(256), comment='user password')
    create_time = db.Column(db.DATETIME, default=datetime.datetime.now)

    posts = db.relationship('Post', back_populates='user')

class Post(db.Model):
     __tablename__ = 't_post'

     id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, index=True)
     title = db.Column(db.String(100), index=True, nullable=False)
     image = db.Column(db.String(255), nullable=True)
     ingredient1 = db.Column(db.TEXT, nullable=False)
     ingredient2 = db.Column(db.TEXT, nullable=True)
     ingredient3 = db.Column(db.TEXT, nullable=True)
     ingredient4 = db.Column(db.TEXT, nullable=True)
     ingredient5 = db.Column(db.TEXT, nullable=True)
     ingredient6 = db.Column(db.TEXT, nullable=True)
     servings = db.Column(db.INTEGER, default=0)
     prep_time = db.Column(db.FLOAT, default=0, comment='Preparation time in minutes')
     cooking_time = db.Column(db.FLOAT, default=0, comment='Cooking time in minutes')
     calories = db.Column(db.INTEGER, default=0)
     content = db.Column(db.TEXT, nullable=False)
     create_time = db.Column(db.DateTime, default=datetime.datetime.now)
     update_time = db.Column(db.DateTime, default=datetime.datetime.now)
     read_times = db.Column(db.INTEGER, default=0)
     # 用户对帖子的操作
     likes = db.Column(db.INTEGER, default=0, comment='like post persons')
     comment_num = db.Column(db.INTEGER, default=0, comment='comment numbers')
     
     # 外键id
     author_id = db.Column(db.INTEGER, db.ForeignKey('t_user.id'))
     
     # 用户关系
     user = db.relationship('User', back_populates='posts')

     @hybrid_property
     def score(self):
        return 2 * self.comment_num + self.likes

     @score.expression
     def score(cls):
        return 2 * cls.comment_num + cls.likes
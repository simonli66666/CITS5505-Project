import datetime
from sqlalchemy.ext.hybrid import hybrid_property

from bbs.extensions import db
from bbs.extensions import event
from flask_login import UserMixin

likes_table = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('t_user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('t_post.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 't_user'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, index=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, index=True, unique=True, comment='user name')
    nickname = db.Column(db.String(40), nullable=False, unique=True, comment='user nick name')
    password = db.Column(db.String(256), comment='user password')
    create_time = db.Column(db.DATETIME, default=datetime.datetime.now)
    gender = db.Column(db.String(6))  # "male" or "female"
    age = db.Column(db.Integer)
    mobile = db.Column(db.String(15))
    email = db.Column(db.String(120))
    signature = db.Column(db.Text)
    post_num = db.Column(db.INTEGER, default=0, comment='Number of posts made by the user')
    badges = db.Column(db.INTEGER, default=20)
    like_num = db.Column(db.INTEGER, default=0)
    selflike_num = db.Column(db.INTEGER, default=0)
    posts = db.relationship('Post', back_populates='user')
    liked_posts = db.relationship('Post', secondary=likes_table, 
                                   back_populates='likers',  
                                  lazy='dynamic')
    selfcomment_num = db.Column(db.INTEGER, default=0)
    user_likes = db.relationship('Like', back_populates='user', lazy='dynamic')

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
     likes_num = db.Column(db.INTEGER, default=0, comment='like post persons')
     comment_num = db.Column(db.INTEGER, default=0, comment='comment numbers')
     
     # 外键id
     author_id = db.Column(db.INTEGER, db.ForeignKey('t_user.id'))
     
     # 用户关系
     user = db.relationship('User', back_populates='posts')
     likes = db.relationship('Like', back_populates='post', lazy='dynamic')
     likers = db.relationship('User', secondary=likes_table, back_populates='liked_posts', lazy='dynamic')
     @hybrid_property
     def score(self):
        return 2 * self.comment_num + self.likes_num

     @score.expression
     def score(cls):
        return 2 * cls.comment_num + cls.likes_num
     


class Like(db.Model):
    __tablename__ = 't_like'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    
    timestamps = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.INTEGER, db.ForeignKey('t_user.id'))
    post_id = db.Column(db.INTEGER, db.ForeignKey('t_post.id'))
    user = db.relationship('User', back_populates='user_likes', lazy='joined')
    post = db.relationship('Post', back_populates='likes', lazy='joined')
     
@event.listens_for(Post, 'after_insert')
def increment_post_num(mapper, connection, target):
    user = db.session.query(User).get(target.author_id)
    if user:
        user.post_num += 1
        db.session.commit()

@event.listens_for(Post, 'after_delete')
def decrement_post_num(mapper, connection, target):
    user = db.session.query(User).get(target.author_id)
    if user:
        user.post_num -= 1
        db.session.commit()

@event.listens_for(Post.likes, 'set')
def update_total_likes(target, value, oldvalue, initiator):
    if value != oldvalue:  # Check if the likes have actually changed
        user = db.session.query(User).get(target.author_id)
        if user:
            # Adjust the user's like_num only if the old value is set (i.e., not None or similar)
            if oldvalue is not None:
                user.like_num += (value - oldvalue)
            else:
                user.like_num += value
            db.session.commit()
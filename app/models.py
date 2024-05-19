import datetime
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions import *
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Association table for many-to-many relationship between users and posts (likes)
likes_table = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('t_user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('t_post.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 't_user'

    id = db.Column(db.INTEGER, primary_key=True, nullable=False, index=True, autoincrement=True)
    username = db.Column(db.String(40), nullable=False, index=True, unique=True)
    nickname = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(256))
    create_time = db.Column(db.DATETIME, default=datetime.datetime.now)
    gender = db.Column(db.String(6))  # "male" or "female"
    age = db.Column(db.Integer)
    mobile = db.Column(db.String(15))
    email = db.Column(db.String(120))
    signature = db.Column(db.Text)
    post_num = db.Column(db.INTEGER, default=0, comment='Number of posts made by the user')
    posts = db.relationship('Post', back_populates='user')
    liked_posts = db.relationship('Post', secondary=likes_table, back_populates='likers', lazy='dynamic')
    user_likes = db.relationship('Like', back_populates='user', lazy='dynamic')
    comments = db.relationship('Comments', back_populates='author')
    
    
    # Hybrid property for the number of comments made by the user
    @hybrid_property
    def selfcomment_num(self):
        return len(self.comments)

    @selfcomment_num.expression
    def selfcomment_num(cls):
        return (
            select([func.count(Comments.id)])
            .where(Comments.author_id == cls.id)
            .label("selfcomment_num")
        )

    # Hybrid property for the number of likes the user has given
    @hybrid_property
    def selflike_num(self):
        return self.user_likes.count()

    @selflike_num.expression
    def selflike_num(cls):
        return (
            select([func.count(Like.id)])
            .where(Like.user_id == cls.id)
            .label("selflike_num")
        )

    # Hybrid property for the number of likes received by the user's posts
    @hybrid_property
    def like_num(self):
        return (
            db.session.query(func.count(Like.id))
            .join(Post, Like.post_id == Post.id)
            .filter(Post.author_id == self.id)
            .scalar()
        )

    @like_num.expression
    def like_num(cls):
        return (
            select([func.count(Like.id)])
            .join(Post, Like.post_id == Post.id)
            .where(Post.author_id == cls.id)
            .label("like_num")
        )

    # Hybrid property for the number of posts made by the user
    @hybrid_property
    def post_num(self):
        return len(self.posts)

    @post_num.expression
    def post_num(cls):
        return (
            select([func.count(Post.id)])
            .where(Post.author_id == cls.id)
            .label("post_num")
        )

    # Hybrid property for the number of comments on the user's posts
    @hybrid_property
    def comment_num(self):
        return (
            db.session.query(func.count(Comments.id))
            .join(Post, Comments.post_id == Post.id)
            .filter(Post.author_id == self.id)
            .scalar()
        )

    @comment_num.expression
    def comment_num(cls):
        return (
            select([func.count(Comments.id)])
            .join(Post, Comments.post_id == Post.id)
            .where(Post.author_id == cls.id)
            .label("comment_num")
        )
    
    # Hybrid property for calculating user badges
    @hybrid_property
    def badges(self):
        return 20 + self.post_num * 5 + self.like_num * 2 + self.comment_num * 2 + self.selfcomment_num * 2

    @badges.expression
    def badges(cls):
        return (
            20 +
            (select([func.count(Post.id)]) .where(Post.author_id == cls.id) * 5) +
            (select([func.count(Like.id)]) .join(Post, Like.post_id == Post.id) .where(Post.author_id == cls.id) * 2) +
            (select([func.count(Comments.id)]) .join(Post, Comments.post_id == Post.id) .where(Post.author_id == cls.id) * 2) +
            (select([func.count(Comments.id)]) .where(Comments.author_id == cls.id) * 2)
        )
    
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
    likes_num = db.Column(db.INTEGER, default=0, comment='Number of likes on the post')
    comment_num = db.Column(db.INTEGER, default=0, comment='Number of comments on the post')
    
    # Foreign key for the author of the post
    author_id = db.Column(db.INTEGER, db.ForeignKey('t_user.id'))
    
    # Relationships with other models
    user = db.relationship('User', back_populates='posts')
    likes = db.relationship('Like', back_populates='post', lazy='dynamic')
    likers = db.relationship('User', secondary=likes_table, back_populates='liked_posts', lazy='dynamic')
    comments = db.relationship('Comments', back_populates='post')

    # Hybrid property for calculating the score of the post
    @hybrid_property
    def score(self):
        return self.read_times + 2 * self.likes_num

    @score.expression
    def score(cls):
        return cls.read_times + 2 * cls.likes_num

class Like(db.Model):
    __tablename__ = 't_like'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    timestamps = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.INTEGER, db.ForeignKey('t_user.id'))
    post_id = db.Column(db.INTEGER, db.ForeignKey('t_post.id'))
    user = db.relationship('User', back_populates='user_likes', lazy='joined')
    post = db.relationship('Post', back_populates='likes', lazy='joined')

class Comments(db.Model):
    __tablename__ = 't_comments'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    body = db.Column(db.Text)
    timestamps = db.Column(db.DATETIME, default=datetime.datetime.now)
    author_id = db.Column(db.INTEGER, db.ForeignKey('t_user.id'))
    post_id = db.Column(db.INTEGER, db.ForeignKey('t_post.id'))
    replied_id = db.Column(db.INTEGER, db.ForeignKey('t_comments.id'))

    post = db.relationship('Post', back_populates='comments')
    author = db.relationship('User', back_populates='comments')
    replies = db.relationship('Comments', back_populates='replied', cascade='all')
    replied = db.relationship('Comments', back_populates='replies', remote_side=[id])




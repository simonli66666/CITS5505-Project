from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, select, func
from sqlalchemy.orm import scoped_session, sessionmaker

db = SQLAlchemy()
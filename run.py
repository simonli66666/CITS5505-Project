from flask_migrate import Migrate
from app import create_app
from app.extensions import db
from app.setting import DevelopmentConfig

app = create_app(DevelopmentConfig)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(port=5000)
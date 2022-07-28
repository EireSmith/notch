from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "notch_database.db"


def create_app():
    app = Flask(__name__)
    app.secret_key = '324390jgf19didqjw0jifwv'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  #locating the databse (sqlite, old) 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hbrbxqjsftpeze:3df463dcea0a49b379e4fa92c63f92e18f663ed18d6bdaee02db6189bd207e6e@ec2-54-246-185-161.eu-west-1.compute.amazonaws.com:5432/d8jdbjj2rah3lt'  #locating the databse 

    db.init_app(app)

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/') #leaving the prefix as small as possible
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #looks for primary key

    return app

# def create_database(app):
#      if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Database Created')


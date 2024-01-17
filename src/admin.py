import os
from flask_admin import Admin
from models import db, User, Item,  Character, Vehicle, Characters, Planet, User_Favorite
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.config['SECRET_KEY'] = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example, this is how we add the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Item, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Vehicle, db.session))
    admin.add_view(ModelView(User_Favorite, db.session))
    admin.add_view(ModelView(Characters, db.session))
    # You can duplicate that line to add new models
    # admin.add_view(ModelView(YourModelName, db.session))

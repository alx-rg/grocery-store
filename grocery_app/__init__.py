from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from grocery_app.models import User
from grocery_app.extensions import app

login = LoginManager()
login.login_view = 'auth.login'
login.init_app(app)

@login.user_loader
def load_user(user_id):
  return User.query.get(user_id)

bcrypt = Bcrypt(app)
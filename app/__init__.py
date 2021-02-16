from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
from app.auth.blacklist_token_model import BlacklistToken
from app.auth.refresh_token_model import RefreshToken
from app.users.model import User
from app.wiki.model import WikiPage
from app.terms.model import Term
# db.init_app(app)

#
# USE COMMAND flask run TO RUN THE SCRIPT
#

# db.create_all() after any changes in models

db.create_all()
migrate = Migrate(app, db, ssl_context='adhoc')

from app import routes

if __name__ == '__main__':
    app.run(debug=True)

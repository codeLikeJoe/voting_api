from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from lib.core.config import mail_config, database_config
from lib.core.blueprints import register_blueprints
from lib.core.error_handlers import method_not_allowed, not_found

app = Flask(__name__)

# Mail Configration
app.config.update(mail_config())
app.config.update(database_config())

# Initialize MySQL and Bcrypt
mysql = MySQL(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# Extensions
app.extensions['mysql'] = mysql
app.extensions['bcrypt'] = bcrypt
app.extensions['mail'] = mail

# Error handlers
app.errorhandler(405)(method_not_allowed)
app.errorhandler(404)(not_found)

# Blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)

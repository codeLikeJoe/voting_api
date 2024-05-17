# from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from config import mail_config, database_config
from register_blueprints import register_blueprints
from error_handlers import method_not_allowed, not_found
# import os


app = Flask(__name__)

# load_dotenv()
# secretKey = os.getenv("API_SECRET")


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

# Assuming current_time and expire are already defined as datetime objects
# current_time = datetime.now()
# expire = current_time + timedelta(minutes=60)

# Convert current_time to milliseconds
# current_time_ms = current_time.timestamp() * 1000
# print(f"Current Time in milliseconds: {current_time_ms}")

# Convert expire to milliseconds
# expire_ms = expire.timestamp() * 1000
# print(f"Expire Time in milliseconds: {expire_ms}")

if __name__ == '__main__':
    app.run(debug=True)

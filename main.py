from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from register import register # Import the blueprint object

app = Flask(__name__)

# Configure your application
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "users_db"
app.config['SECRET_KEY'] = 'thisisasecretkey'


# Initialize MySQL and Bcrypt
mysql = MySQL(app)
bcrypt = Bcrypt(app)
app.extensions['mysql'] = mysql
app.extensions['bcrypt'] = bcrypt

# Register the blueprint
app.register_blueprint(register)

if __name__ == '__main__':
    app.run(debug=True)

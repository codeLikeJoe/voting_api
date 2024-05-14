from authentications.Registration.register import register as register_blueprint
from manageUsers.getAllUsers import getUsers as getUsers_blueprint
from manageUsers.getUserByIds import getUserId as getUserId_blueprint
from manageUsers.getUserByEmails import getUserEmail as getUserEmail_blueprint
from authentications.Registration.verifyAccount import verify_user as verify_user_blueprint
from authentications.login import signInUser as signInUser_blueprint
from home import home as home_blueprint
from authentications.Registration.validate_otp import validate_otp as validate_otp_blueprint
from authentications.ForgotPassword.forgot_password import forgot_password as forgot_password_blueprint
from authentications.ForgotPassword.validate_forgot_password_otp import validate_reset_password_otp as validate_reset_password_otp_blueprint
from authentications.ForgotPassword.reset_password import reset_password as reset_password_blueprint

# Register the blueprints
def register_blueprints(app):
    app.register_blueprint(register_blueprint)
    app.register_blueprint(getUsers_blueprint)
    app.register_blueprint(getUserId_blueprint)
    app.register_blueprint(getUserEmail_blueprint)
    app.register_blueprint(verify_user_blueprint)
    app.register_blueprint(signInUser_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(validate_otp_blueprint)
    app.register_blueprint(forgot_password_blueprint)
    app.register_blueprint(validate_reset_password_otp_blueprint)
    app.register_blueprint(reset_password_blueprint)

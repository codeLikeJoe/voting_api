from Authentications.Registration.register import register as register_blueprint
from manageUsers.getAllUsers import getUsers as getUsers_blueprint
from manageUsers.getUserByIds import getUserId as getUserId_blueprint
from manageUsers.getUserByEmails import getUserEmail as getUserEmail_blueprint
from Authentications.Registration.verifyAccount import verify_user as verify_user_blueprint
from Authentications.login import signInUser as signInUser_blueprint
from home import home as home_blueprint
from Authentications.Registration.validate_otp import validate_otp as validate_otp_blueprint

from Authentications.Registration.register_student import register_student as register_student_blueprint
from Authentications.Registration.verify_student import verify_student as verify_student_blueprint

from Authentications.ForgotPassword.forgot_password import forgot_password as forgot_password_blueprint
from Authentications.ForgotPassword.validate_forgot_password_otp import validate_reset_password_otp as validate_reset_password_otp_blueprint
from Authentications.ForgotPassword.reset_password import reset_password as reset_password_blueprint
from Candidate.apply_for_position import apply_position as apply_position_blueprint

from programs.add_programs import add_program as add_program_blueprint
from programs.manage_programs import program as program_blueprint
from programs.get_program import get_programs as get_programs_blueprint

# Register the blueprints
def register_blueprints(app):
    # app.register_blueprint(register_blueprint)
    app.register_blueprint(getUsers_blueprint)
    app.register_blueprint(getUserId_blueprint)
    app.register_blueprint(getUserEmail_blueprint)
    app.register_blueprint(signInUser_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(validate_otp_blueprint)
    app.register_blueprint(forgot_password_blueprint)
    app.register_blueprint(validate_reset_password_otp_blueprint)
    app.register_blueprint(reset_password_blueprint)
    app.register_blueprint(apply_position_blueprint)

    # student registration
    app.register_blueprint(register_student_blueprint)
    app.register_blueprint(verify_student_blueprint)
    app.register_blueprint(verify_user_blueprint)

    # for programs
    app.register_blueprint(add_program_blueprint)
    app.register_blueprint(program_blueprint)
    app.register_blueprint(get_programs_blueprint)

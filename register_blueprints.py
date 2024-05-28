from lib.manageUsers.getAllUsers import getUsers as getUsers_blueprint
from lib.manageUsers.getUserByIds import getUserId as getUserId_blueprint
from lib.manageUsers.getUserByEmails import getUserEmail as getUserEmail_blueprint

from lib.home import home as home_blueprint

# add student
from lib.Authentications.Registration.register_student import register_student as register_student_blueprint
from lib.Authentications.Registration.verify_student import verify_student as verify_student_blueprint
from lib.Authentications.Registration.verifyAccount import verify_user as verify_user_blueprint

from lib.Authentications.login import signInUser as signInUser_blueprint

# managing passwords
from lib.Authentications.ManagePassword.forgot_password import forgot_password as forgot_password_blueprint
from lib.Authentications.ManagePassword.validate_forgot_password_otp import validate_reset_password_otp as validate_reset_password_otp_blueprint
from lib.Authentications.ManagePassword.reset_password import reset_password as reset_password_blueprint

from lib.Candidate.apply_for_position import apply_position as apply_position_blueprint

# programs
from lib.programs.add_programs import add_program as add_program_blueprint
from lib.programs.manage_programs import program as program_blueprint
from lib.programs.get_program import get_programs as get_programs_blueprint

# admin
from lib.admin.add_admin import add_admin as add_admin_blueprint

# Register the blueprints
def register_blueprints(app):
    # login
    app.register_blueprint(signInUser_blueprint)

    app.register_blueprint(getUsers_blueprint)
    app.register_blueprint(getUserId_blueprint)
    app.register_blueprint(getUserEmail_blueprint)

    app.register_blueprint(home_blueprint)
    app.register_blueprint(apply_position_blueprint)

    # student registration
    app.register_blueprint(register_student_blueprint)
    app.register_blueprint(verify_student_blueprint)
    app.register_blueprint(verify_user_blueprint)

    # password management
    app.register_blueprint(forgot_password_blueprint)
    app.register_blueprint(validate_reset_password_otp_blueprint)
    app.register_blueprint(reset_password_blueprint)

    # programs
    app.register_blueprint(add_program_blueprint)
    app.register_blueprint(program_blueprint)
    app.register_blueprint(get_programs_blueprint)

    # admin
    app.register_blueprint(add_admin_blueprint)
    

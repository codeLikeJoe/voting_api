from lib.manageUsers.getAllUsers import getUsers as getUsers_blueprint
from lib.manageUsers.getUserByIds import getUserId as getUserId_blueprint
from lib.manageUsers.getUserByEmails import getUserEmail as getUserEmail_blueprint

from lib.home import home as home_blueprint

# add student
from lib.authentications.verify_otp import verify_otp as verify_otp_blueprint
from lib.authentications.register_student import register_student as register_student_blueprint
from lib.authentications.send_otp import verify_user as verify_user_blueprint

from lib.authentications.login import signInUser as signInUser_blueprint

# managing passwords
from lib.authentications.change_password import change_password as change_password_blueprint
from lib.authentications.reset_password import reset_password as reset_password_blueprint

from lib.Candidate.apply_for_position import apply_position as apply_position_blueprint

# programs
from lib.programs.add_programs import add_program as add_program_blueprint
from lib.programs.edit_programs import program as program_blueprint
from lib.programs.programs import get_programs as get_programs_blueprint

# admin
from lib.admin.add_admin import add_admin as add_admin_blueprint

# elections
from lib.Elections.create_elections import create_elections as create_elections_blueprint
from lib.Elections.edit_elections import edit_elections as edit_elections_blueprint
from lib.Elections.elections import elections as elections_blueprint

# positions
from lib.Positions.positions import positions as positions_blueprint 
from lib.Positions.create_positions import create_positions as create_positions_blueprint 
from lib.Positions.edit_position import edit_positions as edit_positions_blueprint 

# roles
from lib.Roles.add_roles import adding_roles as add_roles_blueprint
from lib.Roles.roles import roles as roles_blueprint
from lib.Roles.edit_roles import edit_roles as edit_roles_blueprint

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
    app.register_blueprint(verify_otp_blueprint)
    app.register_blueprint(verify_user_blueprint)

    # password management
    app.register_blueprint(change_password_blueprint)
    app.register_blueprint(reset_password_blueprint)

    # programs
    app.register_blueprint(add_program_blueprint)
    app.register_blueprint(program_blueprint)
    app.register_blueprint(get_programs_blueprint)

    # admin
    app.register_blueprint(add_admin_blueprint)

    # elections
    app.register_blueprint(create_elections_blueprint)
    app.register_blueprint(edit_elections_blueprint)
    app.register_blueprint(elections_blueprint)

    # positions
    app.register_blueprint(positions_blueprint)
    app.register_blueprint(create_positions_blueprint)
    app.register_blueprint(edit_positions_blueprint)

    # roles
    app.register_blueprint(add_roles_blueprint)
    app.register_blueprint(roles_blueprint)
    app.register_blueprint(edit_roles_blueprint)
    

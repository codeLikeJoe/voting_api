from flask import Blueprint, request, jsonify, current_app

verifyUserAccount = Blueprint('verify_user_account', __name__)

@verifyUserAccount.route('/verifyUser', methods = ['POST'])
def verify():
    email = request.form['email']

    try:
        user = User.query.filter_by(email=email).first()

        if user:
            if user.verified == 'No':
                # expiration = datetime.utcnow() + timedelta(minutes=40)
                # token = jwt.encode({
                #             'user': user.username,
                #             'email': request.form['email'],
                #             'exp': expiration,
                #         }, app.config['SECRET_KEY'], algorithm="HS256")
                user.verified = 'Yes'
                db.session.add(user)
                db.session.commit()
                return jsonify({"user":user.username, "verified": "Yes"})
            elif user.verified == 'Yes':
                return jsonify({"message":"This email has been verified already."})
        else:
            return jsonify({"message": "User with this email does not exist."})
    except Exception as e: 
        print("Error: ", e)
        return jsonify({"error":"sorry, an error occured"})       

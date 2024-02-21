from flask import Blueprint, request, jsonify, session
from app.models.models import db, User
from app.utils.helper import is_valid_email, is_valid_phone
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth',__name__)

bcrypt = Bcrypt()

@auth_bp.route('/', methods=['GET'])
def auth():
    return {'response':'Auth Route'},200

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            user_data = request.get_json()
            if "first_name" not in user_data or not user_data["first_name"]:
                return jsonify({"error": "First name is required"}), 400
            if "last_name" not in user_data or not user_data["last_name"]:
                return jsonify({"error": "Last name is required"}), 400
            if "email" not in user_data or not is_valid_email(user_data["email"]):
                return jsonify({"error": "Invalid Email Address"}), 400
            if "phone" not in user_data or not is_valid_phone(user_data["phone"]):
                return jsonify({"error": "Invalid Phone Number"}), 400
            if "password" not in user_data or not user_data["password"]:
                return jsonify({"error": "Password is required"}), 400
            user_exists = (
                User.query.filter_by(email=user_data["email"]).first() is not None
            )
            if user_exists:
                return jsonify({"error": "Email already in use"}), 400
            hashed_password = bcrypt.generate_password_hash(
                password=user_data["password"].encode("utf-8")
            ).decode("utf-8")
            new_user = User(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
                phone_number=user_data["phone"],
                password=hashed_password,
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify(
                {
                    "message": "registered successfully",
                    "user_data": {
                        "id": new_user.id,
                        "first_name": user_data["first_name"],
                        "last_name": user_data["last_name"],
                        "email": user_data["email"],
                        "phone_number": user_data["phone"],
                    },
                }
            )
        except:
            return jsonify({"error": "Something Went Wrong"}), 500
    else:
        return {"message": "signup route"}


@auth_bp.route("/login", methods=["POST",'GET'])
def login():
    if request.method == "POST":
        try:
            user_data = request.get_json()
            if "email" not in user_data or not user_data["email"]:
                return jsonify({"error": "Invalid Email"}), 401
            if "password" not in user_data or not user_data["password"]:
                return jsonify({"error": "Invalid Password"}), 401
            user = User.query.filter_by(email=user_data["email"]).first()
            if user is None:
                return jsonify({"error": "Invalid Credentials"}), 401
            if not bcrypt.check_password_hash(user.password, user_data["password"]):
                return jsonify({"error": "Invalid Credentials"}), 401
            session["user_id"] = user.id
            return jsonify(
                {
                    "message": "User logged In",
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "phone": user.phone_number,
                    },
                }
            )
        except Exception as e:
            print(e)
            return jsonify({"error": "Something went wrong"}), 500
    return {

        'message':'login route'
    }


@auth_bp.route("/check-auth")
def isUserLoggedIn():
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
        return jsonify(
            {
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone_number,
                }
            }
        )
    else:
        return jsonify({"message": "Unauthorized"})


@auth_bp.route("/logout", methods=["POST"])
def logout():
    if request.method == "POST":
        if "user_id" in session:
            session.pop("user_id")
            return {"status":"success","message": "Logged Out "},200
        else:
            return {"status":"error","message": "Unauthorized"},401
    else:
        return {"message": "Unauthorized"}, 401



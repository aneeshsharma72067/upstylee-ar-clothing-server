from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models import db, User
from config import ApplicationConfig
from validate_email_address import validate_email
from re import match
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
bcrypt = Bcrypt(app)
server_session = Session(app)
db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()


def is_valid_email(email):
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return validate_email(email) and match(email_pattern, email) is not None


def is_valid_phone(phone):
    return len(phone) == 10 and phone.isdigit()


# API Routes
@app.route("/api")
def index():
    return {
        "message": "Upstylee API",
        "routeList": {
            "Login Route": "/api/login",
            "Signup Route": "/api/register",
            "List of Users": "/api/users",
        },
    }


@app.route("/api/test")
def test():
    return {"test_result": "success"}


# Users and Authentication
@app.route("/api/register", methods=["GET", "POST"])
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


@app.route("/api/login", methods=["POST"])
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
        except:
            return jsonify({"error": "Something went wrong"}), 500
    # return {

    #     'message':'login route'
    # }


@app.route("/api/check-auth")
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


@app.route("/api/logout", methods=["POST"])
def logout():
    if request.method == "POST":
        if "user_id" in session:
            session.pop("user_id")
            return {"message": "success"}
        else:
            return {"message": "Unauthorized"}
    else:
        return {"message": "Unauthorized"}


@app.route("/api/users/<user_id>", methods=["GET", "DELETE"])
def usersList(user_id):
    if request.method == "DELETE":
        user_to_delete = User.query.get(user_id)
        if user_to_delete is not None:
            db.session.delete(user_to_delete)
            db.session.commit()
            return (
                jsonify({"message": f"User {user_to_delete.id} deleted successfully"}),
                200,
            )
        else:
            return jsonify({"error": "User does not exists"}), 500
    elif request.method == "GET":
        user = User.query.get(user_id)
        return jsonify(
            {
                "user_data": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                }
            }
        )


@app.route("/api/users")
def getAllUsers():
    user_list = User.query.all()
    users = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
        }
        for user in user_list
    ]
    return jsonify({"user_count": len(user_list), "users": users})


# Products


@app.route("/api/products/<id>")
def getAllProducts(id):
    return "product"


if __name__ == "__main__":
    app.run(debug=True)

from flask import Blueprint, jsonify, request
from app.models.models import db, User

users_bp = Blueprint('users',__name__)

@users_bp.route("/<user_id>", methods=["GET", "DELETE"])
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


@users_bp.route("/")
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


@users_bp.route('/delete-all')
def deleteAllUsers():
    try:
        db.session.query(User).delete()
        db.session.commit();
        return {'status':'success','message':'All User objects deleted successfully'}
    except Exception as e:
        db.session.rollback();
        return {'status':'error','message':f'An error occured : {e}'}
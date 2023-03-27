from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from passlib.hash import pbkdf2_sha256

from db import db

from models import UserModel
from models.schema import UserSchema, RegisterUserSchema
from flask import request


blp = Blueprint("Users", "users", url_prefix='/api', description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.response(200, UserSchema)
    @blp.arguments(RegisterUserSchema)
    def post(self, user_data):

        print(request.headers)
        if UserModel.find_by_email(user_data["email"]):
            abort(400, message="A user with that email already exists.")

        if UserModel.find_by_phone(user_data["phone_number"]):
            abort(400, message="A user with that phone number already exists.")
        try:
            user = UserModel(
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone_number=user_data["phone_number"],
                password=pbkdf2_sha256.hash(user_data["password"]),
            )
            user.save_to_db()
            return user, 201
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the user.")





@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")
        return user

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.find_by_id(user_id)

        if user:
            user = UserModel(id=user_id, **user_data)
            user.save_to_db()
        else:
            abort(404, message="User not found.")
        return user

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")
        user.delete_from_db()
        return {"message": "User deleted."}, 200

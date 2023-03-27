from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from passlib.hash import pbkdf2_sha256

from db import db

from models import AccountModel
from models.schema import ExtAccountSchema, BaseAccountSchema, CreateAccountSchema
from flask import request
from .decorators import authorize


blp = Blueprint("Accounts", "accounts", url_prefix='/api', description="Operations on Accounts")



@blp.route("/accounts")
class AccountList(MethodView):
    @authorize
    @blp.response(200, BaseAccountSchema(many=True))
    def get(self):
        return AccountModel.query.all()


    @authorize
    @blp.arguments(CreateAccountSchema)
    @blp.response(201, ExtAccountSchema)
    def post(self, account_data):
        account = AccountModel(**account_data)
        try:
            db.session.add(account)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="An account with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the account.")

        return account


@blp.route("/accounts/<string:account_id>")
class Account(MethodView):
    @authorize
    @blp.response(200, ExtAccountSchema)
    def get(self, account_id):
        account = AccountModel.query.get_or_404(account_id)
        return account

    @authorize
    def delete(self, account_id):
        account = AccountModel.query.get_or_404(account_id)
        db.session.delete(account)
        db.session.commit()
        return {"message": "Account deleted"}, 200

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from passlib.hash import pbkdf2_sha256

from db import db

from models import TransactionModel, AccountModel
from models.schema import BaseTransactionSchema, ExtTransactionSchema, CreateTransactionSchema
from flask import request
from .utils import get_ip
from .decorators import authorize



blp = Blueprint("Transactions", "accounts", url_prefix='/api', description="Operations on Transactions")



@blp.route("/accounts/<string:account_id>/transactions")
class Transaction(MethodView):
    @authorize
    @blp.response(200, ExtTransactionSchema(many=True))
    def get(cls, account_id):
        the_account = AccountModel.find_by_id(account_id)
        if not the_account:
            abort(400, message="Account Holder does not exist")

        all_account_trans = the_account.transactions

        ROWS_PER_PAGE = 5
        page = request.args.get('page', 1, type = int)
        search = request.args.get('search', None, type = str)

        if search:
            # all_account_trans = [trans for trans in the_account.transactions if trans.description == search]
            all_account_trans = TransactionModel.query.with_parent(the_account).filter_by(description=search)
            print(all_account_trans)

        transactions = all_account_trans.paginate(page = page, per_page =ROWS_PER_PAGE)
        return transactions.items

    @authorize
    @blp.arguments(CreateTransactionSchema)
    @blp.response(201, ExtTransactionSchema)
    def post(self, trans_data, account_id):
        the_account = AccountModel.find_by_id(account_id)
        if not the_account:
            abort(400, message="Account Holder does not exist")

        request_ip = get_ip()
        print(request_ip)
        transaction = TransactionModel(**trans_data, ip=request_ip, account_id=account_id)
        if transaction.trans_type == "debit":
            the_account.balance = abs(int(the_account.balance - transaction.amount))
        elif transaction.trans_type == "credit":
            the_account.balance = abs(int(the_account.balance + transaction.amount))

        try:
            transaction.save_to_db()
            the_account.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return transaction

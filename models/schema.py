from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.UUID()
    # id = fields.Integer()
    email = fields.Email()
    first_name = fields.Str()
    last_name = fields.Str()
    phone_number = fields.Str()
    password = fields.Str(load_only=True)


class RegisterUserSchema(Schema):
    email = fields.Email()
    first_name = fields.Str()
    last_name = fields.Str()
    phone_number = fields.Str()
    password = fields.Str(load_only=True)


class BaseAccountSchema(Schema):
    id = fields.UUID()
    # id = fields.Integer()
    account_name = fields.Str()
    balance = fields.Integer()

class CreateAccountSchema(Schema):
    account_name = fields.Str()


class BaseTransactionSchema(Schema):
    id = fields.UUID()
    # id = fields.Integer()
    trans_type = fields.Str()
    amount = fields.Integer()
    description = fields.Str()
    ip = fields.Str()

class CreateTransactionSchema(Schema):
    trans_type = fields.Str()
    amount = fields.Integer()
    description = fields.Str()



class ExtTransactionSchema(BaseTransactionSchema):
    account_id = fields.UUID(required=True, load_only=True)
    account = fields.Nested(BaseAccountSchema(), dump_only=True)


class ExtAccountSchema(BaseAccountSchema):
    transactions = fields.List(fields.Nested(lambda: BaseTransactionSchema()), dump_only=True)
    trans_count = fields.Method("get_trans_count")

    def get_trans_count(self, obj):
        return obj.transactions.count()

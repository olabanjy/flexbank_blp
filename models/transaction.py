from uuid import uuid4
from db import db
import enum

class TransType(enum.Enum):
    DEBIT='debit'
    CREDIT='credit'





class TransactionModel(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid4)
    # id = db.Column(db.Integer, primary_key=True)
    trans_type = db.Column(
        db.Enum(TransType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=TransType.CREDIT.value,
        server_default=TransType.CREDIT.value
    )
    amount = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(80), nullable=False)
    ip = db.Column(db.String(80), nullable=False)

    account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id"), unique=False, nullable=False
    )

    account = db.relationship("AccountModel", back_populates="transactions")


    def json(self):
        return {
            "id": self.id,
            "trans_type": self.trans_type,
            "amount": self.amount,
            "account_id": self.account_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




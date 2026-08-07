from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.main.api.db.models.transaction_table import Transaction

class TransactionCrudDb:
    @staticmethod
    def get_last_transaction_by_from_account_id(db: Session, from_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=from_account_id).order_by(desc(Transaction.id)).first()
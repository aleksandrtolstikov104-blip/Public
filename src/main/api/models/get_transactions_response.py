from typing import List
from src.main.api.models.base_model import BaseModel


class Transaction(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: int
    toAccountId: int
    createdAt: str

class GetTransactionsResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: List[Transaction]
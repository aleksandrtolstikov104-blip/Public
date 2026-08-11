from typing import List
from src.main.api.models.base_model import BaseModel

class CreditHistoryItem(BaseModel):
    creditId: int
    accountId: int
    amount: float
    termMonths: int
    balance: float
    createdAt: str

class GetHistoryCreditResponse(BaseModel):
    userId: int
    credits: List[CreditHistoryItem]
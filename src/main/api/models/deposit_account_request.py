from typing import Annotated
from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel

class DepositAccountRequest(BaseModel):
    accountId: Annotated[int, CreationRule(regex=r"^\d{3}$")]
    amount: Annotated[float, CreationRule(regex="^([1-8]\d{3}\.\d{2}|9000\.00)$")]
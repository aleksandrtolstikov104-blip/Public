from typing import Annotated

from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel

class CreditRequest(BaseModel):
    accountId: int
    amount: Annotated[float, CreationRule(regex=r"^([5-9]\d{3}|1[0-4]\d{3}\.\d{2}|15000\.00)$")]
    termMonths:Annotated[int, CreationRule(regex=r"^(12|24|36|48|60)$")]
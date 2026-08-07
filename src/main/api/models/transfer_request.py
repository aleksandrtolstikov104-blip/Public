from typing import Annotated
from src.main.api.models.base_model import BaseModel
from src.main.api.generators.creation_rule import CreationRule

class TransferRequest(BaseModel):
    fromAccountId: int = 0
    toAccountId: int = 0
    amount: Annotated[float, CreationRule(regex=r"^(500\.00|[5-9]\d{2}\.\d{2}|1000\.00)$")]
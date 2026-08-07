import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account

@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest, db_session: Session):

        response = api_manager.user_steps.deposit_account(create_user_request ,deposit_account_request)

        assert deposit_account_request.amount == response.balance
        assert deposit_account_request.accountId == response.id
        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db is not None, "Аккаунт не создан, id аккаунта нет в БД"
        assert account_from_db.balance == response.balance, "Баланс в БД не совпадает с ответом API"


    @pytest.mark.parametrize("amount",[999, 9001, 0, -199])
    def test_deposit_account_invalid_amount(self, api_manager: ApiManager, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest, amount: float, db_session: Session):
        deposit_account_request.amount = amount
        api_manager.user_steps.deposit_account_invalid(create_user_request ,deposit_account_request)

        account_from_db = Account.get_account_by_id(db_session, deposit_account_request.accountId)
        assert account_from_db is not None, "Аккаунт не создан, id аккаунта нет в БД"
        assert account_from_db.balance == 0, f"Ошибка. Баланс изменился при невалидном запросе. Текущий баланс: {account_from_db.balance}"
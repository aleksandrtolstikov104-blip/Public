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

        assert deposit_account_request.amount == response.balance, f"Ошибка! Баланс в ответе API ({response.balance}) не совпадает с суммой пополнения ({deposit_account_request.amount})"
        assert deposit_account_request.accountId == response.id, f"Ошибка! ID аккаунта в ответе API ({response.id}) не совпадает с запрошенным ({deposit_account_request.accountId})"

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, f"Ошибка! Аккаунт с id={response.id} не найден в БД или ID не совпадает"
        assert account_from_db.balance == response.balance, f"Ошибка! Баланс в БД ({account_from_db.balance}) не совпадает с ответом API ({response.balance})"



    @pytest.mark.parametrize("amount",[999, 9001, 0, -199])
    def test_deposit_account_invalid_amount(self, api_manager: ApiManager, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest, amount: float, db_session: Session):
        deposit_account_request.amount = amount
        api_manager.user_steps.deposit_account_invalid(create_user_request ,deposit_account_request)

        account_from_db = Account.get_account_by_id(db_session, deposit_account_request.accountId)
        assert account_from_db.id == deposit_account_request.accountId, f"Ошибка! Аккаунт с id={deposit_account_request.accountId} не найден в БД"
        assert account_from_db.balance == 0, f"Ошибка! Баланс ошибочно изменился при невалидном пополнении на сумму {amount}. Ожидалось: 0, фактически в БД: {account_from_db.balance}"
import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.transfer_request import TransferRequest

"""
1)логинимся админом +
2)создаем 1 пользователя +
3)логинимся 1 польз +
4) создаем счет1 +
5) создаем счет2 +
6) пополняем счет 1 + deposit
7) переводим с 1 (transfer_in) счета на 2 (transfer_out) +
8) asserts к 7 пункту.+
"""

@pytest.mark.api
class TestTransferAccount:
    def test_transfer_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, deposit_account_response: DepositAccountResponse, transfer_request: TransferRequest, db_session: Session):
        response = api_manager.user_steps.transfer(create_user_request, transfer_request)

        assert transfer_request.fromAccountId == response.fromAccountId
        assert transfer_request.toAccountId == response.toAccountId

        account_to_from_db = Account.get_account_by_id(db_session, transfer_request.toAccountId)
        assert account_to_from_db is not None, "Счет-получатель не найден в БД"
        assert account_to_from_db.balance == transfer_request.amount, "Баланс получателя в БД не верный"

        transaction_from_db = Transaction.get_last_transaction_by_from_account_id(db_session, transfer_request.fromAccountId)
        assert transaction_from_db is not None, "Запись о транзакции не создана в БД"

        assert transaction_from_db.to_account_id == transfer_request.toAccountId, "В транзакции неверный to_account_id"
        assert transaction_from_db.from_account_id == transfer_request.fromAccountId, "В транзакции неверный from_account_id"
        assert transaction_from_db.amount == transfer_request.amount, "В транзакции неверная сумма"


    @pytest.mark.parametrize("amount", [-499.99, 499.99, 0, 10000.01])
    def test_transfer_account_invalid_amount(self, api_manager: ApiManager, create_user_request: CreateUserRequest, transfer_request: TransferRequest, amount: float, db_session: Session):
        balance_from_before = Account.get_account_by_id(db_session, transfer_request.fromAccountId).balance
        balance_to_before = Account.get_account_by_id(db_session, transfer_request.toAccountId).balance

        transfer_request.amount = amount
        api_manager.user_steps.transfer_invalid(create_user_request, transfer_request)

        db_session.expire_all()

        account_from_after = Account.get_account_by_id(db_session, transfer_request.fromAccountId)
        account_to_after = Account.get_account_by_id(db_session, transfer_request.toAccountId)
        assert account_from_after.balance == balance_from_before, f"Ошибка! Списались деньги у отправителя при amount={amount}. Было: {balance_from_before}, Стало: {account_from_after.balance}"
        assert account_to_after.balance == balance_to_before, f"Ошибка! Зачислились деньги получателю при amount={amount}. Было: {balance_to_before}, Стало: {account_to_after.balance}"
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

        assert transfer_request.fromAccountId == response.fromAccountId, f"Ошибка! fromAccountId в ответе API ({response.fromAccountId}) не совпадает с запросом ({transfer_request.fromAccountId})"
        assert transfer_request.toAccountId == response.toAccountId, f"Ошибка! toAccountId в ответе API ({response.toAccountId}) не совпадает с запросом ({transfer_request.toAccountId})"

        account_to_from_db = Account.get_account_by_id(db_session, transfer_request.toAccountId)
        assert account_to_from_db.id == transfer_request.toAccountId, f"Ошибка! Счет-получатель с id={transfer_request.toAccountId} не найден в БД"
        assert account_to_from_db.balance == transfer_request.amount, f"Ошибка! Баланс получателя в БД ({account_to_from_db.balance}) не равен переведенной сумме ({transfer_request.amount})"


        transaction_from_db = Transaction.get_last_transaction_by_from_account_id(db_session, transfer_request.fromAccountId)
        assert transaction_from_db.to_account_id == transfer_request.toAccountId, f"Ошибка! В транзакции БД неверный to_account_id. Ожидалось: {transfer_request.toAccountId}, Фактически: {transaction_from_db.to_account_id}"
        assert transaction_from_db.from_account_id == transfer_request.fromAccountId, f"Ошибка! Транзакция списания для счета {transfer_request.fromAccountId} не найдена в БД"
        assert transaction_from_db.amount == transfer_request.amount, f"Ошибка! Сумма в БД транзакций ({transaction_from_db.amount}) не совпадает с отправленной ({transfer_request.amount})"


    @pytest.mark.parametrize("amount", [-499.99, 499.99, 0, 10000.01])
    def test_transfer_account_invalid_amount(self, api_manager: ApiManager, create_user_request: CreateUserRequest, transfer_request: TransferRequest, amount: float, db_session: Session):
        balance_from_before_from_transaction_db = Account.get_account_by_id(db_session, transfer_request.fromAccountId).balance
        balance_to_before_from_transaction_db = Account.get_account_by_id(db_session, transfer_request.toAccountId).balance

        transfer_request.amount = amount
        api_manager.user_steps.transfer_invalid(create_user_request, transfer_request)

        balance_from_after_from_transaction_db = Account.get_account_by_id(db_session, transfer_request.fromAccountId).balance
        balance_to_after_from_transaction_db = Account.get_account_by_id(db_session, transfer_request.toAccountId).balance
        assert balance_from_after_from_transaction_db == balance_from_before_from_transaction_db, f"Ошибка! Списались деньги у отправителя при невалидном переводе amount={amount}. Ожидалось: {balance_from_before_from_transaction_db}, Стало: {balance_from_after_from_transaction_db}"
        assert balance_to_after_from_transaction_db == balance_to_before_from_transaction_db, f"Ошибка! Баланс получателя ошибочно изменился при невалидном переводе (amount={amount}). Ожидалось: {balance_to_before_from_transaction_db}, Стало: {balance_to_after_from_transaction_db}"
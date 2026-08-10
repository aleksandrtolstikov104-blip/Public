import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_repay_request: CreditRepayRequest, db_session: Session):
        balance_before_from_credit_db = Credit.get_credit_by_id(db_session, credit_repay_request.creditId).balance

        response = api_manager.user_steps.credit_repay(create_credit_user_request, credit_repay_request)

        assert credit_repay_request.creditId == response.creditId, f"Ошибка! ID кредита в ответе API: {response.creditId} не совпадает с отправленным: {credit_repay_request.creditId}"
        assert response.amountDeposited == credit_repay_request.amount, f"Ошибка! Сумма депозита в ответе API: {response.amountDeposited} не совпадает с отправленной: {credit_repay_request.amount}"

        balance_after_from_credit_db = Credit.get_credit_by_id(db_session, response.creditId).balance

        expected_balance = balance_before_from_credit_db + credit_repay_request.amount
        assert balance_after_from_credit_db == expected_balance, (
            f"Ошибка! Баланс кредита в БД после погашения не совпал с ожидаемым. "
            f"Был долг: {balance_before_from_credit_db}, внесли: {credit_repay_request.amount}, "
            f"стало в БД: {balance_after_from_credit_db}, ожидалось: {expected_balance}"
        )

    """
    Ожидаемый результат: Ошибка 422 "Repayment amount exceeds remaining debt".
    """
    @pytest.mark.parametrize("amount", [16000.00])
    def test_credit_repay_invalid(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_repay_request: CreditRepayRequest, amount: float, db_session: Session):
        balance_before_from_credit_db = Credit.get_credit_by_id(db_session, credit_repay_request.creditId).balance

        credit_repay_request.amount = amount
        api_manager.user_steps.credit_repay_invalid(create_credit_user_request, credit_repay_request)

        balance_after_from_credit_db = Credit.get_credit_by_id(db_session, credit_repay_request.creditId).balance

        assert balance_after_from_credit_db == balance_before_from_credit_db, f"Ошибка! Баланс кредита изменился при невалидном платеже amount={amount}. Было: {balance_before_from_credit_db}, стало: {balance_after_from_credit_db}"

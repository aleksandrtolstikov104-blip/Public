import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_repay_request: CreditRepayRequest, db_session: Session):
        credit_before_from_credit_db = Credit.get_credit_by_id(db_session, credit_repay_request.creditId)
        balance_before_from_credit_db = credit_before_from_credit_db.balance


        response = api_manager.user_steps.credit_repay(create_credit_user_request, credit_repay_request)

        assert credit_repay_request.creditId == response.creditId
        assert response.amountDeposited == credit_repay_request.amount

        db_session.expire_all()

        credit_after_from_credit_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_after_from_credit_db is not None, f"Кредит с id={response.creditId} не найден в БД"
        assert credit_after_from_credit_db.id == credit_repay_request.creditId, f"Ошибка! ID кредита в БД: {credit_after_from_credit_db.id} не совпадает с запросом: {credit_repay_request.creditId}"

        expected_balance = balance_before_from_credit_db + credit_repay_request.amount
        assert credit_after_from_credit_db.balance == expected_balance, f"Ошибка! Баланс кредита в БД не совпадает с ожидаемым. Был долг: {balance_before_from_credit_db}, внесли: {credit_repay_request.amount}, стало в БД: {credit_after_from_credit_db.balance} (ожидалось: {expected_balance})"


    """
    Ожидаемый результат: Ошибка 422 "Repayment amount exceeds remaining debt".
    """
    @pytest.mark.parametrize("amount", [16000.00])
    def test_credit_repay_invalid(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_repay_request: CreditRepayRequest, amount: float, db_session: Session):
        balance_before_from_credit_db = Credit.get_credit_by_id(db_session, credit_repay_request.creditId).balance

        credit_repay_request.amount = amount
        api_manager.user_steps.credit_request_invalid(create_credit_user_request, credit_repay_request)

        db_session.expire_all()
        balance_after_from_credit_db = Credit.get_credit_by_id(db_session, credit_repay_request.creditId).balance

        assert balance_after_from_credit_db == balance_before_from_credit_db, f"Ошибка! Баланс кредита изменился при невалидном платеже amount={amount}. Было: {balance_before_from_credit_db}, стало: {balance_after_from_credit_db}"

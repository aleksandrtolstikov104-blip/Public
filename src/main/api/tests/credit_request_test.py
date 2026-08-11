import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit

@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_valid(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_request: CreditRequest, db_session: Session):

        response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)

        assert credit_request.accountId == response.id, f"Ошибка! ID аккаунта в ответе API ({response.id}) не совпадает с запрошенным ({credit_request.accountId})"
        assert credit_request.amount == response.amount, f"Ошибка! Сумма кредита в ответе API ({response.amount}) не совпадает с запрошенной ({credit_request.amount})"
        assert credit_request.termMonths == response.termMonths, f"Ошибка! Срок кредита в ответе API ({response.termMonths}) не совпадает с запрошенным ({credit_request.termMonths})"

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db.account_id == response.id, f"Ошибка! ID аккаунта в БД: {credit_from_db.account_id}, не совпадает с ID в ответе API: {response.id}"
        assert credit_from_db.amount == response.amount, f"Ошибка. Сумма кредита в БД: {credit_request.amount}, отличается от ответа API: {response.amount} "
        assert credit_from_db.term_months == response.termMonths, f"Ошибка! Срок кредита в БД: {credit_from_db.term_months} мес., не совпадает с ответом API: {response.termMonths} мес."

    @pytest.mark.parametrize("amount", [15000.01, 4999.99, 0, -199])
    def test_credit_request_invalid_amount(self, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, credit_request: CreditRequest, amount: float, db_session: Session):
        credit_request.amount = amount
        api_manager.user_steps.credit_request_invalid(create_credit_user_request, credit_request)

        credit_from_db = Credit.get_credit_by_id(db_session, credit_request.accountId)
        assert credit_from_db is None, f"Ошибка! Ожидалось, что кредит не создастся, но в БД появилась запись при невалидной сумме: amount={amount}"

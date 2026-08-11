import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.transfer_request import TransferRequest


@pytest.fixture
def create_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def user_account_response(api_manager: ApiManager, create_user_request):
    account_response = api_manager.user_steps.create_account(create_user_request)
    return account_response

@pytest.fixture
def user_account_second_response(api_manager: ApiManager, create_user_request):
    account_second_response = api_manager.user_steps.create_account(create_user_request)
    return account_second_response

@pytest.fixture
def deposit_account_request(api_manager: ApiManager, user_account_response):
    deposit_request = RandomModelGenerator.generate(DepositAccountRequest)

    deposit_request.accountId = user_account_response.id
    return deposit_request

@pytest.fixture
def deposit_account_response(api_manager: ApiManager, create_user_request, deposit_account_request):
    deposit_response = api_manager.user_steps.deposit_account(create_user_request, deposit_account_request)
    return deposit_response

@pytest.fixture
def transfer_request(api_manager: ApiManager, user_account_response, user_account_second_response):
    transfer = RandomModelGenerator.generate(TransferRequest)

    transfer.fromAccountId = user_account_response.id
    transfer.toAccountId = user_account_second_response.id
    return transfer

"""
CREDIT_USER
"""

@pytest.fixture
def create_credit_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def credit_user_account_response(api_manager: ApiManager, create_credit_user_request):
    account_response = api_manager.user_steps.create_account(create_credit_user_request)
    return account_response

@pytest.fixture
def credit_request(api_manager: ApiManager, credit_user_account_response):
    credit_request = RandomModelGenerator.generate(CreditRequest)
    credit_request.accountId = credit_user_account_response.id
    return credit_request

@pytest.fixture
def credit_response(api_manager: ApiManager, create_credit_user_request, credit_request):
    credit_response = api_manager.user_steps.credit_request(create_credit_user_request, credit_request)
    return credit_response

@pytest.fixture
def credit_repay_request(api_manager: ApiManager, create_credit_user_request, credit_request: CreditRequest, credit_response: CreditResponse) -> CreditRepayRequest:
    credit_repay_request = CreditRepayRequest(
        creditId=credit_response.creditId,
        accountId=credit_request.accountId,
        amount=credit_request.amount
    )
    return credit_repay_request
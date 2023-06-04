import decimal
import re

from data.model.account import Account
from utils.invalid_email import InvalidEmail
from utils.invalid_phone_number import InvalidPhoneNumber
from utils.mail_sender import MailSender
from data.repository.account_repository_impl import AccountRepositoryImpl
from dtos.request.deposit_request import DepositRequest
from dtos.request.login_request import LoginRequest
from dtos.request.register_request import CreateAccountRequest
from dtos.request.transfer_request import TransferRequest
from dtos.request.withdraw_request import WithdrawRequest
from dtos.response.login_response import LoginResponse
from dtos.response.register_response import RegisterResponse
from dtos.response.withdraw_response import WithdrawResponse
from services.account_service import AccountService
from utils.account_not_found_exception import AccountNotFound
from utils.amount_can_not_be_greater_than_balance import AmountCannotBeGreaterThanBalance
from utils.negative_amount_exception import AmountCannotBeNegative
from utils.mapper import Mapper
from utils.phone_number_exist_exception import PhoneNumberExist


class AccountServiceImpl(AccountService):
    account_repository = AccountRepositoryImpl()
    account = Account()

    def register_account(self, request: CreateAccountRequest) -> RegisterResponse:
        self.validate_phone_number(request.get_phone_number())
        self.validate_password(request.get_password())
        self.validate_email_address(request.get_gmail())

        self.send_mail_to_mail_address(request.get_gmail())

        account = Mapper.map_request_with_account(request)
        saved_account = self.account_repository.add(account)
        response = Mapper.map_account_with_response(saved_account)
        return response

    def send_mail_to_mail_address(self, mail_address):
        mail_sender = MailSender()
        mail_sender.email_alert("Account Registration", """
                    Congratulations!
                    You have successfully created
                    an account with instant pay e_wallet
                    """, mail_address)

    def validate_password(self, password: str):
        if len(password) != 4:
            print()
            raise ValueError("Password length must be 4")

    def validate_email_address(self, email_address: str):
        if not (email_address.endswith("@gmail.com") or email_address.endswith("@yahoo.com")
                or email_address.endswith("@email.com")):
            print()
            raise InvalidEmail("Invalid email address")

        # pattern = r'^[a-zA-Z]+[a-zA-Z0-9]*'
        # if not re.match(pattern, email_address):
        #     print()
        #     raise InvalidEmail("Incorrect Email Address")

    def validate_phone_number(self, phone_number: str):
        if len(phone_number) != 11:
            print()
            raise InvalidPhoneNumber("Length 11 is required for phone number")

        pattern = r'^0\d{10}$'
        if not re.match(pattern, phone_number):
            print()
            raise InvalidPhoneNumber("Invalid Phone Number")

        if self.phone_number_exist(phone_number):
            print()
            raise PhoneNumberExist(phone_number + " " + "already exist")

    def phone_number_exist(self, phone_nuber):
        phone_nuber = self.account_repository.find_phone_number(phone_nuber)
        if phone_nuber is not None:
            return True
        return False

    def login(self, login_request: LoginRequest) -> LoginResponse:
        account = self.account_repository.find_by_account_number(login_request.get_account_number())
        if account:
            login_request.set_full_name(account.get_first_name() + " " + account.get_last_name())
        if not account:
            self.new_line()
            raise AccountNotFound("Account not found")
        self.valid_login_password(login_request.get_password())
        login_response = Mapper.map(login_request)
        return login_response

    def new_line(self):
        print()

    def deposit_into(self, deposit_request: DepositRequest) -> str:
        account = self.account_repository.find_by_account_number(deposit_request.get_receivers_account_number())
        if account:
            deposit_request.set_receivers_account_name(account.get_first_name() + " " + account.get_last_name())
        if not account:
            raise AccountNotFound("Account not found.")
        self.validate_negative_amount(deposit_request.get_amount())
        account.deposit(deposit_request.get_amount())
        self.account_repository.add(account)
        self.new_line()
        return self.success_message()

    def success_message(self) -> str:
        return "Sent Successfully"

    def withdraw_from(self, withdraw_request: WithdrawRequest) -> WithdrawResponse:
        account = self.account_repository.find_by_account_number(withdraw_request
                                                                 .get_account_number())
        if not account:
            raise AccountNotFound("Account not found..")
        self.validate_negative_amount(withdraw_request.get_amount())
        self.validate_send_more_than_balance(withdraw_request.get_account_number(),
                                             withdraw_request.get_amount())
        account.withdraw(withdraw_request.get_amount())
        self.account_repository.add(account)
        withdraw_response = WithdrawResponse()
        return withdraw_response

    @staticmethod
    def validate_negative_amount(amount: decimal):
        if amount < 0:
            raise AmountCannotBeNegative("Cannot deposit negative amount")

    def check_balance(self, account_number: str) -> decimal:
        account = self.account_repository.find_by_account_number(account_number)
        if not account:
            raise AccountNotFound("Account not found..")
        return account.get_balance()

    def account_not_found(self, account):
        account_number = self.account_repository.find_by_account_number(account)
        if account_number is not None:
            return True
        return False

    def transfer(self, transfer_request: TransferRequest) -> str:
        print()
        print("hi one")
        receivers_account = self.account_repository.find_by_account_number \
            (transfer_request.get_receiver_account_number())
        print("receivers account from method -> ", receivers_account.get_account_number())

        if not receivers_account:
            print("hi two")
            raise AccountNotFound("Account Not Found")
        print("hi two two")

        if receivers_account:
            print("hi three")
            transfer_request.set_receiver_account_name(receivers_account.get_first_name()
                                                       + " " + receivers_account.get_last_name())

        self.validate_negative_amount(transfer_request.get_amount())
        print("hi four")
        self.validate_send_more_than_balance(transfer_request.get_sender_account_number(),
                                             transfer_request.get_amount())

        withdraw_request = WithdrawRequest()
        withdraw_request.set_account_number(transfer_request.get_sender_account_number())
        withdraw_request.set_amount(transfer_request.get_amount())
        print("hi five")
        self.withdraw_from(withdraw_request)

        deposit_request = DepositRequest()
        deposit_request.set_receivers_account_number(transfer_request.get_receiver_account_number())
        deposit_request.set_amount(transfer_request.get_amount())
        print("hi six")
        self.deposit_into(deposit_request)

        return self.success_message()

    def valid_login_password(self, password):
        the_password = self.account_repository.find_password(password)
        if the_password is None:
            raise AccountNotFound("Account not found")

    def validate_send_more_than_balance(self, account_to_find: str, amount: decimal):
        account = self.account_repository.find_by_account_number(account_to_find)
        customer_account_balance = account.get_balance()
        print("hiiiiiiiiiiiii")

        if customer_account_balance < amount:
            print(account.get_account_number())
            print("Senders account balance -> ", customer_account_balance)
            print(amount)
            raise AmountCannotBeGreaterThanBalance("Amount can not be greater than balance")

import datetime
import random
import string
from dataclasses import dataclass, field
from typing import List, Tuple, Union

from custom_exceptions import AuthenticationFailed, InvalidAccessToken, ClientTokenExpired


@dataclass
class Client:
    user: str
    password: str


@dataclass
class Token:
    auth_token: str
    refresh_token: str
    # TODO: Implement cancel token
    cancel_token: str = None


@dataclass
class Session:
    client: Client
    tokens: Token
    time_to_leave: int = 300
    creation_time: datetime = field(init=False)

    def __post_init__(self):
        self.creation_time = datetime.datetime.now()

    def is_expired(self) -> bool:
        expiration_time = self.creation_time + datetime.timedelta(seconds=self.time_to_leave)
        return expiration_time.timestamp() - self.creation_time.timestamp() < 0

    def is_active(self) -> bool:
        return not self.is_expired()


class AuthServer:
    authorized_sessions: List[Session]

    def __init__(self):
        self.authorized_sessions = []

    def request_token(self, client_data: Client) -> Tuple[str, str]:
        if not self.check_if_correct_user_data(client_data):
            raise AuthenticationFailed("Wrong username or password")
        auth_token = self.generate_random_token(45)
        refresh_token = self.generate_random_token(45)
        client_tokens = Token(auth_token=auth_token, refresh_token=refresh_token)
        session = Session(client_data, client_tokens)
        self.authorized_sessions.append(session)
        # TODO: Implement separate method for refresh token gathering
        return client_tokens.auth_token, client_tokens.refresh_token

    @staticmethod
    def check_if_correct_user_data(client_data) -> bool:
        # TODO: ALLOWED_CLIENT_DATA it's mock for DB records
        ALLOWED_CLIENT_DATA = [Client("admin", "admin2")]
        return client_data in ALLOWED_CLIENT_DATA

    @staticmethod
    def generate_random_token(token_lenght) -> str:
        return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(token_lenght))

    def is_auth_token_valid(self, access_token) -> bool:

        def get_session_data() -> Union[Session, None]:
            for session in self.authorized_sessions:
                if session.tokens.auth_token == access_token:
                    return session
            return None

        client_session = get_session_data()
        #TODO: Qualify it as separated
        # if not client_session:
        #     raise InvalidAccessToken("Access token not found in authorized token list")
        # if client_session.is_expired():
        #     raise ClientTokenExpired("Access token expired. Use refresh token to renew it.")

        return client_session and client_session.is_expired()

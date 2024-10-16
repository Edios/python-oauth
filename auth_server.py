import datetime
import random
import string
from dataclasses import dataclass, field
from typing import List, Tuple, Union

from custom_exceptions import AuthenticationFailed, InvalidToken, AccessTokenExpired


@dataclass
class Client:
    user: str
    password: str


@dataclass
class Token:
    access_token: str
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
        self.creation_time = self.get_timestamp()

    def is_expired(self) -> bool:
        expiration_time = self.creation_time + datetime.timedelta(seconds=self.time_to_leave)
        return expiration_time.timestamp() - self.creation_time.timestamp() < 0

    def is_active(self) -> bool:
        return not self.is_expired()

    @staticmethod
    def get_timestamp():
        return datetime.datetime.now()


class AuthServer:
    authorized_sessions: List[Session]

    def __init__(self):
        self.authorized_sessions = []

    def request_token(self, client_data: Client) -> Tuple[str, str]:
        if not self.check_if_correct_user_data(client_data):
            raise AuthenticationFailed("Wrong username or password")
        auth_token = self.generate_random_token(45)
        refresh_token = self.generate_random_token(45)
        client_tokens = Token(access_token=auth_token, refresh_token=refresh_token)
        session = Session(client_data, client_tokens)
        self.authorized_sessions.append(session)
        # TODO: Implement separate method for refresh token gathering
        return client_tokens.access_token, client_tokens.refresh_token

    @staticmethod
    def check_if_correct_user_data(client_data) -> bool:
        # TODO: ALLOWED_CLIENT_DATA it's mock for DB records
        ALLOWED_CLIENT_DATA = [Client("admin", "admin2")]
        return client_data in ALLOWED_CLIENT_DATA

    def get_session_data_by_token(self, token_type, token_value) -> Union[Session, None]:
        for session in self.authorized_sessions:
            token = session.tokens
            if getattr(token, token_type) == token_value:
                return session
        return None

    @staticmethod
    def generate_random_token(token_lenght) -> str:
        return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(token_lenght))

    def is_access_token_valid(self, access_token) -> bool:

        client_session = self.get_session_data_by_token("access_token", access_token)
        return bool(client_session)

    def is_access_token_expired(self, access_token):
        session = self.get_session_data_by_token("access_token", access_token)
        return session.is_expired()

    def refresh_token(self, refresh_token) -> str:
        """
        Create new access token and refresh timestamp for session based on given refresh token.
        :param refresh_token: Given token in pair with access token.
        :return: New access token
        """
        session = self.get_session_data_by_token("refresh_token", refresh_token)
        if not session:
            raise InvalidToken("Unable to find refresh token in authorized sessions")
        session.tokens.access_token = self.generate_random_token(45)
        session.time_to_leave = session.get_timestamp()
        return session.tokens.access_token

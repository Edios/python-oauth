#
import argparse
from typing import Tuple

from auth_server import Client, AuthServer
from custom_exceptions import InvalidToken, AccessTokenExpired


class DataServer:
    auth_server: AuthServer

    def __init__(self, auth_server):
        self.auth_server = auth_server

    def get_server_data(self, user) -> str:
        server_data = {
            "admin": "Silence is golden",
            "admin2": "Super secret user data",
        }
        return server_data.get(user)

    def get_user_info(self, access_token) -> Tuple[str, str]:
        """
        Returns user-specific information if the user is authorized via a valid access token.
        :param access_token: Access token to verify the user
        :return: User information as a string
        """
        if not self.auth_server.is_access_token_valid(access_token):
            raise InvalidToken("Access token is invalid.")

        if self.auth_server.is_access_token_expired(access_token):
            raise AccessTokenExpired("Access token expired. Please refresh the token.")
        # This should be an external endpoint with trimmed out sensitive data
        session = self.auth_server.get_session_data_by_token('access_token', access_token)
        user_data=self.get_server_data(session.client.user)
        return session.client.user, user_data


def main(user, password):
    client = Client(user, password)
    auth_server = AuthServer()
    data_server = DataServer(auth_server)

    # Fetch tokens /fetch_token
    access_token, refresh_token = auth_server.fetch_token(client)

    # Refresh Token /refresh_token
    # auth_server.refresh_token(refresh_token)

    def validate_and_refresh_token() -> str:
        """
        Check if the access token is valid and refresh if necessary.
        :return: A valid access token
        """
        if not auth_server.is_access_token_valid(access_token):
            raise InvalidToken("Access token is invalid.")

        if auth_server.is_access_token_expired(access_token):
            print("Access token expired. Refreshing token...")
            return auth_server.refresh_token(refresh_token)
        return access_token

    access_token = validate_and_refresh_token()

    # Get user info - Authorization test endpoint
    try:
        user_info = data_server.get_user_info(access_token)
        print(user_info)
    except InvalidToken as e:
        print(f"Authorization failed: {e}")
    except AccessTokenExpired as e:
        print(f"Token expired: {e}")


if __name__ == '__main__':
    # Correct script parameters: --user admin --password admin2
    parser = argparse.ArgumentParser()
    parser.add_argument("--user")
    parser.add_argument("--password")
    args = parser.parse_args()
    main(args.user, args.password)

#
import argparse

from auth_server import Client, AuthServer
from custom_exceptions import InvalidToken, AccessTokenExpired


class DataServer:
    auth_server: AuthServer

    def get_user_info(self, access_token)->:
        pass


def main(user, password):
    client = Client(user, password)
    auth_server = AuthServer()
    data_server = DataServer(auth_server)
    access_token, refresh_token = auth_server.request_token(client)

    if not auth_server.is_access_token_valid(access_token):
        raise InvalidToken("Access token not found in authorized token list")
    if auth_server.is_access_token_expired(access_token):
        raise AccessTokenExpired("Access token expired. Use refresh token to renew it.")

    access_token = auth_server.refresh_token(refresh_token)

    data_server.get_user_info(access_token)


if __name__ == '__main__':
    # Correct script parameters: --user admin --password admin2
    parser = argparse.ArgumentParser()
    parser.add_argument("--user")
    parser.add_argument("--password")
    args = parser.parse_args()
    main(args.user, args.password)

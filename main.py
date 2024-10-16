#
import argparse

from auth_server import Client, AuthServer
from custom_exceptions import InvalidAccessToken, AccessTokenExpired


def main(user, password):
    client = Client(user, password)
    auth_server = AuthServer()
    access_token, refresh_token = auth_server.request_token(client)


    if not auth_server.is_access_token_valid(access_token):
        raise InvalidAccessToken("Access token not found in authorized token list")
    if auth_server.is_access_token_expired(access_token):
        raise AccessTokenExpired("Access token expired. Use refresh token to renew it.")


if __name__ == '__main__':
    # Correct script parameters: --user admin --password admin2
    parser = argparse.ArgumentParser()
    parser.add_argument("--user")
    parser.add_argument("--password")
    args = parser.parse_args()
    main(args.user, args.password)

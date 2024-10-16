#
import argparse

from auth_server import Client, AuthServer

def main(user, password):
    client = Client(user, password)
    auth_server = AuthServer()
    # TODO: Add exchanging client data for code

    # TODO: Use code to get access token
    # TODO: Separated endpoint for fetching refresh token
    access_token, refresh_token = auth_server.request_token(client)

    # Content server should ask for this
    auth_server.is_auth_token_valid(access_token)

    #print()


if __name__ == '__main__':
    # Correct script parameters: --user admin --password admin2
    parser = argparse.ArgumentParser()
    parser.add_argument("--user")
    parser.add_argument("--password")
    args = parser.parse_args()
    main(args.user, args.password)

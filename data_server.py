from custom_exceptions import InvalidToken, AccessTokenExpired


class DataServer:
    def __init__(self, auth_server):
        self.auth_server = auth_server

    def get_server_data(self, user) -> str:
        server_data = {
            "admin": "Silence is golden",
            "adm": "jp2137",
        }
        return server_data.get(user)

    def get_user_info(self, access_token) -> str:
        if not self.auth_server.is_access_token_valid(access_token):
            raise InvalidToken("Access token is invalid.")

        if self.auth_server.is_access_token_expired(access_token):
            raise AccessTokenExpired("Access token expired.")

        session = self.auth_server.get_session_data_by_token('access_token', access_token)
        user_data = self.get_server_data(session.client.user)
        return session.client.user, user_data

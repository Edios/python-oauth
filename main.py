import argparse
from flask import Flask, request, jsonify
from functools import wraps
from auth_server import Client, AuthServer
from custom_exceptions import AuthenticationFailed, InvalidToken, AccessTokenExpired

app = Flask(__name__)

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


# Initialize serving class instances
auth_server = AuthServer()
data_server = DataServer(auth_server)


def basic_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username and auth.password):
            return jsonify({"error": "Invalid credentials"}), 401
        return f(*args, **kwargs)

    return decorated_function


@app.route('/fetch_token', methods=['POST'])
@basic_auth_required
def fetch_token():
    user = request.authorization.username
    password = request.authorization.password
    client = Client(user, password)

    try:
        access_token, refresh_token = auth_server.fetch_token(client)
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 3600,
            "token_type": "bearer"
        }), 201
    except AuthenticationFailed:
        return jsonify(error="Invalid Credentials"), 401


@app.route('/refresh_token', methods=['POST'])
def refresh_access_token():
    refresh_token = request.args.get('refresh_token')
    if not refresh_token:
        return jsonify(error="Missing refresh token."), 400

    try:
        new_access_token = auth_server.refresh_token(refresh_token)
        return jsonify({
            "access_token": new_access_token,
            "expires_in": 3600,
            "token_type": "bearer"
        }), 200
    except InvalidToken:
        return jsonify(error="Invalid Credentials"), 401


@app.route('/login', methods=['POST'])
def user_info():
    access_token = request.args.get('auth_token')
    if not access_token:
        return jsonify(error="Missing access token."), 400

    try:
        user, user_data = data_server.get_user_info(access_token)
        return jsonify({
            "authorized_user": user,
            "content": user_data,
        }), 200
    except InvalidToken:
        return jsonify(error="Invalid Token"), 401
    except AccessTokenExpired:
        return jsonify(error="Expired token"), 401


def main():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    # Initialize argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--user")
    parser.add_argument("--password")
    args = parser.parse_args()

    # Start the Flask app
    main()
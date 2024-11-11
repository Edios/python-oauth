from flask import Flask, request, jsonify
from functools import wraps
from auth_server import Client, AuthServer
from custom_exceptions import AuthenticationFailed, InvalidToken, AccessTokenExpired
from data_server import DataServer

app = Flask(__name__)
# Initialize serving class instances
auth_server = AuthServer()
data_server = DataServer(auth_server)


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


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


@app.route('/login', methods=['GET'])
def login():
    access_token = request.authorization.token
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
        return jsonify(error="Expired token"), 419


if __name__ == '__main__':
    main()

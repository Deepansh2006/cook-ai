from flask import request, jsonify, g
import secrets
from werkzeug.security import check_password_hash
from backend.db import (
    create_user,
    get_user_by_username,
    get_user_by_token,
    update_user_token,
    save_history,
    get_history,
)
from backend.recommender import recommend


def parse_auth_token():
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header.split(' ', 1)[1].strip()
    return request.args.get('token') or (request.get_json(silent=True) or {}).get('token')


def auth_required(fn):
    def wrapper(*args, **kwargs):
        token = parse_auth_token()
        user = get_user_by_token(token)
        if user is None:
            return jsonify({'error': 'Unauthorized, token invalid or missing'}), 401
        g.current_user = user
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper


def register_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json(silent=True) or {}
        username = (data.get('username') or '').strip()
        password = data.get('password') or ''
        if not username or not password:
            return jsonify({'error': 'Username aur password dono chahiye'}), 400
        if get_user_by_username(username):
            return jsonify({'error': 'Username already taken'}), 400
        token = create_user(username, password)
        return jsonify({'message': 'User created', 'token': token}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json(silent=True) or {}
        username = (data.get('username') or '').strip()
        password = data.get('password') or ''
        user = get_user_by_username(username)
        if user is None or not check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Invalid username or password'}), 401
        token = secrets.token_hex(16)
        update_user_token(user['id'], token)
        return jsonify({'message': 'Login successful', 'token': token})

    @app.route('/recommend', methods=['POST'])
    @auth_required
    def recommend_api():
        data = request.get_json(silent=True) or {}
        query = (data.get('query') or '').strip()
        if not query:
            return jsonify({'error': 'Query field required'}), 400
        recommendations = recommend(query)
        save_history(g.current_user['id'], query, len(recommendations))
        return jsonify({
            'query': query,
            'recommendations': recommendations,
        })

    @app.route('/history', methods=['GET'])
    @auth_required
    def history_api():
        limit = request.args.get('limit', 20)
        try:
            limit = int(limit)
        except ValueError:
            limit = 20
        history = get_history(g.current_user['id'], limit)
        return jsonify({'history': history})

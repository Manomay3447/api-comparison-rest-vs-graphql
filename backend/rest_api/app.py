import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from flask import Flask, jsonify
from backend.data import users

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    return jsonify(user or {})

if __name__ == '__main__':
    app.run(port=5001)


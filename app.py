from flask import Flask, request, jsonify
from user_service import UserService

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "User Management System", "status": "running"})

@app.route('/users', methods=['GET'])
def get_all_users():
    users, error = UserService.get_all_users()
    if error:
        return jsonify({"status": "error", "message": error}), 500
    return jsonify({"status": "success", "data": users}), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user, error = UserService.get_user_by_id(user_id)
    if error:
        status_code = 404 if "not found" in error else 500
        return jsonify({"status": "error", "message": error}), status_code
    return jsonify({"status": "success", "data": user}), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400
    
    result, error = UserService.create_user(data)
    if error:
        status_code = 400 if any(word in error for word in ["required", "Invalid", "must be"]) else 500
        return jsonify({"status": "error", "message": error}), status_code
    return jsonify({"status": "success", "message": result["message"]}), 201

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400
    
    result, error = UserService.update_user(user_id, data)
    if error:
        status_code = 404 if "not found" in error else 400 if any(word in error for word in ["required", "Invalid"]) else 500
        return jsonify({"status": "error", "message": error}), status_code
    return jsonify({"status": "success", "message": result["message"]}), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result, error = UserService.delete_user(user_id)
    if error:
        status_code = 404 if "not found" in error else 500
        return jsonify({"status": "error", "message": error}), status_code
    return jsonify({"status": "success", "message": result["message"]}), 200

@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    users, error = UserService.search_users(name)
    if error:
        status_code = 400 if "provide a name" in error else 500
        return jsonify({"status": "error", "message": error}), status_code
    return jsonify({"status": "success", "data": users}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400
    
    result, error = UserService.authenticate_user(data.get('email'), data.get('password'))
    if error:
        status_code = 401 if "Invalid credentials" in error else 400 if "required" in error else 500
        return jsonify({"status": "error", "message": error}), status_code
    return jsonify({"status": "success", "user_id": result["user_id"]}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=False)

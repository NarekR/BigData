from flask import Flask, request, jsonify
import os

app = Flask(__name__)

user_files_directory = "C:/Users/Guest_user/Desktop/User"
if not os.path.exists(user_files_directory):
    os.makedirs(user_files_directory)

users = {}

def load_users():
    for username in os.listdir(user_files_directory):
        password_file_path = os.path.join(user_files_directory, username, "password.txt")
        if os.path.exists(password_file_path):
            with open(password_file_path, 'r') as password_file:
                password = password_file.read()
                users[username] = {'password': password}

load_users()

def save_password(username, password):
    user_directory = os.path.join(user_files_directory, username)
    password_file_path = os.path.join(user_directory, "password.txt")

    if not os.path.exists(user_directory):
        os.makedirs(user_directory)

    with open(password_file_path, 'w') as password_file:
        password_file.write(password)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user_directory = os.path.join(user_files_directory, username)

    if username and password and not os.path.exists(user_directory):
        save_password(username, password)
        users[username] = {'password': password}
        return jsonify({'message': 'Registration successful'})
    else:
        return jsonify({'error': 'Invalid username or password or user already exists'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user_directory = os.path.join(user_files_directory, username)
    password_file_path = os.path.join(user_directory, "password.txt")

    if username in users and os.path.exists(password_file_path):
        with open(password_file_path, 'r') as password_file:
            saved_password = password_file.read()

        if saved_password == password:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'error': 'Invalid password'}), 401
    else:
        return jsonify({'error': 'Invalid username or user does not exist'}), 401

@app.route('/copy_file', methods=['POST'])
def copy_file():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    file_content = data.get('file_content')

    user_directory = os.path.join(user_files_directory, username)

    if username in users and users[username]['password'] == password and os.path.exists(user_directory):
        file_path = os.path.join(user_directory, f"{username}_file.txt")

        with open(file_path, 'w') as file:
            file.write(file_content)

        return jsonify({'message': 'File copied successfully'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/get_file', methods=['GET'])
def get_file():
    username = request.args.get('username')
    password = request.args.get('password')

    user_directory = os.path.join(user_files_directory, username)

    if username in users and users[username]['password'] == password and os.path.exists(user_directory):
        files = [f for f in os.listdir(user_directory) if f.endswith("_file.txt")]
        if files:
            file_path = os.path.join(user_directory, files[0])
            with open(file_path, 'r') as file:
                file_content = file.read()

            os.remove(file_path)
            return jsonify({'file_content': file_content})  # Возвращаем текстовое содержимое файла
        else:
            return jsonify({'message': 'No files available'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(port=5000)

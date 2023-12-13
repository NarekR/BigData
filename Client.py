import requests
import json

def register(username, password):
    url = 'http://localhost:5000/register'
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)
    try:
        print(response.json())
    except json.JSONDecodeError:
        print(response.text)


def login(username, password):
    url = 'http://localhost:5000/login'
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)
    try:
        print(response.json())
    except json.JSONDecodeError:
        print(response.text)

def copy_file(username, password, file_content):
    url = 'http://localhost:5000/copy_file'
    data = {'username': username, 'password': password, 'file_content': file_content}
    response = requests.post(url, json=data)
    try:
        print(response.json())
    except json.JSONDecodeError:
        print(response.text)

def get_file(username, password):
    url = f'http://localhost:5000/get_file?username={username}&password={password}'
    response = requests.get(url)

    try:
        response.raise_for_status()
        print(response.text)
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)

if __name__ == '__main__':
    # Пример использования
    # file_content = input('file content: ')

    while True:
        print("1. Register\n2. Log-in\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            register(username, password)
            file_content = input('file content: ')
            copy_file(username, password, file_content)
            get_file(username, password)
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            login(username, password)
            get_file(username, password)
        elif choice == '3':

            break
        else:
            print("Invalid choice. Please enter a valid option.")

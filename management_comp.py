import json
import logging
from flask import Flask, jsonify, request
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def get_message():
    data = {
        'Name': 'John Mathews',
        'Message': 'No Logo'
    }
    return jsonify(data)


class Keychain:
    text: str
    logo: str

    def __init__(self, text: str, logo: str):
        self.text = text
        self.logo = logo


class User:
    surname: str
    name: str
    email: str
    company: str
    department: str
    phone: str
    role: str
    newsletter: bool

    def __init__(self, surname: str, name: str, email: str, company: str, department: str, phone: str, role: str,
                 newsletter: bool, text: str, logo: str):
        self.surname = surname
        self.name = name
        self.email = email
        self.company = company
        self.department = department
        self.phone = phone
        self.role = role
        self.newsletter = newsletter
        self.obj_keychain = Keychain(text, logo)


users = []


@app.route('/add', methods=['POST'])
def add_value():
    if request.is_json:
        new_data = request.get_json()
        user = User(new_data['surname'], new_data['name'], new_data['email'], new_data['company'],
                    new_data['department'], new_data['phone'], new_data['role'], new_data['newsletter'],
                    new_data['text'], new_data['logo'])
        users.append(user)
        print([user.name for user in users])
        # data.append(users)
        # logging.debug(users)
        return jsonify(new_data), 201
    return {"error": "Request must be JSON"}, 415


@app.route('/delete/<name>', methods=['DELETE'])
def delete_value(name):
    u_1 = User("Britt", "Max", "m.britt@mail.com", "XYZ", "Operations", "+4915192345678", "HR", True, "something", "azure")
    u_2 = User("Hannes", "Patrick", "p.hannes@mail.com", "XYZ", "Operations", "+4915192345779", "HR", False, "something", "terraform")
    users.append(u_1)
    users.append(u_2)
    print(len(users))
    deleted = False
    for user in users:
        if user.name == name:
            users.remove(user)
            print(user.name)
            deleted = True

    if deleted:
        return jsonify('Deleted Successfully', 201)
    else:
        return {"error": "Request must be JSON only"}, 415


if __name__ == '__main__':
    app.run(debug=True)

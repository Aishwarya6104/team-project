import uuid
import datetime
import logging
from azure.core.exceptions import ResourceExistsError, HttpResponseError
from azure.data.tables import TableServiceClient
import os
import yaml
from datetime import datetime, timedelta
import json
from flask import Flask, request
from flask_restful import Api, Resource
from json import JSONEncoder

# https://stkeychainprintwebsite.z6.web.core.windows.net/
app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)


def load_config():
    dir_root = os.path.dirname(os.path.abspath(__file__))
    with open(dir_root + "/config.yaml", "r") as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.FullLoader)


config = load_config()

from uuid import uuid4

# Create a logger for the 'azure' SDK
logger = logging.getLogger('azure')
logger.setLevel(logging.DEBUG)


class Keychain:
    def __init__(self, text, logo):
        self.text = text
        self.logo = logo


class User:
    def __init__(self, surname, name, email, company, department, phone, role, keychain=None):
        self.surname = surname
        self.name = name
        self.email = email
        self.company = company
        self.department = department
        self.phone = phone
        self.role = role
        self.keychain = keychain

    def __repr__(self):
        return "User()"

    def __str__(self):
        return f"member of User {self.surname}, {self.name}, {self.email}, {self.company}, {self.department}, {self.phone}, {self.role}"

    # @property
    # def keychain(self):
    #     return self.keychain
    #
    # @keychain.setter
    # def keychain(self, keychain):
    #     self.keychain = keychain


class UserModel:
    def __init__(self):
        """Initialize the connection to Azure storage account"""
        self.table_service = TableServiceClient.from_connection_string(
            conn_str=config['azure_storage_connection_string'],
            logging_enable=True)
        self.__tablename__ = "users"

    def insert_user_data(self, user_model):
        # try:
        #     self.table_service.create_table_if_not_exists(self.__tablename__)
        # except HttpResponseError:
        #     print("Table already exists")
        print(user_model)
        try:
            user_id = uuid.uuid1().int
            user_name = f"{user_model.surname.capitalize()}{user_model.name.capitalize()}{user_id}"
            user_entity = {
                u'PartitionKey': str(user_name),
                u'RowKey': str(user_id),
                u'surname': str(user_model.surname),
                u'name': str(user_model.name),
                u'email': user_model.email,
                u'company': user_model.company,
                u'department': user_model.department,
                u'phone': user_model.phone,
                u'role': user_model.role,
                u'create_on': str(datetime.datetime.now())
            }
            table_client = self.table_service.get_table_client(table_name=self.__tablename__)
            user_model_entity = table_client.create_entity(entity=user_entity)
        except ResourceExistsError:
            print("Entity already exists")


# subclass JSONEncoder
class UserModelEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class RestFrontBackend(Resource):

    def post(self):
        data = request.get_json()
        new_keychain = Keychain(data['keychain']['text'], data['keychain']['logo'])
        new_user = User(data['surname'], data['name'],
                        data['email'], data['company'],
                        data['department'], data['phone'],
                        data['role'], new_keychain)
        # create an object to insert Data in Table Storage
        user_model = UserModel()
        user_model.insert_user_data(new_user)
        # user_model.insert_user_data(data['surname'], data['name'],
        #                             data['email'], data['company'],
        #                             data['department'], data['phone'],
        #                             data['role'])

        UserModelEncoder().encode(new_user)
        # Encode User Object into JSON formatted Data using custom JSONEncoder
        userJSONData = json.dumps(new_user, indent=0, cls=UserModelEncoder)
        return userJSONData, 201


api.add_resource(RestFrontBackend, '/keychain/api/v1.0/users')

if __name__ == '__main__':
    app.run(debug=True)

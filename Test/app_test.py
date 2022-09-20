import unittest
import requests

API_URL = 'https://restservicebackend-lv.azurewebsites.net/keychain/api/v1.0/users'


class ApiTest(unittest.TestCase):
    # API_URL = 'https://restservicebackend-lv.azurewebsites.net/keychain/api/v1.0/users'
    # DATA_GET_URL = '{}/'.format(API_URL)
    DATA_POST_URL = '{}/'.format(API_URL)
    DATA_OBJ = {
        "surname": "Max",
        "name": "Musterman",
        "email": "mmuster@gmail.com",
        "company": "Thinkport",
        "department": "Development",
        "phone": "+4917659565045",
        "role": "Cloud Engineer",
        "keychain": {
            "text": "Firetornado",
            "logo": "aws"
        }
    }

    '''def test1_get(self):
        r = requests.get(ApiTest.DATA_GET_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)'''

    def test2_post(self):
        r = requests.post(API_URL, json=ApiTest.DATA_OBJ)
        self.assertEqual(r.status_code, 201)

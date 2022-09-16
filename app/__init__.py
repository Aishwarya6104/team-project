import azure.functions as func
import logging
from flask import Flask

app = Flask(__name__)


def main(request: func.HttpRequest):
    logging.info(request.method)

    if request.method == "POST":

        try:
            name = request.get_json()['name']
        except (ValueError, KeyError):
            return func.HttpResponse("Wrong json")

        return func.HttpResponse(f'Hello, {name}')

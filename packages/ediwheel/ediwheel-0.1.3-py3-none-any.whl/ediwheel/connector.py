import base64
import os
from dataclasses import dataclass

from jinja2 import Environment
import requests
import time

MODULE_ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_PATH = os.path.join(MODULE_ABSOLUTE_PATH, 'templates')


@dataclass
class EdiConnectorConfig:
    """
    Class that contains all configuration to connect to the XML API endpoint
    """
    host: str
    username: str
    password: str
    id: str
    timeout_s: int = 10

    def encode_auth(self):
        """
        :return: The base 64 encoded user:password
        """
        capsule = "{}:{}".format(self.username, self.password)
        # encode as BASE64
        return base64.b64encode(bytes(capsule, 'utf-8')).decode('utf-8')


class EdiConnectorTimeoutError(Exception):
    pass


class EdiConnector:
    def __init__(self, config):
        self.config: EdiConnectorConfig = config

    def enquiry(self, ean, manufacturer=""):
        # prepare the headers:
        headers = {
            'Content-type': 'application/xml',
            'Authorization': "Basic " + self.config.encode_auth(),
        }
        # prepare the xml payload, render using jinja2
        # templates/inquiry.xml
        with open(TEMPLATES_PATH + "/inquiry.xml", 'r') as f:
            template = Environment().from_string(f.read())

        print(headers)
        # send the request
        payload = template.render(id=self.config.id, ean=ean, manufacturer=manufacturer)
        try:
            response = requests.post(
                url=self.config.host,
                headers=headers,
                data=payload,
                timeout=self.config.timeout_s,
            )
        except requests.exceptions.Timeout:
            raise EdiConnectorTimeoutError()

        # check the response
        print(response.content.decode('utf-8'))
        print(response.status_code)

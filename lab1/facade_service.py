import json
import uuid

import requests

from base import BaseRequestHandler
from base import run_server

LOGGING_URL = 'http://0.0.0.0:8001'
MESSAGES_URL = 'http://0.0.0.0:8002'


class FacadeRequestHandler(BaseRequestHandler):
    def do_GET(self):
        logging_resp = requests.get(LOGGING_URL)
        messages_resp = requests.get(MESSAGES_URL)

        content = f'{logging_resp.content.decode('utf-8')}|{messages_resp.content.decode('utf-8')}'
        self.write_response(200, 'text/plain', content)

    def do_POST(self):
        body = self.read_body()
        msg_id = str(uuid.uuid4())

        requests.post(
            LOGGING_URL,
            data=json.dumps({msg_id: body}),
            headers={'Content-Type': 'application/json'}
        )

        self.write_response(200, 'text/plain', 'OK')


if __name__ == '__main__':
    run_server(8000, FacadeRequestHandler)
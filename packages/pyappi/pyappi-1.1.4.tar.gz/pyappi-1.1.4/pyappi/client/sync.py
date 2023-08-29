from pyappi.client.client_handle import get_connection_details
from pyappi.util.login import encode_session
from pyappi.client.session import get_session
from pyappi.client.config import set_config
import threading
import time


class RawClientEvents:
    def __init__(self, handler,interval=3, config=None, session={}):
        self.handler = handler
        self.interval = interval

        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

        if config:
            set_config(config)

        self.session = get_session() if not len(session) else encode_session(session)

    def stop(self):
        self.running = False
        self.thread.join()

    def run(self):
        client, config = get_connection_details()

        res = client.get(f'{config["protocol"]}{config["host"]}/sync/root?{self.session}').json()
        
        tsx = res["_cmt"]

        while self.running:
            time.sleep(self.interval)

            res = client.get(f'{config["protocol"]}{config["host"]}/sync/status/{tsx}?{self.session}').json()

            if res:
                self.handler(res)

    

    
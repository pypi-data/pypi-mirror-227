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

        if config:
            set_config(config)

        self.session = get_session() if not len(session) else encode_session(session)

        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def run(self):
        client, config = get_connection_details()

        _res = client.get(f'{config["protocol"]}{config["host"]}/sync/updates/-1?{self.session}')
        res = _res.json()
        
        tsx = res["tsx"]

        while self.running:
            time.sleep(self.interval)

            res = client.get(f'{config["protocol"]}{config["host"]}/sync/updates/{tsx}?{self.session}').json()

            tsx = res["tsx"]

            if res["updates"]:
                self.handler(res["updates"])


class UserTail:
    def __init__(self, config=None, session={}, interval=1):
        self.config = config
        self.session = session
        self.interval = interval

    @staticmethod
    def handler(update):
        print(update)

    def __enter__(self):
        self.client = RawClientEvents(UserTail.handler,self.interval,self.config,self.session)

        return self
    
    def __exit__(self, type, value, traceback):
        self.client.stop()


 
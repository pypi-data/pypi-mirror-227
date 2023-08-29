import unittest
from pyappi.client import use_test_client, RealtimeHttpClient
from pyappi.client.sync import RawClientEvents
import time


class TestSync(unittest.TestCase):
    def setUp(self):
        use_test_client()

        RealtimeHttpClient("test_sync").delete()
 
    def test_events(self):
        update = None
        def handler(_update):
            nonlocal update
            update = _update

        service = RawClientEvents(handler, interval=.3)

        time.sleep(1)

        with RealtimeHttpClient("test_sync") as doc:
            u = doc.update

            u.nested.value = "CAsfawojgaw"
            u.name = "TEST"
            u.here = "HERE"

        while update is None:
            time.sleep(.3)

        self.assertIsNotNone(update.get("test_sync",None))

        service.stop()


if __name__ == "__main__":
    unittest.main()

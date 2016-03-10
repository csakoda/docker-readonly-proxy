import unittest
from test.test_support import EnvironmentVarGuard
import mock
import monitor

@mock.patch('time.sleep')
class MonitorTest(unittest.TestCase):
    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.env.set('STATUS_ENDPOINT', 'http://localhost/status_nginx')
        self.env.set('SLEEP_DURATION', '60')
        self.env.set('MAX_IDLE_COUNT', '5')
        global count
        count = 0

    @mock.patch('requests.get')
    def test(self, mock_requests, mock_time):
        mock_requests.side_effect = get_return
        self.assertTrue(monitor.main())

    @mock.patch('requests.get')
    def test_with_reset(self, mock_requests, mock_time):
        mock_requests.side_effect = get_return_with_reset
        self.assertTrue(monitor.main())


count = 0
def get_return(*args, **kwargs):
    global count
    count += 1
    class MockResponse:
        text = """Active connections: 43
server accepts handled requests
 {0} {0} {0}
Reading: 0 Writing: 5 Waiting: 38""".format(count)
    return MockResponse()

# simulate other activity on the 4th attempt
def get_return_with_reset(*args, **kwargs):
    global count
    if count == 4:
        count += 2
    else:
        count += 1
    class MockResponse:
        text = """Active connections: 43
server accepts handled requests
 {0} {0} {0}
Reading: 0 Writing: 5 Waiting: 38""".format(count)
    return MockResponse()

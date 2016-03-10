import time
import requests
import os
from logbook import Logger, StreamHandler
import sys

StreamHandler(sys.stdout).push_application()
log = Logger('monitor.py')

def main():
    endpoint = os.environ['STATUS_ENDPOINT']
    sleep_duration = int(os.environ['SLEEP_DURATION'])
    max_idle_count = int(os.environ['MAX_IDLE_COUNT'])
    idle_count = 0
    last_status = None
    while True:
        resp = requests.get(endpoint)
        lines = resp.text.split('\n')

        status = lines[2]
        class Status:
            server = 0
            accepts = 0
            handled = 0
            requests = 0
            def __str__(self):
                return "{0} {1} {2} {3}".format(self.server, self.accepts, self.handled, self.requests)
        new_status = Status()
        fields = status.split(' ')
        # account for the possibly empty first field
        if status[0] == ' ':
            fields[0] = '0'

        new_status.server = int(fields[0])
        new_status.accepts = int(fields[1])
        new_status.handled = int(fields[2])
        new_status.requests = int(fields[3])

        log.info('new_status: {0}'.format(new_status))
        if last_status == None:
            last_status = new_status

        log.info('last_status: {0}'.format(last_status))

        if (last_status.accepts + 1 == new_status.accepts
            and last_status.handled + 1 == new_status.handled
            and last_status.requests + 1 == new_status.requests):
            idle_count += 1
        else:
            idle_count = 0

        last_status = new_status
        if idle_count >= max_idle_count:
            log.info('Found {0} consecutive periods of {1} seconds with no activity.  Exiting.'.format(idle_count, sleep_duration))
            return True
        else:
            time.sleep(sleep_duration)
            continue

    return False
if __name__ == "__main__":
    die = main()
    if die:
        sys.exit(1)

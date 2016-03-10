# monitor.py

Intended to die if the nginx status page shows that the only thing hitting nginx is monitor.py

This is useful if you mark the container `essential` in an ECS task definition.

## Configuration

* `STATUS_ENDPOINT` - URL to nginx status page
* `SLEEP_DURATION` - Seconds to sleep between each try
* `MAX_IDLE_COUNT` - Number of consecutive idles seen before exiting

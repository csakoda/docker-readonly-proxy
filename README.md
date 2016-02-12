# docker-readonly-proxy

A WIP reverse proxy using nginx that exposes a few readonly APIs for the docker daemon.

# Usage

```
docker-compose up
```

or

```
docker run -v /var/run/docker.sock:/tmp/docker.sock:ro -p 80:80 csakoda/docker-readonly-proxy
```

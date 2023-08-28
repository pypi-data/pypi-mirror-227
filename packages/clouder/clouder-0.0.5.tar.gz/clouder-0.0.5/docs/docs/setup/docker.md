# Docker

You will need docker images built for you on [DockerHub](https://hub.docker.com/u/datalayer).

## Build

You can also build those docker images if you prefer.

```bash
# Build docker images for local docker.
DATALAYER_DOCKER_REPO=datalayer \
  dla docker-build
```

## Publish

You can also publish new Docker images if you have credentials for.

```bash
# Deploy docker iamges.
DATALAYER_DOCKER_REPO=datalayer \
  dla docker-push
```

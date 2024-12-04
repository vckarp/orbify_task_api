# Orbify FastAPI Technical task

## Requirements

* [Docker](https://www.docker.com/).

## Docker Compose

Deploy the app locally with; 
```console
docker compose up -d --build
```
This command will spawn two containers:
* FastAPI app that listenes on port 8000
* Postgresql database that listenes on port 5432
The default ports can be changed within the [.env](.env) file

## Tests

In order to execute a simple test suite while the stack is already up use command:
```console
docker compose exec orbify_task_api bash run-tests.sh
```
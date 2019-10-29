## Development and testing environments

  - Docker Compose (1.24.1, build 4667896b)
  - Docker  (1.13.1, build 092cba3)
  - Python docker image (python:3.7-alpine)
  - PostgreSQL docker image (postgres:11-alpine)


## How to run the application

Make sure that docker-compose and docker are installed on your system. Clone the repository and then change directory to the cloned repository.

Build and run the web application

```sh
docker-compose build web
docker-compose up -d web
```

Create the database

```sh
docker-compose exec web flask create-db
```

Create admin user with email "admin@mail.com" and password "admin"

```sh
docker-compose exec web flask create-admin
```

## How to create a valid hash of the user's password

You can use this command to create a valid hash

```sh
docker-compose exec web flask generate-password-hash <password>
```

## API base URL

- [http://localhost:5000/api/v1/](http://localhost:5000/api/v1/)

## API authentication

The authentication is based on HTTP Basic authentication

This is an Curl example

```sh
curl -X POST -H 'Content-Type: application/json' -u 'admin@mail.com:admin' -d '{"name": "Project"}' http://localhost:5000/api/v1/project
```

## How to run tests

Build and run the tests

```sh
docker-compose build test
docker-compose up test
```

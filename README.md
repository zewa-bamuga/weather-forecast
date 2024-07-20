# FastAPI weather forecast using React

## Run locally

### Run with Docker Compose

> :warning: **Linux Users**: Running docker-compose may require using sudo command if current user is not in the docker group

> :warning: **Windows Users**: Check that your `git config core.autocrlf` is `false` or set it to `false` before starting, otherwise build/run may fail

```shell script
	make run
```

or

```shell script
	make run-mac
```
or

```shell script
	cp .env.example .env
	cp ./deploy/compose/local/docker-compose.yml docker-compose.yml
	docker-compose up -d
```

After launching, go to http://localhost:3000 to access the React application

### What has been done

- tests were written (27)
- all this is placed in a docker container
- when you visit the site again, you will be prompted to view the weather in the city where the user has already viewed it before
- the search history for each user will be saved, and there will be an API showing how many times which city was entered

### Used technologies

- poetry package manager
- asynchrony
- dependency injection
- migrations using Alembic
- traefik
- s3 was planned to display user avatars, but there was not enough time
- it was planned to make auto-completion (hints) when entering the city, I know how to do it, but I did not have time
- when registering, a message confirming registration is sent to the entered email

### Useful Tips

- use http://localhost to access web UI
- use http://localhost:8000/api/docs to access the FastAPI online documentation
- use http://localhost:3000 to access the React application
- use `make logs` to see logs


### Run tests

```shell script
	make test
```

or

```shell script
	cp ./deploy/compose/test/docker-compose.yml docker-compose.yml
	docker-compose up --build --force-recreate --remove-orphans --abort-on-container-exit
```

or

```shell script
	cp ./deploy/compose/test/docker-compose.yml docker-compose.yml
	docker-compose run --rm fastapi_test pytest
```
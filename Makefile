install:
	poetry install

run:
	cp -f ./deploy/compose/local/docker-compose.yml docker-compose.yml && \
		cp -n .env.example .env && \
		docker-compose up -d --build --remove-orphans

run-mac:
	cp -f ./deploy/compose/local/docker-compose.yml docker-compose.yml && \
	cp -f .env.example .env && \
	docker-compose up -d --build --remove-orphans

stop:
	docker-compose down

test:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . run --rm fastapi_test  pytest -vv --cov=app --cov-branch --cov-report term-missing --cov-fail-under=80

test-key:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . run --rm fastapi_test  pytest -vv --cov=app --cov-branch --cov-report term-missing --cov-fail-under=80 -k $(name)

test-lf:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . run --rm fastapi_test  pytest -vv --cov=app --cov-branch --cov-report term-missing --cov-fail-under=80 --lf

test-rebuild:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . build

test-reset:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . down --volumes

migration:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . \
		run --rm fastapi_test alembic revision --autogenerate && \
		sudo chown -R $(USER):$(USER) ./src/alembic

migration-apply:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . \
		run --rm fastapi_test alembic upgrade head


migration-downgrade:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . \
		run --rm fastapi_test alembic downgrade -1

logs:
	docker-compose logs -f
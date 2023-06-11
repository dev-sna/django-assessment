up:
	docker-compose up

upnew:
	docker-compose rm
	docker-compose up --build

migrations:
	docker-compose run --rm backend python manage.py makemigrations --check

migrate: ## Apply database migrations
	python manage.py migrate --noinput

shell:
	docker exec -it django-assessment_backend_1 bash
build:
	docker-compose build

start:
	docker-compose up

daemon:
	docker-compose up -d

down:
	docker-compose down

show:
	docker-compose exec web python manage.py showmigrations

migrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

freeze:
	docker-compose exec web pip freeze > requirements.txt

shell:
	docker-compose exec web python manage.py shell
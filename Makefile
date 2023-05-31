build:
	docker-compose build

up:
	docker-compose up

pip-compile:
	docker-compose run jupyter \
		pip-compile --no-annotate --resolver=backtracking --output-file requirements.txt requirements.in

shell:
	docker-compose run jupyter bash

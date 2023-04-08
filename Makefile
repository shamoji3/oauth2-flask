build:
	docker-compose build
up:
	docker-compose up --build --remove-orphans
stop:
	docker-compose stop
clean:
	docker-compose kill && docker-compose rm

null:yml
    @:

ENV ?= dev

ifeq ($(ENV),dev)
COMPOSE_FILE = docker/dev/docker-compose.yml
PERSISTENT_PATH = docker/dev/persistent
else ifeq ($(ENV),prod)
COMPOSE_FILE = docker/prod/docker-compose.yml
PERSISTENT_PATH = docker/prod/persistent
else
$(error Invalid value for ENV: $(ENV))
endif

run: create-persistent
	docker compose -f $(COMPOSE_FILE) up -d
build: create-persistent
	docker compose -f $(COMPOSE_FILE) up --build -d
restart: create-persistent
	docker compose -f $(COMPOSE_FILE) down
	docker compose -f $(COMPOSE_FILE) up --build -d
stop:
	docker compose -f $(COMPOSE_FILE) down
create-persistent:
	mkdir -p $(PERSISTENT_PATH)
	mkdir -p $(PERSISTENT_PATH)/grafana/data
	mkdir -p $(PERSISTENT_PATH)/grafana/provisioning/datasources
	mkdir -p $(PERSISTENT_PATH)/grafana/provisioning/plugins
	mkdir -p $(PERSISTENT_PATH)/grafana/provisioning/notifiers
	mkdir -p $(PERSISTENT_PATH)/grafana/provisioning/alerting
	mkdir -p $(PERSISTENT_PATH)/grafana/provisioning/dashboards
	mkdir -p $(PERSISTENT_PATH)/media
am-i-beautiful:
	isort source/
	flake8 source/
beautiful:
	isort source/
	autopep8 --in-place -r source/

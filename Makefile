.PHONY: install lint test build run

install:
	pip install -r requirements.txt -r requirements-dev.txt

lint:
	ruff check .

test:
	pytest -q

build:
	docker build -t deploywatch .

run:
	python -m deploywatch.app

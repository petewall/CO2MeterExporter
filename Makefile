
ALL_PYTHON_SOURCES := $(shell find $$PWD -name '*.py')

lint: $(ALL_PYTHON_SOURCES)
	pipenv run pylint $(ALL_PYTHON_SOURCES)

build-image:
	docker build -t ghcr.io/petewall/co2meter-exporter .

push-image:
	docker push ghcr.io/petewall/co2meter-exporter

run:
	pipenv run uvicorn  main:app --reload

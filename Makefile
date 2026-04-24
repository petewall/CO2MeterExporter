##@ Dependencies
Pipfile.lock: Pipfile ## Lock the lockfile
	pipenv lock

deps: Pipfile.lock
	@PIPENV_VERBOSITY=-1 pipenv install

dev-deps: Pipfile.lock
	@PIPENV_VERBOSITY=-1 pipenv install --dev

##@ Image management
build-image: ## Build the container image
	docker build -t ghcr.io/petewall/co2meter-exporter .

push-image: ## Push the container image
	docker push ghcr.io/petewall/co2meter-exporter

##@ Running

run: deps ## Run locally with hardware attached
	PIPENV_VERBOSITY=-1 BYPASS_DECRYPT=true pipenv run uvicorn --port 9800 main:app --reload

##@ Test

ALL_PYTHON_SOURCES := $(shell find $$PWD -name '*.py')
lint: dev-deps $(ALL_PYTHON_SOURCES) ## Lint the Python sources
	PIPENV_VERBOSITY=-1 pipenv run pylint $(ALL_PYTHON_SOURCES)

test: dev-deps $(ALL_PYTHON_SOURCES) ## Run tests
	PIPENV_VERBOSITY=-1 pipenv run pytest tests/ -v


##@ General

# The help target prints out all targets with their descriptions organized
# beneath their categories. The categories are represented by '##@' and the
# target descriptions by '##'. The awk commands is responsible for reading the
# entire set of makefiles included in this invocation, looking for lines of the
# file as xyz: ## something, and then pretty-format the target and help. Then,
# if there's a line with ##@ something, that gets pretty-printed as a category.
# More info on the usage of ANSI control characters for terminal formatting:
# https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_parameters
# More info on the awk command:
# http://linuxcommand.org/lc3_adv_awk.php

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

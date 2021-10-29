.DEFAULT_GOAL := help

help: ## Print this help message
	@awk 'BEGIN {fs = ":.*?## "} /^[a-zA-Z_-]+:.*?## /' $(MAKEFILE_LIST)  | sort

.check-pipenv: ## Hidden target to make sure we're running in pipenv
    ifndef PIPENV_ACTIVE
        $(error - must run from pipenv shell)
    endif

.PHONY: setup_precommit ## Carry out basic setup tasks
setup_precommit: .setup_precommit

.setup_precommit: .check-pipenv ## Hidden target to install precommit then install the hooks
	pip install pre-commit && \
	pre-commit install

run: ## Start the server
	cd src && \
	python3 server.py

unit_test: ## Run unit tests
	pytest src/test_protocol.py -v

clean: ## Clean up working directories
	rm -rf src/__pycache__
	rm -rf .pytest_cache

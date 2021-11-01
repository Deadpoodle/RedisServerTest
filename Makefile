.DEFAULT_GOAL := help

help: ## Print this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.check-pipenv: ## Hidden target to make sure we're running in pipenv
    ifndef PIPENV_ACTIVE
        $(error - must run from pipenv shell)
    endif

.PHONY: setup_precommit
setup_precommit: .check-pipenv ## Install precommit then install the hooks
	pip install pre-commit && \
	pre-commit install

install: ## Sync pipenv dependencies
	pipenv sync

run: ## Start the server
	python3 src/server.py

unit_test: ## Run unit tests
	pytest src/test_protocol.py -v

clean: ## Clean up working directories
	rm -rf src/__pycache__
	rm -rf .pytest_cache

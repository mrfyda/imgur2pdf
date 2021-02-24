.DEFAULT-GOAL := help

.PHONY: help
help:
	@echo "---------------------------------------------------------------------------------------------------------"
	@echo "Makefile help"
	@echo "---------------------------------------------------------------------------------------------------------"
	@grep -E '^[a-zA-Z_/%\-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "---------------------------------------------------------------------------------------------------------"

install: ## build and install packages locally
	rm -rf dist
	poetry build
	pip install --upgrade --no-deps --force-reinstall dist/imgur2pdf-*.whl

lint: ## lint all files
	flake8 .
	black .

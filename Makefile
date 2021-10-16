default: format lint test

lint:
	flake8
	mypy .

format:
	isort . 
	autopep8 --in-place --recursive . 
	npm_config_yes=true npx prettier --write .

test:
ifdef PYVICARE_CLIENT_ID
	EXEC_INTEGRATION_TEST=1 pytest
else
	pytest
endif

publish:
	sh publish.sh

.PHONY: install package-install test lint run publish

install:
	@poetry install

pip-install:
	@pip install --user --index-url https://test.pypi.org/simple/ \
		--extra-index-url https://pypi.org/simple/ slavarobotam_task_manager

uninstall:
	@pip uninstall slavarobotam_task_manager

lint:
	@poetry run flake8 --ignore=F401, E501\
		--exclude .git,__pycache__,migrations

publish:
	@poetry build
	@poetry publish -r ott45

test:
	@coverage run --source='.' manage.py test -v 2


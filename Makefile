.PHONY: install package-install test lint run publish

install:
	@poetry install

lint:
	@poetry run flake8 \
		--exclude .git,__pycache__,migrations,staticfiles

publish:
	@poetry build
	@poetry publish -r ott45

test:
	@coverage run --source='.' manage.py test -v 2
	@coverage report
	@coverage xml


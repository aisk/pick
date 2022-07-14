.PHONY=publish
publish:
	poetry build
	poetry publish

.PHONY=test
test:
	poetry run mypy .
	poetry run pytest

.PHONY=clean
clean:
	rm -fr build dist pick.egg-info

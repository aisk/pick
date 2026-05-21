.PHONY=publish
publish:
	uv build
	uv publish

.PHONY=test
test:
	uv run mypy .
	uv run pytest

.PHONY=clean
clean:
	rm -fr build dist pick.egg-info

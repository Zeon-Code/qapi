.PHONY: test

setup:
	@pip install ".[tests]"

test:
	@pytest -p no:cacheprovider

release:
	@python setup.py sdist bdist_wheel
	@python -m twine upload dist/*
	@rm -r build/ dist/ qapi.egg-info/

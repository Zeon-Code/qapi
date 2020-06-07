.PHONY: test

setup:
	@pip install .

test:
	@python -B -m unittest discover test

release:
	@python setup.py sdist bdist_wheel
	@python -m twine upload dist/*

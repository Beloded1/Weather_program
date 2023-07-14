style:
	flake8 .

types:
	mypy app

tests:
	python -m pytest

check:
    make -j3 style types tests

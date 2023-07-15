style:
	flake8 .

types:
	mypy weather_program

test:
	python -m pytest

check:
	make -j3 style types test

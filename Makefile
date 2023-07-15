style:
	flake8 .

types:
	mypy weather_program

test:
	python -m pytest -m "not owm"

check:
	make -j3 style types test

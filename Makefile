all: create install

create:

	python3 -m venv venv

destroy:

	rm -rf venv

install:

	venv/bin/pip install -e .

start-dev:

	FLASK_APP=siege/app.py FLASK_DEBUG=1 venv/bin/flask run

govenv:
	source venv/bin/activate

install:
	pip install -r requirements.txt

docker:
	docker build -t bugarin10/midsmix:latest .
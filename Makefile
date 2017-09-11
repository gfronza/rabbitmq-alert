deps-dev:
	sudo pip install -r requirements_dev

test:
	rabbitmqalert/tests/test_rabbitmqalert.py -b
	rabbitmqalert/tests/test_optionsresolver.py -b

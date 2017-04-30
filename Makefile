deps-dev:
	sudo pip install -r requirements_dev

test:
	rabbitmqalert/test_rabbitmqalert.py -b
	rabbitmqalert/test_optionsresolver.py -b
deps-dev:
	sudo pip2 install -r requirements_dev

test: clean
	python2 -m rabbitmqalert.tests.test_apiclient -b; \
	python2 -m rabbitmqalert.tests.test_argumentsparser -b; \
	python2 -m rabbitmqalert.tests.test_conditionchecker -b; \
	python2 -m rabbitmqalert.tests.test_logger -b; \
	python2 -m rabbitmqalert.tests.test_notifier -b; \
	python2 -m rabbitmqalert.tests.test_rabbitmqalert -b; \
	python2 -m rabbitmqalert.tests.models.test_argument -b;

test-install:
	sudo python2 setup.py install

clean:
	rm -rf build/ dist/ rabbitmq_alert.egg-info/ .eggs/
	find . -name *.pyc -delete

dist: clean
	python2 setup.py sdist

dist-inspect:
	tar -tvf dist/*

publish: dist
	twine upload dist/*

lint:
	pylint rabbitmqalert --ignore=tests

test-publish: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

test-metadata: clean
	python2 setup.py check --restructuredtext; \
	python2 setup.py checkdocs

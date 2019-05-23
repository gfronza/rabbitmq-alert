deps-dev:
	sudo pip install -r requirements_dev

test: clean
	python2 -m rabbitmqalert.tests.test_logger -b; \
	python2 -m rabbitmqalert.tests.test_optionsresolver -b; \
	python2 -m rabbitmqalert.tests.test_rabbitmqalert -b;

test-install:
	sudo python2 setup.py install

clean:
	rm -rf build/ dist/ rabbitmq_alert.egg-info/
	find . -name *.pyc -delete

dist: clean
	python2 setup.py sdist

dist-inspect:
	tar -tvf dist/*

publish: dist
	twine upload dist/*

test-publish: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

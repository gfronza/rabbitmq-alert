deps-dev:
	sudo pip install -r requirements_dev

test:
	rabbitmqalert/tests/test_rabbitmqalert.py -b
	rabbitmqalert/tests/test_optionsresolver.py -b

clean:
	rm -rf dist/ rabbitmq_alert.egg-info/

dist: clean
	python2 setup.py sdist

dist-inspect:
	tar -tvf dist/*

publish: dist
	twine upload dist/*

test-publish: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

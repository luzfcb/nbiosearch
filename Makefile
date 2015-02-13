.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-wrapped - remove all .py and .c swig generated artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-pyc clean-wrapped clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-wrapped:
	find . -name '*_wrap.c' -exec rm -f {} +
	find . -name 'NBio*.py' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 nbiosearch tests

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source nbiosearch setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/nbiosearch.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ nbiosearch
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
	pip install dist/nbiosearch-0.1.0-cp27-none-linux_x86_64.whl
	mkdir -p aaa
	cd aaa
	python -c "from nbiosearch import NBioAPI_IndexSearch; print(dir(NBioAPI_IndexSearch))"
	cd ..
	rm -rf aaa

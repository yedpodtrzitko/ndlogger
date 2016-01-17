clean:
	find . -name '*.pyc' -exec rm '{}' \;
	find . -name '*.pyo' -exec rm '{}' \;

dist:
	rm -Rf ./dist
	rm -Rf ./build
	mkdir -p dist build
	python setup.py sdist

deploy_force:
	fab deploy:force

deploy: dist
	fab deploy

bootstrap:
	fab bootstrap

bump:
	python -c "from ndlogger.cli import bump_version; bump_version()"

install:
	pip install -r requirements-dev.txt
	mkdir _devtmp

.PHONY: clean test dist deploy bootstrap_cluster bump static

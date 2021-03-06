# Makefile for django Organice
#

# variables
LANGUAGES = en de it
REQUIREMENTS = docs/requirements.txt
SHELL = /bin/bash

.PHONY: help assets bootstrap bumpver clean develop undevelop docs install uninstall release requirements setuptools tests transifex

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  bumpver       to bump the version number, commit and tag for releasing"
	@echo "  clean         to remove build files and folders"
	@echo "  coverage      to generate and display a test coverage report"
	@echo "  develop       to install all dependencies needed for development/docs/translation"
	@echo "  undevelop     to uninstall all dependencies needed for development/docs/translation"
	@echo "  docs          to generate documentation in English and all translated languages"
	@echo "  install       to install this project including all dependencies (~ pip install)"
	@echo "  uninstall     to uninstall all dependencies / installed packages (pip uninstall -y)"
	@echo "  release       to package a new release, and upload it to pypi.org"
	@echo "  requirements  to generate the requirements.txt file in the docs folder (pip freeze)"
	@echo "  setuptools    to install setuptools or repair a broken pip installation"
	@echo "  tests         to run all tests manually"
	@echo "  transifex     to synchronize translation resources with Transifex (upload+download)"

bumpver:
	@echo "Not implemented yet. Install pypi package instead: \`pip install bumpversion'"

clean:
	$(MAKE) -C docs clean
	find {organice,tests} -type f -name '*.pyc' -delete
	find {organice,tests} -type d -name '__pycache__' -delete
	rm -rf build/ dist/ *.egg-info/ .eggs/ docs/build/ organice/static/.sass-cache .cache .coverage
	rm -rf manage.py test_project_* coverage.xml tests/reports/ *.egg/
	for DIR in media/ static/ templates/ ; do \
		[ -d $$DIR ] && rmdir $$DIR || true ; \
	done

coverage:
	coverage run setup.py test &> /dev/null && \
	coverage report || \
	echo 'Coverage generation failed. (Try `make develop`)'

develop: setuptools
	pip install -q Sphinx sphinx-intl transifex-client flake8 pytest tox coverage behave-django selenium
	HOOK=.git/hooks/pre-commit && grep 'flake8\.main.*git' $$HOOK &> /dev/null || \
	flake8 --install-hook git

undevelop: setuptools
	for PKG in snowballstemmer babel MarkupSafe Jinja2 sphinx-rtd-theme docutils Pygments alabaster Sphinx click sphinx-intl urllib3 transifex-client pep8 pyflakes mccabe flake8 py pytest virtualenv pluggy tox coverage parse enum34 parse-type behave behave-django selenium ; do \
		pip uninstall -q -y $$PKG || true ; \
	done
	HOOK=.git/hooks/pre-commit && grep 'flake8\.main.*git' $$HOOK &> /dev/null && \
	rm $$HOOK || true

docs: develop
	@cd docs && \
	tx pull --all --force && \
	sphinx-intl build
	@for LANG in $(LANGUAGES) ; do \
		$(MAKE) -C docs -e SPHINXOPTS="-D language='"$$LANG"'" html && \
		DIR_LANG=docs/build/html/$$LANG && \
		rm -rf $$DIR_LANG && \
		mkdir $$DIR_LANG && \
		mv docs/build/html/{_sources/,_static/,*.html,*.js} $$DIR_LANG/ ; \
	done
	@echo
	@echo "Build finished. Documentation is in subdirectories ($(LANGUAGES)) of docs/build/html/"

install: setuptools
	python setup.py install

uninstall:
	pip freeze | sed 's/==.*$$//' | xargs -I PKG pip uninstall -y PKG

release: setuptools clean requirements
	cp -v docs/requirements.txt requirements.txt
	python setup.py sdist upload
	git checkout requirements.txt

requirements: setuptools undevelop
# NOTE: we must filter out erroneously listed globally installed packages on Ubuntu
	pip install -q -r requirements.txt
	pip freeze | sed -e '/^django-organice==/d' > $(REQUIREMENTS)
	$(MAKE) develop
	git diff $(REQUIREMENTS)

setuptools:
	python -c 'import setuptools' || \
	curl -s -S https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python
	rm -f setuptools-*.zip

tests:
	py.test

behave: clean
	python setup.py -q develop && \
	organice-setup -v0 test_project_acceptance && \
	python manage.py behave

transifex: develop
	@cd docs && tx pull --all --force
	@$(MAKE) -C docs gettext
	@cd docs && sphinx-intl update -p build/locale && tx push -s
	@echo
	@echo "Translation resources synchronized."

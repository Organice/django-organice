# Makefile for django Organice
#

# variables
LANGUAGES = en de it
REQUIREMENTS = docs/requirements.txt
SHELL = /bin/bash

.PHONY: help clean docs transifex tests

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  bumpver    to bump the version number, commit and tag for releasing"
	@echo "  clean      to remove build files and folders"
	@echo "  depsgen    to generate the requirements.txt file in the docs folder (pip freeze)"
	@echo "  depspurge  to uninstall all dependencies / installed packages (pip uninstall -y)"
	@echo "  docs       to generate documentation in English and all translated languages"
	@echo "  install    to install this project including all dependencies (~ pip install)"
	@echo "  release    to package a new release, and upload it to pypi.org"
	@echo "  tests      to run all tests manually"
	@echo "  transifex  to synchronize translation resources with Transifex (upload+download)"

bumpver:
	@echo "Not implemented yet. Install pypi package instead: \`pip install bumpversion'"

clean:
	$(MAKE) -C docs clean
	rm -rf build/ dist/ django_organice.egg-info/ docs/build/ docs/locale/
	for DIR in media/ static/ templates/ ; do \
		[ -d $$DIR ] && rmdir $$DIR || true ; \
	done

depsgen:
# NOTE: we must filter out erroneously listed globally installed packages on Ubuntu
	pip freeze | sed -e '/^argparse/d' -e '/^wsgiref/d' > $(REQUIREMENTS)
	git diff $(REQUIREMENTS)

depspurge:
	pip freeze | sed 's/==.*$//' | xargs -I PKG pip uninstall -y PKG

docs:
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

install:
	python setup.py install

release:
	$(MAKE) clean
	$(MAKE) install
	$(MAKE) depsgen
	python setup.py sdist upload

tests:
	@echo "Not implemented yet."

transifex:
	@cd docs && tx pull --all --force
	@$(MAKE) -C docs gettext
	@cd docs && sphinx-intl update -p build/locale && tx push -s
	@echo
	@echo "Translation resources synchronized."

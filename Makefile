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
	find . -name '*.pyc' -exec rm {} \;
	rm -rf build/ dist/ django_organice.egg-info/ docs/build/ organice/static/.sass-cache tests/__pycache__/
	for DIR in media/ static/ templates/ ; do \
		[ -d $$DIR ] && rmdir $$DIR || true ; \
	done

develop: setuptools
	pip install Sphinx sphinx-intl transifex-client flake8 pytest
	HOOK=.git/hooks/pre-commit && grep 'flake8\.hooks' $$HOOK &> /dev/null || \
	flake8 --install-hook

undevelop: setuptools
	for PKG in docutils Jinja2 MarkupSafe polib Pygments Sphinx sphinx-intl transifex-client flake8 pyflakes pep8 mccabe pytest py ; do \
		pip uninstall -y $$PKG || true ; \
	done
	HOOK=.git/hooks/pre-commit && grep 'flake8\.hooks' $$HOOK &> /dev/null && \
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
	python setup.py sdist upload

requirements: setuptools undevelop
# NOTE: we must filter out erroneously listed globally installed packages on Ubuntu
	pip freeze | sed -e '/^argparse/d' -e '/^wsgiref/d' > $(REQUIREMENTS)
	$(MAKE) develop
	git diff $(REQUIREMENTS)

setuptools:
	python -c 'import setuptools' || \
	curl -s -S https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python
	rm -f setuptools-*.zip

tests:
	py.test --quiet --strict tests

transifex: develop
	@cd docs && tx pull --all --force
	@$(MAKE) -C docs gettext
	@cd docs && sphinx-intl update -p build/locale && tx push -s
	@echo
	@echo "Translation resources synchronized."

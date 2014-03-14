# Makefile for django Organice
#

# variables
LANGUAGES = en de it
SHELL = /bin/bash

.PHONY: help clean docs transifex tests

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  docs       to generate documentation in English and all translated languages"
	@echo "  tests      to run all tests manually"
	@echo "  transifex  to synchronize translation resources with Transifex (upload+download)"

clean:
	$(MAKE) -C docs clean
	cd docs && rm -rf locale/

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

tests:
	@echo "Not implemented yet."

transifex:
	@cd docs && tx pull --all --force
	@$(MAKE) -C docs gettext
	@cd docs && sphinx-intl update -p build/locale && tx push -s
	@echo
	@echo "Translation resources synchronized."

===============================
Contributing to django Organice
===============================

Official repositories: (kept in sync)

#. `Bitbucket`:index:: https://bitbucket.org/bittner/django-organice
#. `GitHub`:index:: https://github.com/bittner/django-organice

Fork any of the repositories, make your code changes or additions, and place a pull request.

How To Get Started
==================

After cloning your own fork from Bitbucket or GitHub make sure you have created and activated
a virtual environment for development, then run ``make develop`` to install packages that help
you with your development tasks (tools for testing, translation, docs generation).

Guidelines
----------

The primary interpreter target to develop against is **Python 3**.  Ideally, use the highest one the
`Django package`_ integrated into our project is compatible with (3.4, at the moment).  All other
supported Python versions are tested by the `integration server`_ as soon as you place the pull request.
You can run tests locally before pushing using ``tox`` or ``setup.py test``, e.g. ::

    $ tox               # run all tests against all supported Python versions
    $ tox -e py34,py27  # run all tests against Python 3.4 and 2.7 only
    $ ./setup.py -q test -a tests/management  # only run management tests against default python

Source code is supposed to satisfy ``flake8`` default rules (with the exception of line length,
which can be up to 120 characters long).  A pre-commit hook for Git is installed automatically
for your convenience when you run ``make develop``, so you shouldn't even be able to commit when
``flake8`` is not passing.  Additional static analysis is conducted by the `QA server`_, and you
should make sure that code health goes up (or stays the same) with each contribution.


.. _Django package: https://pypi.python.org/pypi/Django/1.8#downloads
.. _integration server: https://travis-ci.org/Organice/django-organice
.. _QA server: https://landscape.io/github/Organice/django-organice/master

Help Wanted
===========

- Writing tests (unit tests, BDD tests)
- New features on the roadmap (see README)
- Translations (blog posts, documentation, user interface)

Translation
-----------

Translation is done on `Transifex`_ for both the project text strings and the documentation.

The multilingual documentation is written in `reStructuredText`_ syntax, and built using `Sphinx`_.
As a `translator`:index: you can simply jump on `Transifex`:index: and get your hands dirty for
your language.  Some helpful background reading is available from `Read the Docs`_ and
`Transifex support`_.


.. _Transifex: https://www.transifex.com/projects/p/django-organice-docs/
.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _Sphinx: http://sphinx-doc.org/intl.html
.. _Read the Docs: http://read-the-docs.readthedocs.org/en/latest/i18n.html
.. _Transifex support: http://support.transifex.com/customer/portal/articles/972120-introduction-to-the-web-editor

Bumping Versions, Package, Release
==================================

As for the `version numbers`:index: of django Organice we use `Semantic Versioning`_.  Changes
from one to the next `release`:index: are documented in the :doc:`changelog`.


.. _Semantic Versioning: http://semver.org/

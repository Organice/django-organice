============
Installation
============

This document assumes you are familiar with basic Python and Django development and their tools_.
If not, please read up on pip_, virtualenv_, and virtualenvwrapper_ first. A basic understanding is sufficient.

.. _tools: http://www.clemesha.org/blog/modern-python-hacker-tools-virtualenv-fabric-pip/
.. _pip: http://www.pip-installer.org/en/latest/
.. _virtualenv: http://docs.python-guide.org/en/latest/dev/env/#interpreter-tools
.. _virtualenvwrapper: http://www.doughellmann.com/docs/virtualenvwrapper/

Requirements
============

- Python 2.5 or higher

All other depencencies are resolved by the django Organice installer.

Recommended for installation
----------------------------

- pip
- virtualenv

Installing django Organice
==========================

1. We recommend preparing a virtual environment for running django Organice::

    $ mkvirtualenv myproject
    $ workon myproject

  The prompt will change to something like ``(myproject)~$`` to reflect that your new virtual environment is active.

2. The easiest way is using ``pip`` for installation::

    $ pip install django-organice

  This will pull the latest django Organice package from the Internet and install all dependencies automatically.

3. Install the adapter suitable for your database (PostgreSQL ``psycopg2``, MySQL ``MySQL-python``,
   Oracle ``cx_Oracle``, `etc.`_), e.g. ::

    $ pip install psycopg2

  The Django project recommends PostgreSQL.

  *NOTE:* You can skip this step if you decide to use SQLite, e.g. for evaluation purposes.

.. _`etc.`: https://docs.djangoproject.com/en/dev/topics/install/#database-installation



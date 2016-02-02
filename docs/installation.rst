============
Installation
============

This document assumes you are familiar with basic Python and Django development and their `tools`_.
If not, please read up on `pip`_, `virtualenv`_, and `virtualenvwrapper`_ first.  A basic
understanding is sufficient.

.. _`tools`: http://www.clemesha.org/blog/modern-python-hacker-tools-virtualenv-fabric-pip/
.. _`pip`: http://www.pip-installer.org/en/latest/
.. _`virtualenv`: http://docs.python-guide.org/en/latest/dev/env/#interpreter-tools
.. _`virtualenvwrapper`: http://www.doughellmann.com/docs/virtualenvwrapper/

`Requirements`:index:
=====================

- Python 2.7, 3.3, or 3.4

All other `dependencies`:index: are resolved by the django Organice installer.  Most of those
dependencies are intentionally not pinned on their version number to allow a liberal upgrade
path.  This means you will get more up-to-date packages installed, but they may break your setup
or not install at all.

Confirmed, working dependencies are documented in the :doc:`changelog` for each release.  If
anything goes wrong during the installation described below try installing those requirements
in your virtual environment *before* you install ``django-organice``::

    $ pip install -r docs/requirements.txt

Recommended for installation
----------------------------

- pip
- virtualenv
- virtualenvwrapper

Installing django Organice
==========================

1. We recommend preparing a `virtual environment`:index: for running django Organice::

    $ mkvirtualenv example
    $ workon example

   The prompt will change to something like ``(example)~$`` to reflect that your new virtual
   environment is active.

2. The easiest way is using ``pip`` for installation::

    $ pip install django-organice

   This will pull the latest django Organice package from the Internet and `install`:index: all
   dependencies automatically.

   If you're a developer you may want to run django Organice with the latest sources: (don't do this
   as a user) ::

    $ git clone https://github.com/Organice/django-organice.git
    $ cd django-organice
    $ python setup.py install

   or, alternatively, using pip::

    $ pip install git+https://github.com/Organice/django-organice.git#egg=django-organice

3. Install the adapter suitable for your `database`:index: (PostgreSQL ``psycopg2``, MySQL
   ``MySQL-python``, Oracle ``cx_Oracle``, `etc.`_), e.g. ::

    $ pip install psycopg2

   The Django project recommends PostgreSQL.

.. NOTE::

    You can skip this step if you decide to use SQLite, e.g. for evaluation purposes.

4. Run the Organice setup command to create your new project: (e.g. *example*) ::

    $ organice-setup example

5. Edit your settings in ``example/settings/common.py``, ``example/settings/develop.py``, etc.  See
   the `Django documentation`_ on settings if you're not familiar with it.  The ``develop`` settings
   are used by your project by default (local development), ``common`` is included in all profiles.

6. Initialize your database::

    $ python manage.py organice bootstrap

   This will prepare the database and add some sample content.   If you'd rather wish to start with
   a clean database run to ``migrate`` only instead::

    $ python manage.py migrate

7. Start your Django project::

    $ python manage.py runserver

   You can now point your browser to http://127.0.0.1:8000/ and start developing your project
   locally.

.. NOTE::

    If you're planning to create your content locally make sure you use the same database engine
    for local development and production.  Your plan of moving the whole database content from
    development to production will give you major headaches otherwise.  And, use Sqlite for
    evaluating only!

.. _`etc.`: https://docs.djangoproject.com/en/1.8/topics/install/#database-installation
.. _`Django documentation`: https://docs.djangoproject.com/en/1.8/topics/settings/

Initial Configuration
=====================

#. Follow the instructions given to you by the django Organice installer ``organice-setup`` after
   setup has completed.  You have to adapt some values in your project settings!

#. If you want your site to use a language other than English, or you want to use several languages:
   Adapt the values of :const:`LANGUAGE_CODE` and :const:`LANGUAGES`, and set
   :const:`USE_I18N = True` in your project settings.

#. After installation django Organice is configured, but unless you ran the ``bootstrap`` management
   command the database is blank without any content.  You can add some sample content and other data
   running one or all of the following commands::

    $ python manage.py organice initauth  # prepare social auth provider configuration
    $ python manage.py organice initcms   # add pages for your website
    $ python manage.py organice initblog  # add blog categories and posts

#. Alternatively, add your first pages, blog posts, and newsletter data manually:

   - Add some pages and navigation in the Django administration at Cms > Pages, and publish your
     changes.
   - Surf your new website, and fill your new pages with content using the front-end editing
     feature.
   - Surf to ``/blog/`` on your website, and start adding Blog posts.
   - Add a user in the Django administration at Newsletter > Contacts.
   - Add ``localhost`` (or appropriate server) to Newsletter > SMTP servers.
   - To allow subscribing from the website (from ``/newsletter/subscribe``) add a list to
     Newsletter > Mailing lists.
   - Finally, add your first newsletter to Newsletter > Newsletters.
   - For adding templates to Emencia Newsletter please consult the related section in the
     `TinyMCE 3.x documentation`_.
   - To add a link page simply use the "bookmarks" template for a page.  You have to add categories
     and links in the Django Admin.  (NOTE: This feature may be replaced by an integration of social
     bookmarking services in future.)

#. For sending newsletters to work you must configure a cronjob polling on
   ``python manage.py send_newsletter`` every half an hour.  If that was just Greek to you go ask
   your server admin for help.  She knows!

.. _`TinyMCE 3.x documentation`: http://www.tinymce.com/wiki.php/Configuration3x:external_template_list_url

Deployment to Production
========================

During the installation ``organice-setup`` prepared 3 different environments that help you with
deployment::

    example
    ├── settings
    │   ├── __init__.py
    │   ├── common.py
    │   ├── develop.py
    │   ├── staging.py
    │   └── production.py

This modularized setup is described in Solution 2 of Tommy Jarnac's blog on `Django settings best
practices`_ [1]_.  The ``develop`` settings are active by default (for local development),
``common`` is included by all profiles.

For deployment to environments other than ``develop`` the settings module location must be
overridden by setting the Django environment variable :const:`DJANGO_SETTINGS_MODULE`.  For example,
if you use Apache as your Django web server adapt your Apache configuration file for ``example``
with::

    SetEnv DJANGO_SETTINGS_MODULE example.settings.production

.. NOTE::

  To test different settings locally you can start the Django webserver with the ``--settings``
  option::

    $ python manage.py runserver --settings=example.settings.staging

Finally, make sure you also have consulted the `deployment checklist`_ of the Django project
and follow their best practices.


.. _`Django settings best practices`: http://www.sparklewise.com/django-settings-for-production-and-development-best-practices/
.. [1] David Cramer from DISQUS has described a similar solution at http://justcramer.com/2011/01/13/settings-in-django/
.. _deployment checklist: https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

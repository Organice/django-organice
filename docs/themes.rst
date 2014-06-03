======
Themes
======

One of the nice things of django Organice is that themes are handled as separate projects.  In fact,
they are pluggable Django apps composed of assets and templates that you can simply install and activate.

Official Themes
===============

Here is a list of django Organice themes officially supported by us:

#. RSSK Theme: `django-organice-theme-rssk`_
#. Fullpage Theme: `django-organice-theme-fullpage`_

If you have a nice theme and would like to include it in this list `let us know by e-mail`_
or make a pull request on this page of the documentation.

Mother Theme
------------

``django-organice-theme`` is the mother of all themes for django Organice.  This theme is installed automatically
when you install django Organice.  From the development perspective all themes are derived from the mother theme,
which contains a collection of static files (assets) and templates, as well as a ``Makefile`` for asset management.
The mother theme is composed of:

- `bootstrap-sass`_ (Sass version of Twitter Bootstrap v3)
- `Compass`_ (CSS authoring framework using Sass)
- `UglifyJS v2`_ (JavaScript minifier)

The ``Makefile`` also supports you with updating those components on your development system.

Rolling Your Own Theme
======================

Preparations:

- Visit http://organice.io/themes and find a theme that is as close as it gets of what you want.
- Go to that theme's repository page, make a copy of the whole project, and rename it (e.g. to ``mytheme``).

Loop until you're happy:

- Add or adapt the style sheet (``.scss``), JavaScript (``.js``), and other files in ``mytheme/static/``.
- Run ``make assets`` in order to compile the Sass files to CSS, and combine and minify both CSS und JavaScript.
- Adapt the template files in ``mytheme/templates/``, and test the results on your development system.


.. _`django-organice-theme-rssk`: https://pypi.python.org/pypi/django-organice-theme-rssk
.. _`django-organice-theme-fullpage`: https://pypi.python.org/pypi/django-organice-theme-fullpage
.. _`let us know by e-mail`: support@organice.io
.. _`bootstrap-sass`: https://github.com/twbs/bootstrap-sass
.. _`Compass`: http://compass-style.org/
.. _`UglifyJS v2`: https://github.com/mishoo/UglifyJS2

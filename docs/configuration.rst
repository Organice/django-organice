=============
Configuration
=============

django Organice comes with sensible defaults for almost anything.  Yet still, you can customize its
behavior with the help of the settings listed in this section.

.. _settings:

Settings
========

You may define any of the following options in your project's ``settings`` to override the default
value.

:const:`ORGANICE_URL_PATH_ADMIN`
--------------------------------
:Default: ``'admin'``

The URL path for accessing the Django Administration backend (e.g. ``www.example.com/admin``).  Must
be non-empty.  Use an identifier only, no white space, no leading or trailing slash.

:const:`ORGANICE_URL_PATH_BLOG`
-------------------------------
:Default: ``'blog'``

The URL path for the blog's start page (e.g. ``www.example.com/blog``).  Must be non-empty.  Use an
identifier only, no white space, no leading or trailing slash.

:const:`ORGANICE_URL_PATH_NEWSLETTER`
-------------------------------------
:Default: ``'newsletter'``

The URL path for accessing newsletter functionality on the front-end (e.g.
``www.example.com/newsletter``).  Must be non-empty.  Use an identifier only, no white space, no
leading or trailing slash.

:const:`ORGANICE_URL_PATH_TODO`
-------------------------------
:Default: ``'todo'``

The URL path for accessing todo list functionality on the front-end (e.g. ``www.example.com/todo``).
Must be non-empty.  Use an identifier only, no white space, no leading or trailing slash.

Third Party Settings
====================

:const:`ACCOUNT_ADAPTER`
------------------------
:Default: (see `django-allauth configuration`_)

The authentication adapter used by Organice.  The ``organice-setup`` command sets its value to
``'organice.auth.adapters.AccountAdapter'``, which ensures that the CMS editorial workflow
is activated for every new user.  This is originally a setting from ``django-allauth`` (see the
`Advanced Usage`_ chapter of the allauth docs).  Must be a valid dotted module path.
*Remove this setting to deactivate the editorial workflow for guest users with email signup.*

:const:`SOCIALACCOUNT_ADAPTER`
-------------------------------
:Default: (see `django-allauth configuration`_)

The authentication adapter used by Organice.  The ``organice-setup`` command sets its value to
``'organice.auth.adapters.SocialAccountAdapter'``, which ensures that the CMS editorial workflow
is activated for every new user.  This is originally a setting from ``django-allauth`` (see the
`Advanced Usage`_ chapter of the allauth docs).  Must be a valid dotted module path.
*Remove this setting to deactivate the editorial workflow for guest users with social signup.*

Analytics Providers
-------------------

The `analytics`:index: services supported by ``django-analytical`` are enabled by setting various
service properties in your settings file.  The properties are documented in `their documentation`_.
For security reasons you shouldn't add those to your common settings file, but to
``settings.production``.

Maps (Plugin for django CMS)
----------------------------

All map providers require that you configure an API key.  See the `djangocms-maps configuration`_
for details.

.. _django-allauth configuration:
    http://django-allauth.readthedocs.io/en/latest/configuration.html?highlight=ACCOUNT_ADAPTER
.. _Advanced Usage:
    http://django-allauth.readthedocs.io/en/latest/advanced.html#creating-and-populating-user-instances
.. _`their documentation`: https://pythonhosted.org/django-analytical/install.html#enabling-the-services
.. _djangocms-maps configuration: https://github.com/Organice/djangocms-maps#configuration

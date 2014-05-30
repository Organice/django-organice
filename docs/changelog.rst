=========
CHANGELOG
=========

0.2
===

- Project-level Makefile
- Automation of translation processes with Transifex (for documentation only)
- New options for settings (see :ref:`settings`)
- Newsletter editor configuration, newsletter template sample
- User profiles and social login (django-allauth)
- Added assets pipeline (bootstrap-sass, Compass, UglifyJS v2)
- Upgraded jQuery to v1.11.0, template overhaul with Bootstrap
- Added language selection dropdown menu
- Migrated theme data (templates, styles, and javascript) and assets pipeline
  to separate projects
- Generation of server configuration (lighttpd) and more options in organice-setup
- Rudimentary media management for django CMS (django-filer)

:Changes: https://github.com/bittner/django-organice/compare/v0.1...HEAD
:Packages: https://github.com/bittner/django-organice/blob/v0.2/docs/requirements.txt

0.1
===

- Initial release
- Based on Django 1.5.5, django CMS 2.4.3, Zinnia blog 0.13, Emencia newsletter 0.3.dev
- A more natural i18n mechanism than vanilla Django, no language prefix for default language
- Setup script with project generation, deployment settings, custom templates, Bootstrap 3

:Packages: https://github.com/bittner/django-organice/blob/v0.1/docs/requirements.txt

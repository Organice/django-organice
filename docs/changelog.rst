=========
CHANGELOG
=========

:Changes: https://github.com/bittner/django-organice/compare/v0.2...HEAD

0.2
===

- Project-level Makefile
- Automation of translation processes with Transifex (for documentation only)
- New options for settings (``ORGANICE_URL_PATH_``...)
- Newsletter editor configuration, newsletter template sample
- Added social login and user profiles (django-allauth)
- Added assets pipeline (bootstrap-sass, Compass, UglifyJS v2)
- Upgraded jQuery to v1.11.0, template overhaul with Bootstrap
- Added language selection dropdown menu
- Migrated theme data (templates, styles, and javascript) and assets pipeline
  to separate projects
- Generation of server configuration (lighttpd) and more options in organice-setup
- Added media management (django-media-tree)
- Added todo lists (django-todo)
- Added generic analytics (django-analytical)

:Changes: https://github.com/bittner/django-organice/compare/v0.1...v0.2
:Packages: https://github.com/bittner/django-organice/blob/v0.2/docs/requirements.txt

0.1
===

- Initial release
- Based on Django 1.5.5, django CMS 2.4.3, Zinnia blog 0.13, Emencia newsletter 0.3.dev
- A more natural i18n mechanism than vanilla Django, no language prefix for default language
- Setup script with project generation, deployment settings, custom templates, Bootstrap 3

:Packages: https://github.com/bittner/django-organice/blob/v0.1/docs/requirements.txt

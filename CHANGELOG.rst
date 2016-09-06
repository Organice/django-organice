0.4
===

- Use djangocms-maps (instead of djangocms-googlemap)
- Add a simple type of editorial workflow (via user groups and CMS permissions)
- Upgrade Zinnia templates (django-organice-theme)
- Upgrade and add more social auth providers (django-allauth)
- Upgrade to Django 1.8.14, django CMS 3.3.2, Zinnia 0.16
- Add ability to generate Nginx deployment configuration

:Changes: https://github.com/Organice/django-organice/compare/v0.3...v0.4
:Dependencies: https://github.com/Organice/django-organice/blob/v0.4/docs/requirements.txt

0.3
===

- Disable Contact Page plugin (to be replaced by forms builder) -- *planned for v0.5*
- Disable Mediatree component (needs upgrade to Python 3) -- *planned for v0.5*
- Disable Newsletter component (needs upgrade to Python 3) -- *planned for v0.5*
- Add Python 3 support
- Switch from develop/master model to feature branching model (default branch: ``master``)
- Migrate project to Django 1.8.8 and django CMS 3.2
- Add sample content loading (first using fixtures, later converted to management command)
- Integration of Piwik open source analytics (optional via django-analytical)
- Add some test coverage, finally!
- Start with continuous builds (Travis-CI, Shippable)

:Changes: https://github.com/Organice/django-organice/compare/v0.2...v0.3
:Dependencies: https://github.com/Organice/django-organice/blob/v0.3/docs/requirements.txt

0.2
===

- Project-level Makefile
- Automation of translation processes with Transifex (for documentation only)
- New options for settings (``ORGANICE_URL_PATH_``...)
- Newsletter editor configuration, newsletter template sample
- Add social login and user profiles (django-allauth)
- Add assets pipeline (bootstrap-sass, Compass, UglifyJS v2)
- Upgrade jQuery to v1.11.0, template overhaul with Bootstrap
- Add language selection dropdown menu
- Migrate theme data (templates, styles, and javascript) and assets pipeline
  to separate projects
- Generation of server configuration (lighttpd) and more options in organice-setup
- Add media management (django-media-tree)
- Add todo lists (django-todo)
- Add generic analytics (django-analytical)

:Changes: https://github.com/Organice/django-organice/compare/v0.1...v0.2
:Dependencies: https://github.com/Organice/django-organice/blob/v0.2/docs/requirements.txt

0.1
===

- Initial release
- Based on Django 1.5.5, django CMS 2.4.3, Zinnia blog 0.13, Emencia newsletter 0.3.dev
- A more natural i18n mechanism than vanilla Django, no language prefix for default language
- Setup script with project generation, deployment settings, custom templates, Bootstrap 3

:Dependencies: https://github.com/Organice/django-organice/blob/v0.1/docs/requirements.txt

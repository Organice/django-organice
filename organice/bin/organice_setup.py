#!/usr/bin/env python
#
# Copyright 2014 Peter Bittner <django@bittner.it>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Setup script for starting a django Organice project.
"""
from organice.management.settings import DjangoModuleManager, DjangoSettingsManager
from stat import S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IXGRP, S_IROTH, S_IXOTH
from subprocess import call
import django.conf
import django.template
import errno
import os
import sys


# global variables (a class with members would be too verbose) *nirg*
args = None
profiles = None
projectname = None
settings = None


def safe_delete(filename):
    """
    Make a best-effort delete without raising an exception when file didn't
    exist (no race condition). All other errors raise their usual exception.
    """
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:  # no such file
            raise  # re-raise exception for any other error


def safe_rename(source, target):
    """
    Perform a forced rename of a file, overwriting an existing target.
    If the source file doesn't exist the target is simply deleted.
    """
    safe_delete(target)
    try:
        os.rename(source, target)
    except OSError as e:
        if e.errno != errno.ENOENT:  # no such file
            raise  # re-raise exception for any other error


def adding_settings_for(section):
    """Simple helper for progress printouts"""
    return 'Adding settings for %s ...' % section


def _print_verbose(vlevel, message):
    """Print text to stdout in accordance with user-specified verbosity level."""
    global args

    if args.verbosity >= vlevel:
        print message


def _evaluate_command_line():
    global projectname
    global args

    usage_descr = 'django Organice setup. Start getting organiced! ' \
                  'Your collaboration platform starts here.'
    help_account = 'Organice account name used as subdomain (default: projectname)'
    help_domain = 'optional domain name to enforce'
    help_engine = 'database engine (for profiles: staging, production)'
    help_database = 'database name (for profiles: staging, production)'
    help_username = 'database user (for profiles: staging, production)'
    help_password = 'database password (for profiles: staging, production)'
    help_manage = 'use default single manage.py or use multi-settings variant (default: %(default)s)'
    help_webserver = 'create appropriate web server configuration (default: %(default)s)'
    help_set = 'set the value of a settings variable in a destination file (this option can be used several times)'
    help_verbosity = 'Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output'

    if sys.version_info < (2, 7):
        from optparse import OptionParser  # Deprecated since version 2.7

        parser = OptionParser(description=usage_descr)
        parser.add_option('--account', help=help_account)
        parser.add_option('--domain', help=help_domain)
        parser.add_option('--engine', choices=['postgresql_psycopg2', 'mysql', 'oracle'], help=help_engine)
        parser.add_option('--database', help=help_database)
        parser.add_option('--username', help=help_username)
        parser.add_option('--password', help=help_password)
        parser.add_option('--manage', choices=['single', 'multi'], default='single', help=help_manage)
        parser.add_option('--webserver', choices=['apache', 'lighttp'], default='apache', help=help_webserver)
        parser.add_option('--set', help=help_set, nargs=3, metavar=('dest', 'var', 'value'), action='append')
        parser.add_option('--verbosity', '-v', type=int, choices=range(4), default=3, help=help_verbosity)
        (options, args) = parser.parse_args()
        if len(args) != 1:
            parser.error('Please specify a projectname')
        projectname = args[0]
        args = options
    else:
        from argparse import ArgumentParser  # New since version 2.7

        parser = ArgumentParser(description=usage_descr)
        parser.add_argument('projectname', help='name of project to create')
        parser.add_argument('--account', help=help_account)
        parser.add_argument('--domain', help=help_domain)
        parser.add_argument('--engine', choices=['postgresql_psycopg2', 'mysql', 'oracle'], help=help_engine)
        parser.add_argument('--database', help=help_database)
        parser.add_argument('--username', help=help_username)
        parser.add_argument('--password', help=help_password)
        parser.add_argument('--manage', choices=['single', 'multi'], default='single', help=help_manage)
        parser.add_argument('--webserver', choices=['apache', 'lighttp'], default='apache', help=help_webserver)
        parser.add_argument('--set', help=help_set, nargs=3, metavar=('dest', 'var', 'value'), action='append')
        parser.add_argument('--verbosity', '-v', type=int, choices=range(4), default=3, help=help_verbosity)
        args = parser.parse_args()
        projectname = args.projectname


def _create_project():
    global args
    global projectname

    manage_script_name = 'manage.py'
    manage_delete_name = 'manage.py~deleted'
    mode0755 = S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH

    if args.manage == 'multi':
        if os.path.isfile(manage_script_name):
            _print_verbose(2, 'Deleting manage.py to allow multi-settings platform setup ...')
            safe_rename(manage_script_name, manage_delete_name)

    _print_verbose(2, 'Generating project %s ...' % projectname)
    code = call(['django-admin.py', 'startproject', projectname, '.'])
    if code != 0:
        if args.manage == 'multi':
            _print_verbose(1, 'Restoring original manage.py ...')
            safe_rename(manage_delete_name, manage_script_name)
        raise SystemExit(code)
    os.chmod(manage_script_name, mode0755)

    if args.manage == 'multi':
        safe_delete(manage_delete_name)
        _print_verbose(2, 'Removing project specific configuration from manage.py ...')
        with open(manage_script_name, 'a+') as f:
            lines = f.readlines()
            f.seek(0)
            f.truncate()
            for line in lines:
                if 'import os' not in line and 'DJANGO_SETTINGS_MODULE' not in line:
                    f.write(line)


def _split_project():
    global args
    global profiles
    global projectname
    global settings

    profiles = ('develop', 'staging', 'production')
    filenames = ('__init__', 'common') + profiles

    _print_verbose(2, 'Creating directories ...')
    os.mkdir('%s.media' % projectname)
    os.mkdir('%s.static' % projectname)
    os.mkdir('%s.templates' % projectname)
    os.mkdir(os.path.join(projectname, 'settings'))

    _print_verbose(2, 'Converting settings to deployment profiles (%s) ...' % ', '.join(profiles))
    os.rename(os.path.join(projectname, 'settings.py'),
              os.path.join(projectname, 'settings', 'common.py'))

    settings = DjangoSettingsManager(projectname, *filenames)
    settings.append_lines('__init__',
                          '"""',
                          'Modularized settings generated by django Organice setup. http://organice.io',
                          'This solution follows the second recommendation from',
                          'http://www.sparklewise.com/django-settings-for-production-and-development-best-practices/',
                          '"""',
                          'from .develop import *')
    for prof in profiles:
        settings.append_lines(prof,
                              '# Django project settings for %s environment' % prof.capitalize(),
                              '',
                              'from .common import *')

    # out-of-the-box Django values relevant for deployment
    settings.delete_var('common', 'SITE_ID')
    settings.insert_lines('common',
                          '_ = lambda s: s',
                          'import os',
                          'PROJECT_PATH = os.sep.join(__file__.split(os.sep)[:-3])',
                          '',
                          'SITE_ID = 1')
    settings.set_value('common', 'MEDIA_ROOT', "os.path.join(PROJECT_PATH, '%s.media')" % projectname)
    settings.set_value('common', 'STATIC_ROOT', "os.path.join(PROJECT_PATH, '%s.static')" % projectname)
    settings.set_value('common', 'MEDIA_URL', "'/media/'")
    settings.set_value('common', 'USE_I18N', False)
    settings.move_var('common', profiles, 'DEBUG')
    settings.move_var('common', profiles, 'TEMPLATE_DEBUG')
    settings.move_var('common', profiles, 'ALLOWED_HOSTS')
    settings.move_var('common', profiles, 'DATABASES')
    settings.move_var('common', profiles, 'MEDIA_ROOT')
    settings.move_var('common', profiles, 'STATIC_ROOT')
    settings.move_var('common', profiles, 'SECRET_KEY')
    for prof in ('staging', 'production'):
        settings.set_value(prof, 'DEBUG', False)
        settings.set_value_lines(prof, 'ALLOWED_HOSTS',
                                 '[',
                                 "    '%s.organice.io'," % (args.account if args.account else projectname),
                                 "    '%s'," % (args.domain if args.domain else 'www.example.com'),
                                 ']')


def _configure_database():
    global args
    global projectname
    global settings

    db_template = django.template.Template("""{
    'default': {
        'ENGINE': 'django.db.backends.{{ engine }}',  # 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': {{ database|safe }},  # path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '{{ username|safe }}',
        'PASSWORD': '{{ password|safe }}',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}""")
    db_context = django.template.Context({
        'engine': 'sqlite3',
        'database': "os.path.join(PROJECT_PATH, '%s.sqlite')" % projectname,
        'username': '',
        'password': '',
    })

    _print_verbose(2, 'Configuring database for all profiles ...')
    settings.set_value('develop', 'DATABASES', db_template.render(db_context))

    db_context['engine'] = args.engine if args.engine else ''
    db_context['database'] = "'%s'" % (args.database if args.database else '')
    db_context['username'] = args.username if args.username else ''
    db_context['password'] = args.password if args.password else ''

    for prof in ('staging', 'production'):
        settings.set_value(prof, 'DATABASES', db_template.render(db_context))


def _configure_installed_apps():
    global settings

    _print_verbose(2, adding_settings_for('installed apps'))
    settings.delete_var('common', 'INSTALLED_APPS')
    settings.append_lines('common',
                          'INSTALLED_APPS = (',
                          "    'django.contrib.auth',",
                          "    'django.contrib.comments',",
                          "    'django.contrib.contenttypes',",
                          "    'django.contrib.sessions',",
                          "    'django.contrib.sites',",
                          "    'django.contrib.messages',",
                          "    'django.contrib.staticfiles',",
                          "    'django.contrib.admin',",
                          "#    'organice_theme_add-your-theme-here',",
                          "    'organice_theme',",
                          "    'organice',",
                          "    'cms',",
                          "    'mptt',",
                          "    'menus',",
                          "    'south',",
                          "    'sekizai',",
                          "    'reversion',",
                          "    'easy_thumbnails',",
                          "    'media_tree',",
                          "    'cms.plugins.text',",
                          "    'cms.plugins.link',",
                          "    'cms.plugins.flash',",
                          "    'cms.plugins.googlemap',",
                          "    'cms.plugins.inherit',",
                          "    'cms.plugins.video',",
                          "    'media_tree.contrib.cms_plugins.media_tree_image',",
                          "    'media_tree.contrib.cms_plugins.media_tree_gallery',",
                          "    'media_tree.contrib.cms_plugins.media_tree_slideshow',",
                          "    'media_tree.contrib.cms_plugins.media_tree_listing',",
                          "    'cmsplugin_contact',",
                          "    'cmsplugin_zinnia',",
                          "    'tagging',",
                          "    'todo',",
                          "    'emencia.django.newsletter',",
                          "    'tinymce',",
                          "    'simple_links',",
                          "    'zinnia',",
                          "    'allauth',",
                          "    'allauth.account',",
                          "    'allauth.socialaccount',",
                          "    'allauth.socialaccount.providers.amazon',",
                          "#    'allauth.socialaccount.providers.angellist',",
                          "    'allauth.socialaccount.providers.bitbucket',",
                          "    'allauth.socialaccount.providers.bitly',",
                          "    'allauth.socialaccount.providers.dropbox',",
                          "#    'allauth.socialaccount.providers.facebook',",
                          "#    'allauth.socialaccount.providers.flickr',",
                          "#    'allauth.socialaccount.providers.feedly',",
                          "    'allauth.socialaccount.providers.github',",
                          "    'allauth.socialaccount.providers.google',",
                          "    'allauth.socialaccount.providers.instagram',",
                          "#    'allauth.socialaccount.providers.linkedin',",
                          "    'allauth.socialaccount.providers.linkedin_oauth2',",
                          "#    'allauth.socialaccount.providers.openid',",
                          "#    'allauth.socialaccount.providers.persona',",
                          "    'allauth.socialaccount.providers.soundcloud',",
                          "    'allauth.socialaccount.providers.stackexchange',",
                          "#    'allauth.socialaccount.providers.tumblr',",
                          "#    'allauth.socialaccount.providers.twitch',",
                          "#    'allauth.socialaccount.providers.twitter',",
                          "    'allauth.socialaccount.providers.vimeo',",
                          "#    'allauth.socialaccount.providers.vk',",
                          "#    'allauth.socialaccount.providers.weibo',",
                          "    'allauth.socialaccount.providers.xing',",
                          "    'analytical',",
                          ')')


def _configure_authentication():
    global settings

    _print_verbose(2, adding_settings_for('user profiles and authentication'))
    settings.delete_var('common', 'SERVER_EMAIL')
    settings.set_value_lines('common', 'ADMINS',
                             '(',
                             "    ('Your Name', 'noreply@example.com'),",
                             ')',
                             'SERVER_EMAIL = ADMINS[0][1]')
    settings.append_lines('common',
                          'AUTHENTICATION_BACKENDS = (',
                          "    'django.contrib.auth.backends.ModelBackend',",
                          "    'allauth.account.auth_backends.AuthenticationBackend',",
                          ')')
    settings.set_value('common', 'LOGIN_REDIRECT_URL', "'/'")
    settings.set_value('develop', 'EMAIL_BACKEND', "'django.core.mail.backends.console.EmailBackend'")


def _configure_cms():
    global projectname
    global settings

    _print_verbose(2, adding_settings_for('django CMS'))
    settings.delete_var('common', 'MIDDLEWARE_CLASSES')
    settings.append_lines('common',
                          'MIDDLEWARE_CLASSES = (',
                          "    'django.contrib.sessions.middleware.SessionMiddleware',",
                          "    'django.contrib.messages.middleware.MessageMiddleware',",
                          "    'django.contrib.auth.middleware.AuthenticationMiddleware',",
                          "    'solid_i18n.middleware.SolidLocaleMiddleware',",
                          "    'django.middleware.common.CommonMiddleware',",
                          "    'django.middleware.doc.XViewMiddleware',",
                          "    'django.middleware.csrf.CsrfViewMiddleware',",
                          "    'cms.middleware.page.CurrentPageMiddleware',",
                          "    'cms.middleware.user.CurrentUserMiddleware',",
                          "    'cms.middleware.toolbar.ToolbarMiddleware',",
                          "    'cms.middleware.language.LanguageCookieMiddleware',",
                          ')')
    # must be set both in order to make solid_i18n work properly
    settings.set_value_lines('common', 'LANGUAGE_CODE', "'en'",
                             'LANGUAGES = (',
                             "    ('en', _('English')),",
                             "    ('de', _('German')),",
                             "    ('it', _('Italian')),",
                             ')')
    settings.set_value('common', 'CMS_USE_TINYMCE', False)
    settings.append_lines('common',
                          'CMS_TEMPLATES = (',
                          "    ('cms_base.html', 'Template for normal content pages'),",
                          "    ('cms_bookmarks.html', 'Template for the bookmarks page'),",
                          ')')
    settings.delete_var('common', 'TEMPLATE_DIRS')
    settings.append_lines('common',
                          'TEMPLATE_DIRS = (',
                          "    # Don't forget to use absolute paths, not relative paths.",
                          "    os.path.join(PROJECT_PATH, '%s.templates')," % projectname,
                          "    os.path.join(PROJECT_PATH, '%s.templates', 'zinnia')," % projectname,
                          ')')
    settings.delete_var('common', 'TEMPLATE_LOADERS')
    settings.append_lines('common',
                          'TEMPLATE_LOADERS = (',
                          "    'django.template.loaders.filesystem.Loader',",
                          "    'django.template.loaders.app_directories.Loader',",
                          "    'apptemplates.Loader',",
                          ')')
    settings.append_lines('common',
                          'TEMPLATE_CONTEXT_PROCESSORS = (',
                          "    'django.contrib.auth.context_processors.auth',",
                          "    'django.core.context_processors.i18n',",
                          "    'django.core.context_processors.request',",
                          "    'django.core.context_processors.media',",
                          "    'django.core.context_processors.static',",
                          "    'allauth.account.context_processors.account',",
                          "    'allauth.socialaccount.context_processors.socialaccount',",
                          "    'cms.context_processors.media',",
                          "    'sekizai.context_processors.sekizai',",
                          "    'organice.context_processors.expose',",
                          ')')
    settings.append_lines('common',
                          'MEDIA_TREE_MEDIA_BACKENDS = (',
                          "    'media_tree.contrib.media_backends.easy_thumbnails.EasyThumbnailsBackend',",
                          ')')


def _configure_newsletter():
    global settings

    _print_verbose(2, adding_settings_for('Emencia Newsletter'))
    settings.append_lines('common',
                          "NEWSLETTER_DEFAULT_HEADER_SENDER = 'Your Organization <newsletter@your.domain>'",
                          'NEWSLETTER_USE_TINYMCE = True',
                          'NEWSLETTER_TEMPLATES = [',
                          "    { 'title': 'Sample template for newsletter',",
                          "      'src': '/media/newsletter/templates/sample-template.html',",
                          "      'description': 'Newsletter template tabular sample' },",
                          ']',
                          'TINYMCE_DEFAULT_CONFIG = {',
                          "    'height': 450,",
                          "    'width': 800,",
                          "    'convert_urls': False,",
                          "    'plugins': 'table,paste,searchreplace,template,advlist,autolink,autosave',",
                          "    'template_templates': NEWSLETTER_TEMPLATES,",
                          "    'theme': 'advanced',",
                          "    'theme_advanced_toolbar_location': 'top',",
                          "    'theme_advanced_buttons1': 'template,|,formatselect,' \\",
                          "        '|,bold,italic,underline,strikethrough,|,undo,redo,' \\",
                          "        '|,justifyleft,justifycenter,justifyright,justifyfull,' \\",
                          "        '|,bullist,numlist,dt,dd,|,outdent,indent,|,blockquote',",
                          "    'theme_advanced_buttons2': 'tablecontrols,|,forecolor,backcolor,' \\",
                          "        '|,hr,image,anchor,link,unlink,|,visualaid,code',",
                          "    'theme_advanced_resizing': True,",
                          '}')


def _configure_blog():
    global settings

    _print_verbose(2, adding_settings_for('Zinnia Blog'))
    settings.append_lines('common',
                          '# use plugin system of django-cms in blog entries',
                          "ZINNIA_ENTRY_BASE_MODEL = 'cmsplugin_zinnia.placeholder.EntryPlaceholder'",
                          "ZINNIA_WYSIWYG = 'wymeditor'")
    settings.append_lines('common',
                          'SOUTH_MIGRATION_MODULES = {',
                          '    # integration of EntryPlaceholder (django CMS) into Zinnia',
                          "    'zinnia': 'organice.migrations.zinnia',",
                          "    'easy_thumbnails': 'easy_thumbnails.south_migrations',",
                          '}')


def _configure_set_custom():
    """
    Set variable values specified via any ``--set`` command line options.
    """
    global args
    global settings

    if args.set:
        _print_verbose(2, adding_settings_for(", ".join([v[1] for v in args.set])))
        for dest, var, value in args.set:
            settings.set_value(dest, var, value)


def _generate_urls_conf():
    global projectname

    _print_verbose(2, 'Configuring project URLs ...')
    gen_by_comment = '# generated by django Organice'
    project = DjangoModuleManager(projectname)
    project.add_file('urls', lines=(gen_by_comment, 'from organice.urls import urlpatterns'))
    project.save_files()


def _generate_webserver_conf():
    global args
    global profiles
    global projectname

    if args.webserver == 'apache':
        settings.move_var('common', profiles, 'WSGI_APPLICATION')
    else:
        _print_verbose(2, 'Generating lighttp web server configuration ...')
        os.unlink(os.path.join(projectname, 'wsgi.py'))
        settings.delete_var('common', 'WSGI_APPLICATION')
        settings.append_lines('common',
                              '# Override the server-derived value of SCRIPT_NAME',
                              '# See http://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#lighttpdfastcgiandothers',  # noqa
                              "FORCE_SCRIPT_NAME = ''")
        settings.move_var('common', profiles, 'FORCE_SCRIPT_NAME')

        conf_template = django.template.Template("""# Lighttp web server configuration

# {{ account }}.organice.io
$HTTP["host"] =~ "^({{ account }}.organice.io|{{ custom_domain }})$" {
    fastcgi.server = (
        "/django.fcgi" => (
            "main" => (
                "socket" => env.HOME + "/{{ organice }}/{{ projectname }}.sock",
                "check-local" => "disable",
            )
        ),
    )
    alias.url = (
        "/media/" => env.HOME + "/{{ organice }}/{{ projectname }}.media/",
        "/static/" => env.HOME + "/{{ organice }}/{{ projectname }}.static/",
    )
    url.rewrite-once = (
        "^(/media/.*)$" => "/$1",
        "^(/static/.*)$" => "/$1",
        "^/favicon\.ico$" => "/media/favicon.ico",
        "^(/.*)$" => "/django.fcgi$1",
    )
    # enforce optional custom domain name
    {{ ignore }}$HTTP["host"] != "{{ custom_domain }}" {
    {{ ignore }}    url.redirect = ("^/django.fcgi(.*)$" => "http://{{ custom_domain }}$1")
    {{ ignore }}}
}
""")
        conf_context = django.template.Context({
            'organice': 'organice',
            'projectname': projectname,
            'account': args.account if args.account else projectname,
            'custom_domain': args.domain if args.domain else 'www.example.com',
            'ignore': '' if args.domain else '#',
        })
        conf_file = open('%s.conf' % projectname, 'w')
        conf_file.write(conf_template.render(conf_context))
        conf_file.close()


def _show_final_hints():
    global projectname
    global settings

    suggest_editing = ('ADMINS', 'TIME_ZONE', 'LANGUAGE_CODE', 'LANGUAGES', 'EMAIL_BACKEND', 'SERVER_EMAIL')
    suggest_adding = ()

    _print_verbose(1, 'Done. Enjoy your organiced day!')
    _print_verbose(2, '')
    _print_verbose(2, 'Please visit file `%s` and edit or add the variables: %s' %
                   (settings.get_file('common').name, ", ".join(suggest_editing + suggest_adding)))
    _print_verbose(2, 'Please visit file `%s` and configure your development database in: %s' %
                   (settings.get_file('develop').name, 'DATABASES'))
    _print_verbose(3, 'See https://docs.djangoproject.com/en/1.5/ref/settings/ for details.')
    _print_verbose(3, '')
    _print_verbose(3, '1) To initialize your development database run: `python manage.py syncdb --migrate`')
    _print_verbose(3, '2) You can then run your development server with: `python manage.py runserver`')
    _print_verbose(3, '3) To prepare your production server you may run: '
                   '`python manage.py collectstatic --link --settings=%s.settings.production`' % projectname)


def startproject():
    """
    Starts a new django Organice project by first generating a Django project
    using ``django-admin.py``, and then modifying the project settings.
    """
    global settings

    _evaluate_command_line()
    django.conf.settings.configure()  # for django.template init only

    _create_project()
    _split_project()
    _configure_database()
    _configure_installed_apps()
    _configure_authentication()
    _configure_cms()
    _configure_newsletter()
    _configure_blog()
    _configure_set_custom()

    _generate_urls_conf()
    _generate_webserver_conf()

    settings.save_files()
    _show_final_hints()


if __name__ == "__main__":
    startproject()

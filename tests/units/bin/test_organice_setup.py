from os import getcwd, rmdir, stat, unlink
from os.path import exists, isfile, join
from pytest import fixture
from shutil import rmtree
from stat import S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IXGRP, S_IROTH, S_IXOTH
from subprocess import call
from ..utils import probe_values_in_tuple, probe_values_in_list
from ..utils import pytest_generate_tests  # noqa


def settings_file_for(project, profile):
    """Returns the relative path to a settings file"""
    return join(project, 'settings', profile + '.py')


def run_management_cmd_for(project_name, testcmd_args, *command_args):
    """
    Execute a management command, including the required settings if needed.
    """
    manage_cmd = ['python', 'manage.py'] + list(command_args)
    if 'multi' in testcmd_args:
        manage_cmd += ['--settings', '%s.settings' % project_name]
    return call(manage_cmd)


@fixture(scope="class")
def setup(request, project_name):
    """test setup"""

    @request.addfinalizer
    def teardown():
        """test teardown"""
        try:
            unlink('manage.py')
            rmtree(project_name)
            for suffix in ('media', 'static', 'templates'):
                rmdir(project_name + '.' + suffix)
            unlink(project_name + '.conf')
            rmdir(getcwd())
        except Exception:
            pass


class TestOrganiceSetup(object):
    """
    Tests for the startproject() function.
    Py.test class, must have no ``__init__`` method!
    """
    scenarios = [
        ['default', dict(project_name='test_project_default', cmd_args=[])],
        ['multi', dict(project_name='test_project_multi', cmd_args=['--manage', 'multi'])],
        ['nginx', dict(project_name='test_project_nginx', cmd_args=['--webserver', 'nginx'])],
        ['lighttp', dict(project_name='test_project_lighttp', cmd_args=['--webserver', 'lighttp'])],
    ]

    def test_01_create_project(self, tmpdir, project_name, cmd_args, setup):
        """
        - does setup command execute and finish?
        - does manage script exist, and is it executable?
        """
        mode0755 = oct(S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH)[-3:]
        manage_script = 'manage.py'
        tmpdir.chdir()
        exit_code = call(['organice-setup',
                          '--set', 'develop', 'TEST_SETTING_01', "'test value'",
                          '--verbosity=0'] + cmd_args + [project_name])
        assert exit_code == 0
        assert isfile(manage_script)
        file_mode = oct(stat(manage_script).st_mode)[-3:]
        assert file_mode == mode0755
        with open(manage_script) as script:
            content = script.read()
            assert 'execute_from_command_line' in content
            assert ('multi' in cmd_args) != ('DJANGO_SETTINGS_MODULE' in content)

    def test_02_split_project(self, project_name, cmd_args):
        """
        - are subdirectories accessible as modules?
        - do profiles exist?
        """
        project_module = join(project_name, '__init__.py')
        project_settings_module = join(project_name, 'settings', '__init__.py')
        assert exists(project_module)
        assert exists(project_settings_module)
        assert exists(settings_file_for(project_name, 'common'))
        assert exists(settings_file_for(project_name, 'develop'))
        assert exists(settings_file_for(project_name, 'staging'))
        assert exists(settings_file_for(project_name, 'production'))
        for profile in (settings_file_for(project_name, 'staging'),
                        settings_file_for(project_name, 'production')):
            content = open(profile).read()
            assert "ALLOWED_HOSTS = [\n" \
                   "    '%(target_domain)s',\n" \
                   "    '%(redirect_domain)s',\n" \
                   "]\n" % {
                       'target_domain': '%s.organice.io' % project_name,
                       'redirect_domain': 'www.%s.organice.io' % project_name,
                   } in content
            assert 'DEBUG = ' in content
            assert 'ALLOWED_HOSTS = [\n' in content
            assert 'DATABASES = {\n' in content
            assert 'MEDIA_ROOT = ' in content
            assert 'STATIC_ROOT = ' in content
            assert 'SECRET_KEY = ' in content

    def test_03_configure_database(self, project_name, cmd_args):
        selected = (cmd_args[cmd_args.index('--database') + 1] if '--database' in cmd_args else "")
        db_engine = {
            settings_file_for(project_name, 'develop'): "sqlite3",
            settings_file_for(project_name, 'staging'): selected,
            settings_file_for(project_name, 'production'): selected,
        }
        for profile in (settings_file_for(project_name, 'develop'),
                        settings_file_for(project_name, 'staging'),
                        settings_file_for(project_name, 'production')):
            content = open(profile).read()
            assert ("DATABASES = {\n"
                    "    'default': {\n"
                    "        'ENGINE': 'django.db.backends.%s'," %
                    db_engine[profile]) in content

    def test_04_configure_installed_apps(self, project_name, cmd_args):
        common_settings = open(settings_file_for(project_name, 'common')).read()
        required_apps = [
            'organice',
            # 'organice_theme',
        ]
        assert probe_values_in_list(common_settings, ['INSTALLED_APPS = ['], required_apps)
        # TODO: Test for: ORGANICE_DJANGO_APPS + ORGANICE_CMS_APPS + ORGANICE_BLOG_APPS
        # TODO:  + ORGANICE_AUTH_APPS + ORGANICE_UTIL_APPS

    def test_04_configure_installed_dev(self, project_name, cmd_args):
        dev_settings = open(settings_file_for(project_name, 'develop')).read()
        required_apps = [
            'behave_django',
        ]
        assert probe_values_in_tuple(dev_settings, 'DEVELOP_APPS', required_apps)

    def test_05_configure_authentication(self, project_name, cmd_args):
        common_settings = open(settings_file_for(project_name, 'common')).read()
        assert 'SERVER_EMAIL = ADMINS[0][1]' in common_settings
        assert "AUTHENTICATION_BACKENDS = (\n" \
               "    'django.contrib.auth.backends.ModelBackend',\n" \
               "    'allauth.account.auth_backends.AuthenticationBackend',\n" \
               ")\n" in common_settings
        assert "ACCOUNT_AUTHENTICATION_METHOD = 'email'\n" in common_settings
        assert "ACCOUNT_EMAIL_REQUIRED = True\n" in common_settings
        assert "ACCOUNT_USERNAME_REQUIRED = False\n" in common_settings
        assert "LOGIN_REDIRECT_URL = '/'\n" in common_settings
        assert "LOGIN_URL = '/login'\n" in common_settings
        assert "LOGOUT_URL = '/logout'\n" in common_settings

        develop_settings = open(settings_file_for(project_name, 'develop')).read()
        assert "EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'" \
               in develop_settings

    def test_06_configure_templates(self, project_name, cmd_args):
        common_settings = open(settings_file_for(project_name, 'common')).read()
        required_ctx = [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'cms.context_processors.cms_settings',
            'sekizai.context_processors.sekizai',
            'organice.context_processors.expose',
        ]
        required_loaders = [
            'apptemplates.Loader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
        assert probe_values_in_list(common_settings, [
            "TEMPLATES = [", "{", "'OPTIONS': {", "'context_processors': ["
        ], required_ctx)
        assert probe_values_in_list(common_settings, [
            "TEMPLATES = [", "{", "'OPTIONS': {", "'loaders': ["
        ], required_loaders)

    def test_07_configure_cms(self, project_name, cmd_args):
        common_settings = open(settings_file_for(project_name, 'common')).read()
        required_middleware = [
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'cms.middleware.language.LanguageCookieMiddleware',
            'cms.middleware.page.CurrentPageMiddleware',
            'cms.middleware.toolbar.ToolbarMiddleware',
            'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.utils.ApphookReloadMiddleware',
            'solid_i18n.middleware.SolidLocaleMiddleware',
        ]
        required_mediatree = [
            'media_tree.contrib.media_backends.easy_thumbnails.EasyThumbnailsBackend',
        ]
        assert probe_values_in_list(common_settings, ['MIDDLEWARE_CLASSES = ['], required_middleware)
        assert probe_values_in_list(common_settings, ['MEDIA_TREE_MEDIA_BACKENDS = ['], required_mediatree)

    def test_08_configure_newsletter(self, project_name, cmd_args):
        common_settings = open(settings_file_for(project_name, 'common')).read()
        assert "NEWSLETTER_DEFAULT_HEADER_SENDER = " in common_settings
        assert "NEWSLETTER_USE_TINYMCE = True" in common_settings
        assert "NEWSLETTER_TEMPLATES = [\n" in common_settings
        assert "TINYMCE_DEFAULT_CONFIG = {\n" in common_settings

    def test_09_configure_blog(self, project_name, cmd_args):
        common_settings = open(settings_file_for(project_name, 'common')).read()
        required_migrations = [
            "zinnia': 'organice.migrations.zinnia"
        ]
        assert "ZINNIA_ENTRY_BASE_MODEL = 'cmsplugin_zinnia.placeholder.EntryPlaceholder'" \
               in common_settings
        assert "ZINNIA_WYSIWYG = 'wymeditor'" in common_settings
        assert probe_values_in_list(common_settings, ["MIGRATION_MODULES = {"], required_migrations)

    def test_10_configure_set_custom(self, project_name, cmd_args):
        settings = open(settings_file_for(project_name, 'develop')).read()
        assert "TEST_SETTING_01 = 'test value'" in settings

    def test_11_generate_urls_conf(self, project_name, cmd_args):
        project_urls_file = join(project_name, 'urls.py')
        assert exists(project_urls_file)
        assert open(project_urls_file).read() == '# generated by django Organice\n' \
                                                 'from organice.urls import urlpatterns  # noqa\n'

    def test_12_generate_webserver_conf(self, project_name, cmd_args):
        webserver = (cmd_args[cmd_args.index('--webserver') + 1]
                     if '--webserver' in cmd_args else 'apache')
        wsgi_conf = join(project_name, 'wsgi.py')
        webserv_conf = project_name + '.conf'
        conf_values = {
            'project': project_name,
            'target_domain': '%s.organice.io' % project_name,
            'redirect_domain': 'www.%s.organice.io' % project_name,
        }

        if webserver == 'lighttp':
            assert not exists(wsgi_conf)
            assert exists(webserv_conf)
            content = open(webserv_conf).read()
            for required_line in [
                r'$HTTP["host"] =~ "^(%(target_domain)s|%(redirect_domain)s)$" {',
                r'                "socket" => env.HOME + "/organice/%(project)s.sock",',
                r'        "/media/" => env.HOME + "/organice/%(project)s.media/",',
                r'        "/static/" => env.HOME + "/organice/%(project)s.static/",',
                r'        "^/favicon\.ico$" => "/media/favicon.ico",',
                r'$HTTP["host"] != "%(target_domain)s" {',
                r'    url.redirect = ("^/django.fcgi(.*)$" => "http://%(target_domain)s$1")',
            ]:
                line = (required_line % conf_values) + '\n'
                assert line in content, 'Missing in lighttp configuration: %s' % line.strip()

            for profile in (settings_file_for(project_name, 'develop'),
                            settings_file_for(project_name, 'staging'),
                            settings_file_for(project_name, 'production')):
                content = open(profile).read()
                assert 'WSGI_APPLICATION = ' not in content
                assert "FORCE_SCRIPT_NAME = ''" in content

        elif webserver == 'nginx':
            assert exists(wsgi_conf)
            assert exists(webserv_conf)
            content = open(webserv_conf).read()
            for required_line in [
                r'upstream %(project)s {',
                r'    server_name %(target_domain)s;',
                r'        alias /home/organice/organice/%(project)s.static/;',
                r'        alias /home/organice/organice/%(project)s.media/;',
                r'    server_name %(redirect_domain)s;',
                r'    return 301 $scheme://%(target_domain)s$request_uri;',
            ]:
                line = (required_line % conf_values) + '\n'
                assert line in content, 'Missing in nginx configuration: %s' % line.strip()

            for profile in (settings_file_for(project_name, 'develop'),
                            settings_file_for(project_name, 'staging'),
                            settings_file_for(project_name, 'production')):
                content = open(profile).read()
                assert 'WSGI_APPLICATION = ' in content
                assert "FORCE_SCRIPT_NAME = ''" in content

        elif webserver == 'apache':  # default
            assert exists(wsgi_conf)
            for profile in (settings_file_for(project_name, 'develop'),
                            settings_file_for(project_name, 'staging'),
                            settings_file_for(project_name, 'production')):
                content = open(profile).read()
                assert 'WSGI_APPLICATION = ' in content

    def test_13_system_check(self, project_name, cmd_args):
        exit_code = run_management_cmd_for(project_name, cmd_args, 'check')
        assert exit_code == 0, 'Validation of Django project failed. See output for details.'

    def test_14_init_database(self, project_name, cmd_args):
        """NOTE: This is the first test that takes significantly more time to complete"""
        # TODO: move this and subsequent calls to management command
        exit_code = run_management_cmd_for(project_name, cmd_args, 'migrate')
        assert exit_code == 0, 'Initialization of project database failed. See output for details.'

    def test_15_populate_database(self, project_name, cmd_args):
        # TODO: fix fixture 'organice_sample_content' and add it to the list below
        for fixture_file in ['organice_auth_providers']:
            exit_code = run_management_cmd_for(project_name, cmd_args, 'loaddata', fixture_file)
            assert exit_code == 0, 'Loading fixture `%s` into database failed.' % fixture

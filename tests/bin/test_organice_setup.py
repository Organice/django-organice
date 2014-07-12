from os import rmdir, stat, unlink
from os.path import exists, join
from pytest import fixture
from shutil import rmtree
from stat import S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IXGRP, S_IROTH, S_IXOTH, ST_MODE
from subprocess import call
from ..utils import probe_values_in_tuple


class TestOrganiceSetup():
    """Tests for the startproject() function. Py.test class, must have no ``__init__`` method!"""
    project_name = 'test_project'
    project_manage_script = 'manage.py'
    project_settings_common_file = join(project_name, 'settings', 'common.py')
    project_settings_develop_file = join(project_name, 'settings', 'develop.py')
    project_settings_staging_file = join(project_name, 'settings', 'staging.py')
    project_settings_production_file = join(project_name, 'settings', 'production.py')

    @fixture(scope="module")
    def setup(self, request):
        """test setup"""

        @request.addfinalizer
        def teardown():
            """test teardown"""
            rmtree(self.project_name)
            for suffix in ('media', 'static', 'templates'):
                rmdir(self.project_name + '.' + suffix)
            unlink('manage.py')

    def test_01_create_project(self, tmpdir, setup):
        """
        - does setup command execute and finish?
        - does manage script exist, and is it executable?
        """
        mode0755 = oct(S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH)
        tmpdir.chdir()
        exit_code = call(['organice-setup',
                          '--set', 'develop', 'TEST_SETTING_01', "'test value'",
                          '--verbosity=0', self.project_name])
        assert exit_code == 0
        assert exists(self.project_manage_script)
        file_mode = oct(stat(self.project_manage_script)[ST_MODE])[-4:]
        assert file_mode == mode0755

    def test_02_split_project(self):
        """
        - are subdirectories accessible as modules?
        - do profiles exist?
        """
        project_module = join(self.project_name, '__init__.py')
        project_settings_module = join(self.project_name, 'settings', '__init__.py')
        assert exists(project_module)
        assert exists(project_settings_module)
        assert exists(self.project_settings_common_file)
        assert exists(self.project_settings_develop_file)
        assert exists(self.project_settings_staging_file)
        assert exists(self.project_settings_production_file)
        for profile in (self.project_settings_staging_file,
                        self.project_settings_production_file):
            content = open(profile).read()
            assert "ALLOWED_HOSTS = [\n" \
                   "    '%(subdomain)s.organice.io',\n" \
                   "    '%(domain)s',\n" \
                   "]\n" % {
                       'subdomain': self.project_name,
                       'domain': 'www.example.com',
                   } in content
            assert 'DEBUG = ' in content
            assert 'TEMPLATE_DEBUG = ' in content
            assert 'ALLOWED_HOSTS = [\n' in content
            assert 'DATABASES = {\n' in content
            assert 'MEDIA_ROOT = ' in content
            assert 'STATIC_ROOT = ' in content
            assert 'SECRET_KEY = ' in content

    def test_03_configure_database(self):
        # TODO: evaluate (args.database if args.database else '') for staging and production
        db_engine = {
            self.project_settings_develop_file: "sqlite3",
            self.project_settings_staging_file: "",
            self.project_settings_production_file: "",
        }
        for profile in (self.project_settings_develop_file,
                        self.project_settings_staging_file,
                        self.project_settings_production_file):
            content = open(profile).read()
            assert ("DATABASES = {\n"
                    "    'default': {\n"
                    "        'ENGINE': 'django.db.backends.%s'," %
                    db_engine[profile]) in content

    def test_04_configure_installed_apps(self):
        content = open(self.project_settings_common_file).read()
        required_apps = {
            'organice',
            'organice_theme',
            'cms',
            'zinnia',
            'emencia.django.newsletter',
            'todo',
            'media_tree',
            'analytical',
            'allauth',
            'allauth.account',
            'allauth.socialaccount',
            'allauth.socialaccount.providers.facebook',
        }
        probe_values_in_tuple(content, 'INSTALLED_APPS', required_apps)

    def test_05_configure_authentication(self):
        common_settings = open(self.project_settings_common_file).read()
        assert 'SERVER_EMAIL = ADMINS[0][1]' in common_settings
        assert "AUTHENTICATION_BACKENDS = (\n" \
               "    'django.contrib.auth.backends.ModelBackend',\n" \
               "    'allauth.account.auth_backends.AuthenticationBackend',\n" \
               ")\n" in common_settings
        assert "LOGIN_REDIRECT_URL = '/'\n" in common_settings

        develop_settings = open(self.project_settings_develop_file).read()
        assert "EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'" \
               in develop_settings

    def test_06_configure_cms(self):
        common_settings = open(self.project_settings_common_file).read()
        required_middleware = {
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'solid_i18n.middleware.SolidLocaleMiddleware',
            'cms.middleware.page.CurrentPageMiddleware',
            'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.toolbar.ToolbarMiddleware',
            'cms.middleware.language.LanguageCookieMiddleware',
        }
        required_loaders = {
            'apptemplates.Loader',
        }
        required_ctx = {
            'allauth.account.context_processors.account',
            'allauth.socialaccount.context_processors.socialaccount',
            'cms.context_processors.media',
            'sekizai.context_processors.sekizai',
            'organice.context_processors.expose',
        }
        required_mediatree = {
            'media_tree.contrib.media_backends.easy_thumbnails.EasyThumbnailsBackend',
        }
        assert probe_values_in_tuple(common_settings, 'MIDDLEWARE_CLASSES', required_middleware)
        assert probe_values_in_tuple(common_settings, 'TEMPLATE_LOADERS', required_loaders)
        assert probe_values_in_tuple(common_settings, 'TEMPLATE_CONTEXT_PROCESSORS', required_ctx)
        assert probe_values_in_tuple(common_settings, 'MEDIA_TREE_MEDIA_BACKENDS',
                                     required_mediatree)

    def test_07_configure_newsletter(self):
        common_settings = open(self.project_settings_common_file).read()
        assert "NEWSLETTER_DEFAULT_HEADER_SENDER = " in common_settings
        assert "NEWSLETTER_USE_TINYMCE = True" in common_settings
        assert "NEWSLETTER_TEMPLATES = [\n" in common_settings
        assert "TINYMCE_DEFAULT_CONFIG = {\n" in common_settings

    def test_08_configure_blog(self):
        common_settings = open(self.project_settings_common_file).read()
        assert "ZINNIA_ENTRY_BASE_MODEL = 'cmsplugin_zinnia.placeholder.EntryPlaceholder'" \
               in common_settings
        assert "ZINNIA_WYSIWYG = 'wymeditor'" in common_settings
        assert "SOUTH_MIGRATION_MODULES = {" in common_settings

    def test_09_configure_set_custom(self):
        settings = open(self.project_settings_develop_file).read()
        assert "TEST_SETTING_01 = 'test value'" in settings

    def test_10_generate_urls_conf(self):
        project_urls_file = join(self.project_name, 'urls.py')
        assert exists(project_urls_file)
        assert open(project_urls_file).read() == '# generated by django Organice\n' \
                                                 'from organice.urls import urlpatterns\n'

    def test_11_generate_webserver_conf(self):
        wsgi_conf = join(self.project_name, 'wsgi.py')
        lighttp_conf = self.project_name + '.conf'
        conf_values = {
            'project': self.project_name,
            'domain': 'www.example.com',
        }

        if True:  # TODO: if called with "--webserver apache":
            assert exists(wsgi_conf)
            for profile in (self.project_settings_develop_file,
                            self.project_settings_staging_file,
                            self.project_settings_production_file):
                content = open(profile).read()
                assert 'WSGI_APPLICATION = ' in content
        elif False:  # TODO: elif called with "--webserver lighttp":
            assert not exists(wsgi_conf)
            assert exists(lighttp_conf)
            for line in [
                '$HTTP["host"] =~ "^(%(project)s.organice.io|%(domain)s)$" {\n',
                '                "socket" => env.HOME + "/organice/%(project)s.sock",\n',
                '        "/media/" => env.HOME + "/organice/%(project)s.media/",\n',
                '        "/static/" => env.HOME + "/organice/%(project)s.static/",\n',
                '$HTTP["host"] != "{{ custom_domain }}" {\n',
                '    url.redirect = ("^/django.fcgi(.*)$" => "http://%(domain)s$1")\n',
            ]:
                assert (line % conf_values) in lighttp_conf

            for profile in (self.project_settings_develop_file,
                            self.project_settings_staging_file,
                            self.project_settings_production_file):
                content = open(profile).read()
                assert 'WSGI_APPLICATION = ' not in content
                assert "FORCE_SCRIPT_NAME = ''" in content

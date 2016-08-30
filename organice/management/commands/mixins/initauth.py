"""
A label command (sub-command) for the Organice management command.
"""
from allauth.socialaccount.models import SocialApp
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.utils import IntegrityError
from django.utils.translation import ugettext as _

from organice.auth.groups import GUESTS_GROUP, EDITORS_GROUP, PUBLISHERS_GROUP
from organice.auth.permissions import (
    BASIC_APP_PERMISSIONS, EDITOR_APP_PERMISSIONS, PUBLISHER_APP_PERMISSIONS,
    BASIC_CMS_PERMISSIONS, EDITOR_CMS_PERMISSIONS, PUBLISHER_CMS_PERMISSIONS,
    reset_group_permissions)


class InitauthCommandMixin(object):
    """Setup of authentication in the database"""

    def initauth_command(self):
        """Initialize social auth providers with generic data"""
        self.create_social_apps()
        self.create_admin_account()
        self.create_groups_and_permissions()

    def create_social_apps(self):
        """Configuration for social apps (django-allauth)"""
        if self.verbosity >= 1:
            self.stdout.write(_('Prepare configuration of SocialAuth apps ...'))

        count = 0
        social_auth_providers = [
            ('amazon', 'Amazon'),
            ('bitbucket', 'Bitbucket'),
            ('bitly', 'Bitly'),
            ('dropbox_oauth2', 'Dropbox'),
            ('facebook', 'Facebook'),
            ('github', 'GitHub'),
            ('gitlab', 'GitLab'),
            ('google', 'Google'),
            ('instagram', 'Instagram'),
            ('linkedin_oauth2', 'LinkedIn'),
            ('pinterest', 'Pinterest'),
            ('slack', 'Slack'),
            ('soundcloud', 'SoundCloud'),
            ('stackexchange', 'Stack Exchange'),
            ('twitter', 'Twitter'),
            ('vimeo', 'Vimeo'),
            ('windowslive', 'Windows Live'),
            ('xing', 'Xing'),
        ]
        for provider, name in social_auth_providers:
            app_config, created = SocialApp.objects.get_or_create(provider=provider, name=name)
            if not created:
                if self.verbosity >= 1:
                    self.stdout.write(_('App configuration already exists: {} -- leaving it untouched.')
                                      .format(name))
            else:
                app_config.secret = app_config.client_id = 'xxxx'
                app_config.key = ''
                app_config.save()
                count += 1

        if self.verbosity >= 1:
            self.stdout.write(_('{count} SocialAuth app configuration drafts added, {total} in total.')
                              .format(count=count, total=SocialApp.objects.count()))

    def create_admin_account(self):
        """Django Admin superuser account for Demo site"""
        username, password, email = 'admin', 'demo', 'demo@organice.io'
        if self.verbosity >= 1:
            self.stdout.write(_('Create admin user ({}/{}) ...').format(username, password))
        try:
            call_command('createsuperuser', '--noinput', username=username, email=email, verbosity=self.verbosity)
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
        except IntegrityError:
            if self.verbosity >= 1:
                self.stdout.write(_("WARNING: Looks like a user '{}' already exists.".format(username)))

    def create_groups_and_permissions(self):
        """
        Prepare a simple editorial workflow using Django Contrib Auth and
        django CMS permissions.
        """

        if self.verbosity >= 1:
            self.stdout.write(_('Prepare groups and permissions for editorial workflow ...'))

        reset_group_permissions(GUESTS_GROUP,
                                app_permissions=BASIC_APP_PERMISSIONS,
                                cms_permissions=BASIC_CMS_PERMISSIONS)
        reset_group_permissions(EDITORS_GROUP,
                                app_permissions=EDITOR_APP_PERMISSIONS,
                                cms_permissions=EDITOR_CMS_PERMISSIONS)
        reset_group_permissions(PUBLISHERS_GROUP,
                                app_permissions=PUBLISHER_APP_PERMISSIONS,
                                cms_permissions=PUBLISHER_CMS_PERMISSIONS)

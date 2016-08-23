"""
A label command (sub-command) for the Organice management command.
"""
from allauth.socialaccount.models import SocialApp
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.utils import IntegrityError
from django.utils.translation import ugettext as _


class InitauthCommandMixin(object):

    def initauth_command(self):
        """
        Initialize social auth providers with generic data
        """
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

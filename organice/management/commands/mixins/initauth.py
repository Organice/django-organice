"""
A label command (sub-command) for the Organice management command.
"""
from allauth.socialaccount.models import SocialApp
from django.utils.translation import ugettext as _


class InitauthCommandMixin(object):

    def initauth_command(self):
        """
        Initialize social auth providers with generic data
        """
        self.stdout.write(_('Prepare configuration of SocialAuth apps ...'))

        count = 0
        social_auth_providers = [
            ('amazon', 'Amazon'),
            ('bitbucket', 'Bitbucket'),
            ('bitly', 'Bitly'),
            ('dropbox', 'Dropbox'),
            ('github', 'GitHub'),
            ('google', 'Google'),
            ('instagram', 'Instagram'),
            ('linkedin_oauth2', 'LinkedIn (OAuth2)'),
            ('soundcloud', 'SoundCloud'),
            ('stackexchange', 'Stack Exchange'),
            ('vimeo', 'Vimeo'),
            ('xing', 'Xing'),
        ]
        for provider, name in social_auth_providers:
            app_config, created = SocialApp.objects.get_or_create(provider=provider, name=name)
            if not created:
                self.stdout.write(_('App configuration already exists: {} -- leaving it untouched.')
                                  .format(name))
            else:
                app_config.secret = app_config.client_id = 'xxxx'
                app_config.key = ''
                app_config.save()
                count += 1

        self.stdout.write(_('{count} SocialAuth app configuration drafts added, {total} in total.')
                          .format(count=count, total=SocialApp.objects.count()))

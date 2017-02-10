"""
A label command (sub-command) for the Organice management command.
"""
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.utils.translation import ugettext as _


class InitdbCommandMixin(object):

    def initdb_command(self):
        """
        Initialize the Organice database and apps
        """
        self.log(_('Initialize database:'))
        call_command('migrate', verbosity=self.verbosity)

        self.log(_('Configure site #1 ...'))
        site, created = Site.objects.get_or_create(id=1)
        site.name, site.domain = 'Organice Demo', 'demo.organice.io'
        site.save()

"""
A label command (sub-command) for the Organice management command.
"""
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.utils.translation import ugettext as _


class InitdbCommandMixin(object):

    def initdb_command(self):
        """
        Initialize the Organice database and apps
        """
        self.stdout.write(_('Initialize database ...'))
        call_command('migrate')

        self.stdout.write(_('Configure site #1 ...'))
        s, created = Site.objects.get_or_create(id=1)
        s.name, s.domain = 'Organice Demo', 'demo.organice.io'
        s.save()

        self.stdout.write(_('Create admin user ...'))
        call_command('createsuperuser', '--username', 'admin', '--email', 'demo@organice.io', '--noinput')
        u = User.objects.get(username='admin')
        u.set_password('admin')
        u.save()

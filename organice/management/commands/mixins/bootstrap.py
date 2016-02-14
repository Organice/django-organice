"""
A label command (sub-command) for the Organice management command.
"""
from django.utils.translation import ugettext as _


class BootstrapCommandMixin(object):

    def bootstrap_command(self):
        """
        Initialize Organice = initdb, initauth, initcms, initblog
        """
        self.handle_label('initdb')
        self.handle_label('initauth')
        self.handle_label('initcms')
        self.handle_label('initblog')

        if self.verbosity >= 1:
            self.stdout.write(_('Have an organiced day!'))

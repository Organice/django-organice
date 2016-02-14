"""
Management commands for django Organice.
"""
from django.core.management.base import CommandError, LabelCommand
from django.utils.translation import ugettext as _

from .mixins.bootstrap import BootstrapCommandMixin
from .mixins.initauth import InitauthCommandMixin
from .mixins.initblog import InitblogCommandMixin
from .mixins.initcms import InitcmsCommandMixin
from .mixins.initdb import InitdbCommandMixin


class Command(InitauthCommandMixin,
              InitblogCommandMixin,
              InitcmsCommandMixin,
              InitdbCommandMixin,
              BootstrapCommandMixin,
              LabelCommand):
    """
    A management command with quite a few label commands.
    Each included mixin provides a label command, implemented as
    ``<label>_command()`` function in that class.
    """
    label = 'command'

    @property
    def label_commands(self):
        """
        A dictionary with a label (key) and a function pointer (value).
        Extracts all functions ending with "_command" from the Mixins.
        """
        tail = '_command'
        commands = {
            func[:-len(tail)]: getattr(self, func)
            for func in dir(self.__class__) if func.endswith(tail)
        }
        return commands

    @property
    def cmd_labels(self):
        """A string-ified list of labels for all available commands"""
        return ', '.join(sorted(self.label_commands))

    @property
    def cmd_help(self):
        """A string-ified list of commands and their docstrings"""
        cmd_help = ['{} ({})'.format(label, func.__doc__.strip())
                    for label, func in self.label_commands.items()]
        return ', '.join(sorted(cmd_help))

    @property
    def help(self):
        help = _('Organice management commands: {}')
        return help.format(self.cmd_labels)

    @property
    def missing_args_message(self):
        msg = _('Please use one of the commands: {}. Use --help for more details.')
        return msg.format(self.cmd_labels)

    def add_arguments(self, parser):
        """
        Add help text to our argparse command. Overrides method of LabelCommand.
        """
        parser.add_argument('args', metavar=self.label, nargs='+', help=self.cmd_help)

    def handle(self, *labels, **options):
        """Make ``verbosity`` available as an attribute, for ease of use."""
        self.verbosity = options.get('verbosity')
        super(Command, self).handle(*labels, **options)

    def handle_label(self, label, **options):
        try:
            self.label_commands[label]()
        except KeyError:
            msg = _('Invalid command: {}. Use --help for detailed usage.')
            raise CommandError(msg.format(label))

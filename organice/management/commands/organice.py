"""
Management commands for django Organice.
"""
from django.core.management.base import LabelCommand
from django.utils.translation import ugettext as _

from .mixins.bootstrap import BootstrapCommandMixin


class Command(BootstrapCommandMixin, LabelCommand):
    label = 'command'

    @property
    def label_commands(self):
        """
        A dictionary with a label (key) and a function pointer (value).
        Extracts all functions ending with "_command" from the Mixins.
        """
        tail = '_command'
        commands = {
            func[:len(tail) + 1]: getattr(self, func)
            for func in dir(self.__class__) if func.endswith(tail)
        }
        return commands

    @property
    def commands_labels(self):
        """A string-ified list of labels for all available commands"""
        return ', '.join(self.label_commands)

    @property
    def commands_help(self):
        """A string-ified list of commands and their docstrings"""
        cmd_help = ['{} ({})'.format(label, func.__doc__.strip())
                    for label, func in self.label_commands.items()]
        return ', '.join(cmd_help)

    @property
    def help(self):
        help = _('Organice management commands: {}')
        return help.format(self.commands_labels)

    @property
    def missing_args_message(self):
        msg = _('Please use one of the commands: {}. Use --help for more details.')
        return msg.format(self.commands_labels)

    def add_arguments(self, parser):
        """
        Add help text to our argparse command. Overrides method of LabelCommand.
        """
        self.parser = parser
        parser.add_argument('args', metavar=self.label, nargs='+', help=self.commands_help)

    def handle_label(self, label, **options):
        try:
            self.label_commands[label]()
        except KeyError:
            msg = _('Invalid command: {}. Use --help for detailed usage.')
            self.parser.error(msg.format(label))

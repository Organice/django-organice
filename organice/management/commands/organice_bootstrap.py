"""
Management commands for django Organice.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from cms.api import create_page
from cms.models import Title


def create_user(username, email='testuser@organice.io'):
    print(u"Creating user {} with password {} ...".format(username, username))
    try:
        User.objects.get(username=username).delete()
        print(u"Warning: deleted existing user {} first.".format(username))
    except User.DoesNotExist:
        pass
    User.objects.create_user(username, email, username).save()


def delete_page(title):
    """Delete all pages with the given title."""
    while len(Title.objects.filter(title=title)):
        # Pain! filter, because django CMS creates 2 titles for each page
        page = Title.objects.filter(title=title).first().page
        print(u"Warning: deleting existing page {} first ...".format(title))
        page.delete()


def add_cms_page(title, template='cms_base.html', parent=None):
    print(u"Creating page {} ...".format(title))
    delete_page(title)
    pk = create_page(title, template, language='en', in_navigation=True, published=True, parent=parent)
    return pk


class Command(BaseCommand):
    help = 'Organice management commands.'

    def handle(self, *args, **options):
        self.stdout.write('Initialize database ...')
        call_command('migrate')

        self.stdout.write('Create admin user ...')
        # call_command('createsuperuser', '--username', 'admin', '--email', 'you@example.com', '--noinput')
        u = User.objects.get(username='admin')
        u.set_password('admin')
        u.save()

        self.stdout.write('Generate menu structure ...')
        add_cms_page(_('Home'))
        about_page = add_cms_page(_('About Us'))
        programs_page = add_cms_page(_('Programs'))
        add_cms_page(_('Sponsors'))
        add_cms_page(_('Jobs'), parent=about_page)
        add_cms_page(_('Contact Us'), parent=about_page)
        add_cms_page(_('Directions'), parent=about_page)
        add_cms_page(_('Juniors'), parent=programs_page)
        add_cms_page(_('Seniors'), parent=programs_page)

        # self.stdout.write('Generate sample content ...')
        # TODO: take over sample content from sample_content fixtures

        # self.stdout.write('Generate provider data for social authentication ...')
        # TODO: generate auth providers instead of loading fixtures

        self.stdout.write('Have an organiced day!')

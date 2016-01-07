from cms.api import add_plugin, create_page
from cms.models import Title
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


def create_user(username, email='testuser@organice.io'):
    print(_('Creating user {} with password {} ...').format(username, username))
    try:
        User.objects.get(username=username).delete()
        print("Warning: deleted existing user {} first.".format(username))
    except User.DoesNotExist:
        pass
    User.objects.create_user(username, email, username).save()


def delete_page(title):
    """Delete all pages with the given title."""
    while len(Title.objects.filter(title=title)):
        # Pain! filter, because django CMS creates 2 titles for each page
        page = Title.objects.filter(title=title).first().page
        print(_('Warning: deleting existing page {} first ...').format(title))
        page.delete()
        # TODO: Check, are plugins deleted automatically? (cascading)


def add_cms_page(title, template='cms_base.html', parent=None, lang='en', plugins=()):
    """
    Create or recreate a CMS page including a content plugins with content in them.
    """
    print(_('Creating page {} ...').format(title))
    delete_page(title)
    page = create_page(title, template, language=lang, in_navigation=True, parent=parent)
    placeholder = page.placeholders.get(slot='content')
    for plugin, body in plugins:
        add_plugin(placeholder, plugin, lang, body=body)
    page.publish(lang)
    return page

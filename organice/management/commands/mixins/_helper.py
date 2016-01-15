"""
Helper functions for our management command mixins.
"""
from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _

from cms.api import add_plugin, create_page
from cms.models import Title
from zinnia.managers import PUBLISHED
from zinnia.models.category import Category


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


def add_cms_page(title, slug=None, template='cms_base.html', parent=None, lang='en', plugins=()):
    """
    Create or recreate a CMS page including content plugins with content in them.
    """
    print(_('Creating CMS page {} ...').format(title))
    delete_page(title)
    page = create_page(title=title, template=template, language=lang,
                       slug=slug, in_navigation=True, parent=parent)
    placeholder = page.placeholders.get(slot='content')
    for plugin, fieldset in plugins:
        add_plugin(placeholder, plugin, lang, **fieldset)
    page.publish(lang)
    return page


def add_blog_category(slug, title, description=None):
    """
    Create or recreate a blog category.
    """
    print(_('Creating blog category {} ...').format(title))
    category, created = Category.objects.get_or_create(slug=slug, title=title, description=description)
    return category


def add_blog_entry(slug, title, excerpt=None, lang='en', categories=(), tags=None, plugins=()):
    """
    Create or recreate a blog entry including content plugins with content in them.
    """
    print(_('Creating blog entry {} ...').format(title))
    Entry = apps.get_model('zinnia', 'entry')
    entry, created = Entry.objects.get_or_create(
            slug=slug, title=title, excerpt=excerpt, tags=tags, status=PUBLISHED)
    entry.sites = Site.objects.all()
    entry.categories.add(*categories)
    for plugin, fieldset in plugins:
        add_plugin(entry.content_placeholder, plugin, lang, **fieldset)
    entry.save()
    return entry

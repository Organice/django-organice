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


class HelperMixin(object):
    """
    A few static helper methods for management command execution.
    """

    def create_user(self, username, email='testuser@organice.io'):
        if self.verbosity >= 1:
            print(_('Creating user {} with password {} ...').format(username, username))
        try:
            User.objects.get(username=username).delete()
            if self.verbosity >= 1:
                print("WARNING: User {} exists. Deleting them first.".format(username))
        except User.DoesNotExist:
            pass
        User.objects.create_user(username, email, username).save()

    def delete_page(self, title):
        """Delete all pages with the given title."""
        # ts = Title.objects.filter(title=title)
        # print("**** {}".format(ts))
        # if not len(ts):
        #     print(Title.objects.filter())
        #     ts = [ Title.objects.get(title=title) ]
        # assert len(ts) > 0, 'Only {} items found of {}'.format(len(ts), title)
        while len(Title.objects.filter(title=title)):
            # Pain! filter, because django CMS creates 2 titles for each page
            page = Title.objects.filter(title=title).first().page
            if self.verbosity >= 1:
                print(_('WARNING: Page {} exists. Deleting it first ...').format(title))
            page.delete()
            # TODO: Check, are plugins deleted automatically? (cascading)

    def add_cms_page(self, title, slug=None, template='cms_base.html', lang='en',
                     parent=None, in_navigation=True, plugins=()):
        """
        Create or recreate a CMS page including content plugins with content in them.
        """
        if self.verbosity >= 1:
            print(_('Creating CMS page {} ...').format(title))
        self.delete_page(title)
        page = create_page(title=title, template=template, language=lang,
                           slug=slug, in_navigation=in_navigation, parent=parent)
        placeholder = page.placeholders.get(slot='content')
        for plugin, fieldset in plugins:
            add_plugin(placeholder, plugin, lang, **fieldset)
        page.publish(lang)
        return page

    def add_blog_category(self, slug, title, description=None):
        """
        Create or recreate a blog category.
        """
        if self.verbosity >= 1:
            print(_('Creating blog category {} ...').format(title))
        category, created = Category.objects.get_or_create(slug=slug, title=title, description=description)
        return category

    def add_blog_entry(self, slug, title, excerpt=None, lang='en', categories=(), tags=None, plugins=()):
        """
        Create or recreate a blog entry including content plugins with content in them.
        """
        if self.verbosity >= 1:
            print(_('Creating blog entry {} ...').format(title))
        entry_model = apps.get_model('zinnia', 'entry')
        entry, created = entry_model.objects.get_or_create(slug=slug, title=title, status=PUBLISHED)
        entry.excerpt = excerpt
        entry.tags = tags
        entry.sites = Site.objects.all()
        entry.categories.add(*categories)
        for plugin, fieldset in plugins:
            add_plugin(entry.content_placeholder, plugin, lang, **fieldset)
        entry.save()
        return entry

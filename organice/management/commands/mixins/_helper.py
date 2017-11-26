"""
Helper functions for our management command mixins.
"""
from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _

from cms.api import add_plugin, create_page
from cms.models import Page, Title
from zinnia.managers import PUBLISHED
from zinnia.models.category import Category


class HelperMixin(object):
    """
    A few static helper methods for management command execution.
    """

    def log(self, text, level=1):
        """Console log output"""
        if self.verbosity >= level:
            self.stdout.write(text)

    def create_user(self, username, email='testuser@organice.io'):
        self.log(_('Creating user {} with password {} ...').format(username, username))
        try:
            User.objects.get(username=username).delete()
            self.log(_('WARNING: User {} exists. Deleting them first.').format(username))
        except User.DoesNotExist:
            pass
        User.objects.create_user(username, email, username).save()

    def delete_page(self, title, template):
        """Delete all pages with the given title/template combination."""
        pages_using_template = Page.objects.filter(template=template)
        title_candidates = Title.objects.filter(title=title, page__in=pages_using_template)
        page_candidates = [title.page for title in title_candidates]
        for page in page_candidates:
            page.delete()
        title_candidates.delete()

    def add_cms_page(self, title, slug=None, template='cms_base.html', lang='en',
                     parent=None, in_navigation=True, plugins=(),
                     apphook=None, apphook_namespace=None):
        """
        Create or recreate a CMS page including content plugins with content in them.
        """
        self.log(_('Creating CMS page {} ...').format(title))
        self.delete_page(title, template)
        page = create_page(title=title, template=template, language=lang,
                           slug=slug, in_navigation=in_navigation, parent=parent,
                           apphook=apphook, apphook_namespace=apphook_namespace)
        placeholder = page.placeholders.get(slot='content')
        for plugin, fieldset in plugins:
            add_plugin(placeholder, plugin, lang, **fieldset)
        page.publish(lang)
        return page

    def add_blog_category(self, slug, title, description=None):
        """
        Create or recreate a blog category.
        """
        self.log(_('Creating blog category {} ...').format(title))
        category, created = Category.objects.get_or_create(slug=slug, title=title, description=description)
        return category

    def add_blog_entry(self, slug, title, excerpt=None, lang='en', categories=(), tags=None, plugins=()):
        """
        Create or recreate a blog entry including content plugins with content in them.
        """
        self.log(_('Creating blog entry {} ...').format(title))
        entry_model = apps.get_model('zinnia', 'entry')
        try:
            entry, created = entry_model.objects.get_or_create(slug=slug, title=title, status=PUBLISHED)
        except entry_model.DoesNotExist:
            entry = entry_model.objects.create(slug=slug, title=title, status=PUBLISHED)
        entry.excerpt = excerpt
        entry.tags = tags
        entry.sites = Site.objects.all()
        entry.categories.add(*categories)
        for plugin, fieldset in plugins:
            add_plugin(entry.content_placeholder, plugin, lang, **fieldset)
        entry.save()
        return entry

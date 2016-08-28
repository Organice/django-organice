"""
A label command (sub-command) for the Organice management command.
"""
from allauth.socialaccount.models import SocialApp
from cms.models import GlobalPagePermission
from django.contrib.auth.models import Group, User, Permission
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.db.utils import IntegrityError
from django.utils.translation import ugettext as _


def permission_list(permission_names):
    """
    Convert a  list of 'app_label.model.codename' permission names to a
    list of (django.contrib.auth) Permission.
    """
    # parameters of get_by_natural_key() for zipping
    keywords = ['app_label', 'model', 'codename']

    return [
        Permission.objects.get_by_natural_key(
            **dict(zip(keywords, app_model_perm.split('.')))
        ) for app_model_perm in permission_names]


class InitauthCommandMixin(object):
    def initauth_command(self):
        """
        Initialize social auth providers with generic data
        """
        self.create_social_apps()
        self.create_admin_account()
        self.create_groups_and_permissions()

    def create_social_apps(self):
        """Configuration for social apps (django-allauth)"""
        if self.verbosity >= 1:
            self.stdout.write(_('Prepare configuration of SocialAuth apps ...'))

        count = 0
        social_auth_providers = [
            ('amazon', 'Amazon'),
            ('bitbucket', 'Bitbucket'),
            ('bitly', 'Bitly'),
            ('dropbox_oauth2', 'Dropbox'),
            ('facebook', 'Facebook'),
            ('github', 'GitHub'),
            ('gitlab', 'GitLab'),
            ('google', 'Google'),
            ('instagram', 'Instagram'),
            ('linkedin_oauth2', 'LinkedIn'),
            ('pinterest', 'Pinterest'),
            ('slack', 'Slack'),
            ('soundcloud', 'SoundCloud'),
            ('stackexchange', 'Stack Exchange'),
            ('twitter', 'Twitter'),
            ('vimeo', 'Vimeo'),
            ('windowslive', 'Windows Live'),
            ('xing', 'Xing'),
        ]
        for provider, name in social_auth_providers:
            app_config, created = SocialApp.objects.get_or_create(provider=provider, name=name)
            if not created:
                if self.verbosity >= 1:
                    self.stdout.write(_('App configuration already exists: {} -- leaving it untouched.')
                                      .format(name))
            else:
                app_config.secret = app_config.client_id = 'xxxx'
                app_config.key = ''
                app_config.save()
                count += 1

        if self.verbosity >= 1:
            self.stdout.write(_('{count} SocialAuth app configuration drafts added, {total} in total.')
                              .format(count=count, total=SocialApp.objects.count()))

    def create_admin_account(self):
        """Django Admin superuser account for Demo site"""
        username, password, email = 'admin', 'demo', 'demo@organice.io'
        if self.verbosity >= 1:
            self.stdout.write(_('Create admin user ({}/{}) ...').format(username, password))
        try:
            call_command('createsuperuser', '--noinput', username=username, email=email, verbosity=self.verbosity)
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
        except IntegrityError:
            if self.verbosity >= 1:
                self.stdout.write(_("WARNING: Looks like a user '{}' already exists.".format(username)))

    def create_groups_and_permissions(self):
        """
        Prepare a simple editorial workflow using Django Contrib Auth and
        django CMS permissions.
        """
        basic_permissions = permission_list([
            'cms.aliaspluginmodel.add_aliaspluginmodel',
            'cms.aliaspluginmodel.change_aliaspluginmodel',
            'cms.aliaspluginmodel.delete_aliaspluginmodel',
            'cms.cmsplugin.add_cmsplugin',
            'cms.cmsplugin.change_cmsplugin',
            'cms.cmsplugin.delete_cmsplugin',
            'cms.page.change_page',
            'cms.page.edit_static_placeholder',
            'cms.page.view_page',
            'cms.pageuser.add_pageuser',
            'cms.pageuser.change_pageuser',
            'cms.pageuser.delete_pageuser',
            'cms.pageusergroup.add_pageusergroup',
            'cms.pageusergroup.change_pageusergroup',
            'cms.pageusergroup.delete_pageusergroup',
            'cms.placeholder.add_placeholder',
            'cms.placeholder.change_placeholder',
            'cms.placeholder.delete_placeholder',
            'cms.placeholderreference.add_placeholderreference',
            'cms.placeholderreference.change_placeholderreference',
            'cms.placeholderreference.delete_placeholderreference',
            'cms.staticplaceholder.add_staticplaceholder',
            'cms.staticplaceholder.change_staticplaceholder',
            'cms.staticplaceholder.delete_staticplaceholder',
            'cms.title.change_title',
            'cms.urlconfrevision.add_urlconfrevision',
            'cms.urlconfrevision.change_urlconfrevision',
            'cms.urlconfrevision.delete_urlconfrevision',
            'cms.usersettings.add_usersettings',
            'cms.usersettings.change_usersettings',
            'cms.usersettings.delete_usersettings',
            'cmsplugin_zinnia.calendarentriesplugin.add_calendarentriesplugin',
            'cmsplugin_zinnia.calendarentriesplugin.change_calendarentriesplugin',
            'cmsplugin_zinnia.calendarentriesplugin.delete_calendarentriesplugin',
            'cmsplugin_zinnia.latestentriesplugin.add_latestentriesplugin',
            'cmsplugin_zinnia.latestentriesplugin.change_latestentriesplugin',
            'cmsplugin_zinnia.latestentriesplugin.delete_latestentriesplugin',
            'cmsplugin_zinnia.queryentriesplugin.add_queryentriesplugin',
            'cmsplugin_zinnia.queryentriesplugin.change_queryentriesplugin',
            'cmsplugin_zinnia.queryentriesplugin.delete_queryentriesplugin',
            'cmsplugin_zinnia.randomentriesplugin.add_randomentriesplugin',
            'cmsplugin_zinnia.randomentriesplugin.change_randomentriesplugin',
            'cmsplugin_zinnia.randomentriesplugin.delete_randomentriesplugin',
            'cmsplugin_zinnia.selectedentriesplugin.add_selectedentriesplugin',
            'cmsplugin_zinnia.selectedentriesplugin.change_selectedentriesplugin',
            'cmsplugin_zinnia.selectedentriesplugin.delete_selectedentriesplugin',
            'djangocms_googlemap.googlemap.add_googlemap',
            'djangocms_googlemap.googlemap.change_googlemap',
            'djangocms_googlemap.googlemap.delete_googlemap',
            'djangocms_inherit.inheritpageplaceholder.add_inheritpageplaceholder',
            'djangocms_inherit.inheritpageplaceholder.change_inheritpageplaceholder',
            'djangocms_inherit.inheritpageplaceholder.delete_inheritpageplaceholder',
            'djangocms_link.link.add_link',
            'djangocms_link.link.change_link',
            'djangocms_link.link.delete_link',
            'djangocms_picture.picture.add_picture',
            'djangocms_picture.picture.change_picture',
            'djangocms_picture.picture.delete_picture',
            'djangocms_text_ckeditor.text.add_text',
            'djangocms_text_ckeditor.text.change_text',
            'djangocms_text_ckeditor.text.delete_text',
            'tagging.tag.add_tag',
            'tagging.tag.change_tag',
            'tagging.tag.delete_tag',
            'tagging.taggeditem.add_taggeditem',
            'tagging.taggeditem.change_taggeditem',
            'tagging.taggeditem.delete_taggeditem',
            'zinnia.category.add_category',
            'zinnia.category.change_category',
            'zinnia.entry.add_entry',
            'zinnia.entry.can_view_all',
            'zinnia.entry.change_entry',
        ])
        editor_permissions = basic_permissions + permission_list([
            'cms.page.add_page',
            'cms.page.delete_page',
            'cms.pagepermission.add_pagepermission',
            'cms.pagepermission.change_pagepermission',
            'cms.pagepermission.delete_pagepermission',
            'cms.placeholder.use_structure',
            'cms.title.add_title',
            'cms.title.delete_title',
            'zinnia.entry.can_change_author',
            'zinnia.entry.can_change_status',
        ])
        publisher_permissions = editor_permissions + permission_list([
            'cms.globalpagepermission.add_globalpagepermission',
            'cms.globalpagepermission.change_globalpagepermission',
            'cms.globalpagepermission.delete_globalpagepermission',
            'cms.page.publish_page',
        ])

        if self.verbosity >= 1:
            self.stdout.write(_('Prepare groups and permissions for editorial workflow ...'))

        sites = Site.objects.all()

        guests_group, created = Group.objects.get_or_create(name='Guests')
        guests_group.permissions = basic_permissions
        guests_group.save()

        guests_perms, created = GlobalPagePermission.objects.get_or_create(group=guests_group)
        guests_perms.sites = sites
        guests_perms.can_edit = True
        guests_perms.can_add = \
            guests_perms.can_delete = \
            guests_perms.can_change_advanced_settings = \
            guests_perms.can_change_permissions = \
            guests_perms.can_move_page = \
            guests_perms.can_recover_page = \
            guests_perms.can_view = \
            guests_perms.can_publish = False
        guests_perms.save()

        editors_group, created = Group.objects.get_or_create(name='Editors')
        editors_group.permissions = editor_permissions
        editors_group.save()

        editors_perms, created = GlobalPagePermission.objects.get_or_create(group=editors_group)
        editors_perms.sites = sites
        editors_perms.can_edit = \
            editors_perms.can_add = \
            editors_perms.can_delete = \
            editors_perms.can_change_advanced_settings = \
            editors_perms.can_change_permissions = \
            editors_perms.can_move_page = \
            editors_perms.can_recover_page = True
        editors_perms.can_view = \
            editors_perms.can_publish = False
        editors_perms.save()

        publishers_group, created = Group.objects.get_or_create(name='Publishers')
        publishers_group.permissions = publisher_permissions
        publishers_group.save()

        publishers_perms, created = GlobalPagePermission.objects.get_or_create(group=publishers_group)
        publishers_perms.sites = sites
        publishers_perms.can_edit = \
            publishers_perms.can_add = \
            publishers_perms.can_delete = \
            publishers_perms.can_change_advanced_settings = \
            publishers_perms.can_change_permissions = \
            publishers_perms.can_move_page = \
            publishers_perms.can_recover_page = \
            publishers_perms.can_view = \
            publishers_perms.can_publish = True
        publishers_perms.save()

"""
Django app permissions used in Organice.

Permissions for an editorial workflow.
See ``adapters.EditorialWorkflowMixin`` for explanations. Background reading:
http://stackoverflow.com/questions/8806705/django-cms-and-editorial-workflows#answer-39128706
"""
from cms.models import GlobalPagePermission
from django.contrib.auth.models import Group, Permission


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


def reset_group_permissions(group_name, app_permissions=(), cms_permissions=(), sites=()):
    """
    Initialize a Django auth group assigning a set of Django app permissions,
    and global page permissions for django CMS.

    :param group_name: Name of Django auth group to create or reset
    :param app_permissions: list of Django auth Permission objects
    :param cms_permissions: dictionary of django CMS permissions
    :param sites: optional list of Django sites objects (None: all sites)
    :return: the created or updated group model instance
    """
    group, created = Group.objects.get_or_create(name=group_name)
    group.permissions = permission_list(app_permissions)
    group.save()

    perms, created = GlobalPagePermission.objects.get_or_create(group=group)
    for attrib, value in dict(cms_permissions).items():
        setattr(perms, attrib, value)
    perms.sites = sites
    perms.save()

    return group


BASIC_CMS_PERMISSIONS = {
    'can_edit': True,
    'can_add': False,
    'can_delete': False,
    'can_change_advanced_settings': False,
    'can_change_permissions': False,
    'can_move_page': False,
    'can_recover_page': False,
    'can_view': False,
    'can_publish': False,
}

EDITOR_CMS_PERMISSIONS = {
    'can_edit': True,
    'can_add': True,
    'can_delete': True,
    'can_change_advanced_settings': True,
    'can_change_permissions': True,
    'can_move_page': True,
    'can_recover_page': True,
    'can_view': True,
    'can_publish': False,
}

PUBLISHER_CMS_PERMISSIONS = {
    'can_edit': True,
    'can_add': True,
    'can_delete': True,
    'can_change_advanced_settings': True,
    'can_change_permissions': True,
    'can_move_page': True,
    'can_recover_page': True,
    'can_view': True,
    'can_publish': True,
}

BASIC_APP_PERMISSIONS = [
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
    'djangocms_inherit.inheritpageplaceholder.add_inheritpageplaceholder',
    'djangocms_inherit.inheritpageplaceholder.change_inheritpageplaceholder',
    'djangocms_inherit.inheritpageplaceholder.delete_inheritpageplaceholder',
    'djangocms_link.link.add_link',
    'djangocms_link.link.change_link',
    'djangocms_link.link.delete_link',
    'djangocms_maps.maps.add_maps',
    'djangocms_maps.maps.change_maps',
    'djangocms_maps.maps.delete_maps',
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
]

EDITOR_APP_PERMISSIONS = BASIC_APP_PERMISSIONS + [
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
]

PUBLISHER_APP_PERMISSIONS = EDITOR_APP_PERMISSIONS + [
    'cms.globalpagepermission.add_globalpagepermission',
    'cms.globalpagepermission.change_globalpagepermission',
    'cms.globalpagepermission.delete_globalpagepermission',
    'cms.page.publish_page',
]

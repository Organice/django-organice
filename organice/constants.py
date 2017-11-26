"""
Constants for django Organice.
"""
ORGANICE_DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]

ORGANICE_CMS_APPS = [
    'cms',
    'mptt',
    'menus',
    'sekizai',
    'treebeard',
    'easy_thumbnails',
    'djangocms_admin_style',
    # 'djangocms_file',
    'djangocms_maps',
    'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    # 'djangocms_teaser',
    'djangocms_text_ckeditor',
    # 'media_tree',
    # 'media_tree.contrib.cms_plugins.media_tree_image',
    # 'media_tree.contrib.cms_plugins.media_tree_gallery',
    # 'media_tree.contrib.cms_plugins.media_tree_slideshow',
    # 'media_tree.contrib.cms_plugins.media_tree_listing',
    # 'form_designer.contrib.cms_plugins.form_designer_form',
]

ORGANICE_BLOG_APPS = [
    'cmsplugin_zinnia',
    'django_comments',
    'tagging',
    'zinnia',
]

ORGANICE_NEWSLETTER_APPS = [
    # 'emencia.django.newsletter',
    'tinymce',
]

ORGANICE_UTIL_APPS = [
    'analytical',
    'simple_links',
    'todo',
]

ORGANICE_AUTH_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.amazon',
    # 'allauth.socialaccount.providers.angellist',
    'allauth.socialaccount.providers.bitbucket',
    'allauth.socialaccount.providers.bitly',
    'allauth.socialaccount.providers.dropbox_oauth2',
    'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.flickr',
    # 'allauth.socialaccount.providers.feedly',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.linkedin_oauth2',
    # 'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.pinterest',
    'allauth.socialaccount.providers.slack',
    'allauth.socialaccount.providers.soundcloud',
    'allauth.socialaccount.providers.stackexchange',
    # 'allauth.socialaccount.providers.tumblr',
    # 'allauth.socialaccount.providers.twitch',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.vimeo',
    # 'allauth.socialaccount.providers.vk',
    # 'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.windowslive',
    'allauth.socialaccount.providers.xing',
]

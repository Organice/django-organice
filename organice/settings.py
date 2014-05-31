"""Default settings for django Organice"""
from django.conf import settings

URL_PATH_ADMIN = getattr(settings, 'ORGANICE_URL_PATH_ADMIN', 'admin')
URL_PATH_BLOG = getattr(settings, 'ORGANICE_URL_PATH_BLOG', 'blog')
URL_PATH_NEWSLETTER = getattr(settings, 'ORGANICE_URL_PATH_NEWSLETTER', 'newsletter')
URL_PATH_TODO = getattr(settings, 'ORGANICE_URL_PATH_TODO', 'todo')

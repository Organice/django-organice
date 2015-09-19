"""
Default urls for django Organice
"""
from django.conf.urls import include, url
from solid_i18n.urls import solid_i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from .settings import URL_PATH_ADMIN, URL_PATH_BLOG, URL_PATH_TODO

admin.autodiscover()

urlpatterns = solid_i18n_patterns(
    '',
    url(r'^' + URL_PATH_ADMIN + '/', include(admin.site.urls)),
    # url(r'^' + URL_PATH_NEWSLETTER + '/', include('emencia.django.newsletter.urls.newsletter')),
    # url(r'^' + URL_PATH_NEWSLETTER + '/', include('emencia.django.newsletter.urls.mailing_list')),
    # url(r'^' + URL_PATH_NEWSLETTER + '/track/', include('emencia.django.newsletter.urls.tracking')),
    # url(r'^' + URL_PATH_NEWSLETTER + '/stats/', include('emencia.django.newsletter.urls.statistics')),
    url(r'^' + URL_PATH_BLOG + '/', include('zinnia.urls', namespace='zinnia')),
    url(r'^' + URL_PATH_TODO + '/', include('todo.urls')),
    url(r'^', include('allauth.urls')),
    url(r'^', include('cms.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

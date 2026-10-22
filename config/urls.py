from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from contact.views import contact
from cv.views import cv, home

admin.site.site_header = "Zhaohan Zhang — site admin"
admin.site.site_title = "Site admin"

urlpatterns = [
    path("", home, name="home"),
    path("cv/", cv, name="cv"),
    path("blog/", include("blog.urls")),
    path("projects/", include("projects.urls")),
    path("contact/", contact, name="contact"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

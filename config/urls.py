from django.contrib import admin
from django.urls import include, path

urlpatterns = [path("admin/", admin.site.urls), path("", include("projects.urls"))]
admin.site.site_header = "Project Select"
admin.site.site_title = "Project Select admin"
admin.site.index_title = "Manage your collection"

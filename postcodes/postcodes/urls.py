from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from query import views
from query.views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'postcodes.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', IndexView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    (r'^index.html', TemplateView.as_view(template_name="index.html")),
    url(r'^getdistances/$', views.get_distances, name='getdistances'),
    url(r'^populate/$', views.populate_postcodes, name='populatepostcodes'),
)

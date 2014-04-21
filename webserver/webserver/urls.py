from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'webserver.views.home', name="home"),


  # AJAX URLs
  url(r'^searchForRasPis$', 'webserver.views.searchForRasPis', name="searchForRasPis"),



    # Examples:
    # url(r'^$', 'webserver.views.home', name='home'),
    # url(r'^webserver/', include('webserver.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

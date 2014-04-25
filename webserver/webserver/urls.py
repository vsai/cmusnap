from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'webserver.views.home', name="home"),

  # AJAX URLs
  url(r'^searchForRasPis$', 'webserver.views.searchForRasPis', name="searchForRasPis"),
  url(r'^send-config$', 'webserver.views.config_handler', name="configureRasPis"),
)

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'note_app.views.index'), # root
    url(r'^login$', 'note_app.views.login_view'), # login
    url(r'^logout$', 'note_app.views.logout_view'), # logout
    url(r'^notes$', 'note_app.views.public'), # public notes
    url(r'^submit$', 'note_app.views.submit'), # submit new note
    url(r'^users/$', 'note_app.views.users'),
    url(r'^users/(?P<username>\w{0,30})/$', 'note_app.views.users'),
    url(r'^follow$', 'note_app.views.follow'),
    url(r'^note/(?P<heading>.{0,140})/$', 'note_app.views.note'),
    url(r'^note$','note_app.views.note'),
    url(r'^signup$', 'note_app.views.signup'),
    url(r'^recommendation$', 'note_app.views.recommendation')
)
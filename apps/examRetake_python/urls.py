from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="go_startpage"),
    url(r'^login', views.login, name="go_login"),
    url(r'^register', views.register, name="go_register"),
    url (r'^process/login$', views.processLogin, name='processLogin'),
    url (r'^process/registration$', views.processRegistration, name='processRegistration'),
    url (r'^dashboard$', views.dashboard, name='go_dashboard'),
    url (r'^logout$', views.processLogout, name='processLogout'),
    url (r'^new$', views.processQuote, name='processNewQuote'),
    url (r'^deleteQuote/(?P<id>\d+)$', views.deleteQuote, name='processDeleteQuote'),
    url (r'^showUser/(?P<id>\d+)$', views.showUser, name='showUser'),
    url (r'^editUser/(?P<id>\d+)$', views.editUser, name='editUser'),
    url (r'^process/update/(?P<id>\d+)$', views.processUpdate, name='updateUser'),
    url (r'^add/like/(?P<id>\d+)$', views.addLike, name='addLike'),
]
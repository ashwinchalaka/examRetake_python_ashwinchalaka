from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.go_index, name="go_startpage"),
    url(r'^login', views.go_login, name="go_login"),
    url(r'^register', views.go_register, name="go_register"),
    url (r'^process/login$', views.processLogin, name='processLogin'),
    url (r'^process/registration$', views.processRegistration, name='processRegistration'),
    url (r'^dashboard$', views.go_dashboard, name='go_dashboard'),
    url (r'^logout$', views.processLogout, name='processLogout'),
    url (r'^addTrip$', views.go_addTrip, name='go_addTrip'),
    url (r'^tripDetails/(?P<id>\d+)$', views.go_tripDetails, name='go_tripDetails'),
    url (r'^process/newTrip$', views.processNewTrip, name='processNewTrip'),
    url (r'^process/deleteTrip/(?P<id>\d+)$', views.processDeleteTrip, name='processDeleteTrip'),
    url (r'^process/cancelTrip/(?P<id>\d+)$', views.processCancelTrip, name='processCancelTrip'),
    url (r'^process/joinTrip/(?P<id>\d+)$', views.processJoinTrip, name='processJoinTrip'),
    url (r'^editUser/(?P<id>\d+)$', views.go_editUser, name='go_editUser'),
    url (r'^process/userUpdate/(?P<id>\d+)$', views.processUserUpdate, name='processUserUpdate'),
    url (r'^editTrip/(?P<id>\d+)$', views.go_editTrip, name='go_editTrip'),
    url (r'^process/tripUpdate/(?P<id>\d+)$', views.processTripUpdate, name='processTripUpdate'),
]
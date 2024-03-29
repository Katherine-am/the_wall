from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loginHomepage, name="loginHomepage"),
    url(r'^registration$', views.registration, name="registrationCheck"),
    url(r'^login$', views.login, name="loginCheck"),
    url(r'^success$', views.successfulLogin, name="successfulLogin"),
    url(r'^wall_homepage$', views.wallHomepage, name="wallHomepage"),
    url(r'^post_message$', views.postMessage, name="postMessage"),
    url(r'^post_comment$', views.postComment, name="postComment"),
    url(r'^logout$', views.logout, name="logout")
]
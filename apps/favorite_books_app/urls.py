from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^log_out$', views.log_out),
    url(r'^books/add_book$', views.add_book),
    url(r'^delete_book/(?P<book_id>\d+)$', views.delete_book),
    url(r'^books/(?P<book_id>\d+)$', views.edit_page),
    url(r'^books/book_edit/(?P<book_id>\d+)$', views.book_edit),
    url(r'^books/book_info/(?P<book_id>\d+)$', views.info_page),
    url(r'^unfavorite/(?P<book_id>\d+)$', views.unfavorite),
    url(r'^add_to_favorite/(?P<book_id>\d+)$', views.addfavorite),
]
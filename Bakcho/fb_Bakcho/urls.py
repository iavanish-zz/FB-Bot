from django.conf.urls import include, url
from .views import BakchoView
urlpatterns = [url(r'^52ad82257c93e100b20ad8498af0fc5f5bdc5a51bdc92913a3/?$', BakchoView.as_view())]

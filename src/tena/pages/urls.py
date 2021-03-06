from django.urls import re_path, reverse_lazy
from django.views.generic import RedirectView

from pages import views

urlpatterns = [
    re_path(r"^home/", views.HomePage.as_view(), name="home"),
    re_path(
        r"^msg/(?P<msg>.+)/$", views.SendMessageView.as_view(), name="send-message"
    ),
    re_path(r"", RedirectView.as_view(url=reverse_lazy("home"))),
]

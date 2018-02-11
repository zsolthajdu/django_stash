
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from .models import Bookmark

from .views import CreateView, DetailsView

urlpatterns = {
    url(r'^bookmarks/$', CreateView.as_view(), name="create"),
    url(r'^bookmarks/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name="details"),

    #url(r'^users/$', UserView.as_view(), name="users"),
    #url(r'users/(?P<pk>[0-9]+)/$',
    #            UserDetailsView.as_view(), name="user_details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)


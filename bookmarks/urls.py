
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .models import Bookmark

from .views import CreateView, DetailsView, SearchView, TagSearchView

urlpatterns = {
    path('bookmarks/', CreateView.as_view(), name="create"),
    path('bookmark/<int:pk>/', DetailsView.as_view(), name="details"),
    path('bookmarks/search/<str:term>/', SearchView.as_view(), name="bookmark-search"),
    path('bookmarks/tags/<str:term>/', TagSearchView.as_view(), name="bookmark-tags"),
    path('api-auth/', include('rest_framework.urls')),
}

urlpatterns = format_suffix_patterns(urlpatterns)


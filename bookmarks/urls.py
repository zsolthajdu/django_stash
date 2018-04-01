
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .models import Bookmark

from .views import CreateView, DetailsView

urlpatterns = {
    path('bookmarks/', CreateView.as_view(), name="create"),
    path('bookmark/<int:pk>/', DetailsView.as_view(), name="details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)


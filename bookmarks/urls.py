
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .models import Bookmark

from .views import CreateView, DetailsView, SearchView, TagSearchView, DateSearchView

urlpatterns = {
	path('', CreateView.as_view(), name="create"),
	path('<int:pk>', DetailsView.as_view(), name="details"),
	path('search/<str:term>/', SearchView.as_view(), name="bookmark-search"),
	path('tags/<str:term>/', TagSearchView.as_view(), name="bookmark-tags"),
	path('date/<int:year>', DateSearchView.as_view(), name='bookamrk-date'),
	path('date/<int:year>/<int:month>', DateSearchView.as_view(), name='bookamrk-date'),
	path('date/<int:year>/<int:month>/<int:day>', DateSearchView.as_view(), name='bookamrk-date'),
	path('api-auth/', include('rest_framework.urls')),
}

urlpatterns = format_suffix_patterns(urlpatterns)

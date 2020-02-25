
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .models import Bookmark

from .views import CreateView, DetailsView, SearchView, TagSearchView, TagListView, DateSearchView

urlpatterns = {
	path('', CreateView.as_view(), name="create"),
	path('<int:pk>', DetailsView.as_view(), name="details"),
	path('search/<str:term>/', SearchView.as_view(), name="bookmark-search"),
	path('tags/', TagListView.as_view(), name="tag-list"),
	path('tags/<str:term>/', TagSearchView.as_view(), name="bookmark-tags"),
	path('date/<int:year>', DateSearchView.as_view(), name='find-year'),
	path('date/<int:year>/<int:month>', DateSearchView.as_view(), name='find-year_month'),
	path('date/<int:year>/<int:month>/<int:day>', DateSearchView.as_view(), name='find-year_month_day'),
	path('api-auth/', include('rest_framework.urls')),
}

urlpatterns = format_suffix_patterns(urlpatterns)

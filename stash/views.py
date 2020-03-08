from django.shortcuts import render

from rest_framework import generics
from rest_framework import permissions
from rest_framework import pagination
from rest_framework.utils.urls import remove_query_param, replace_query_param
from .serializers import BookmarkSerializer, TagSerializer
from .permissions import IsOwnerOrReadOnly
from .models import Bookmark, Tag

def bm_main(request):
	return render( request, 'bm.html')

def bm_file(request, filename):
	return render( request, filename )

# Custom pagination class to
class BMPagination( pagination.PageNumberPagination ):
	"""
	Custom pagination class to
	 - override default page_size.
	 - to provide relative links to previous and next pages in return. The default 
	   pagination provides absolute urls,
		including the same transfer protocol that the request used (ie http stays http). 
		This can cause problems if on the server
	   side a proxy forwards https requests as http to Django. The paginator will 
		generate absolut URLs using http. But some browsers
	   may refuse to follow them when they hotice that they are insecure http as opposed to https, that was used originallly.
	"""
	page_size = 50
	page_size_query_param = 'page_size'
	max_page_size = 1000

	# Create relative path for next page
	def get_next_link(self):
		if not self.page.has_next():
			return None
		url = self.request.get_full_path() # build_absolute_uri()
		page_number = self.page.next_page_number()
		return replace_query_param(url, self.page_query_param, page_number)

	def get_previous_link(self):
		if not self.page.has_previous():
			return None
		url = self.request.get_full_path()  #  build_absolute_uri()
		page_number = self.page.previous_page_number()
		if page_number == 1:
			return remove_query_param(url, self.page_query_param)
		return replace_query_param(url, self.page_query_param, page_number)

class CreateView(generics.ListCreateAPIView):
	"""This class defines the create behavior of our rest api."""
	serializer_class = BookmarkSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly , )
	pagination_class = BMPagination

	def get_queryset( self):
		# Grab logged in user's bookmarks, ordered by creation date
		if self.request.user.is_anonymous:
			# Or, if user is not logged in, all public bookmarks
			qs = Bookmark.objects.all().filter(public = True).order_by('-created')
		else:
			qs = Bookmark.objects.all().filter(owner = self.request.user).order_by('-created')
		req_url = self.request.query_params.get( "url", None )
		if req_url is not None:
			# Can also look if a bookmark already exists, using the url from query
			qs2 = qs.filter( url = req_url )
			return qs2
		return qs

class SearchView(generics.ListCreateAPIView):
	""" Search bookmarks for a keyword using complex queries. """
	serializer_class = BookmarkSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly , )
	pagination_class = BMPagination

	def get_queryset( self ):
		# Grab logged in user's bookmarks, ordered by creation date
		if self.request.user.is_anonymous:
			# Or, if user is not logged in, all public bookmarks
			qs = Bookmark.objects.filter(public = True).order_by('-created')
		else:
			qs = Bookmark.objects.filter(owner = self.request.user).order_by('-created')

		qsTitle = qs.filter( title__icontains=self.kwargs['term'] )

		if qsTitle.count() > 0:
			return qsTitle
		else:
			return  qs.filter( description__icontains=self.kwargs['term'] )


class DateSearchView(generics.ListCreateAPIView):
	""" Search bookmarks based on creation date: year, month and or day  """
	serializer_class = BookmarkSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly , )
	pagination_class = BMPagination

	def get_queryset( self ):
		# Grab logged in user's bookmarks, ordered by creation date
		if self.request.user.is_anonymous:
			# Or, if user is not logged in, all public bookmarks
			qs = Bookmark.objects.all().filter(public = True).order_by('-created')
		else:
			qs = Bookmark.objects.all().filter(owner = self.request.user).order_by('-created')

		if 'day' in self.kwargs:
			return qs.filter( created__year = self.kwargs['year'],
				  created__month = self.kwargs['month'], created__day = self.kwargs['day'] )
		elif 'month' in self.kwargs:
			return qs.filter( created__year = self.kwargs['year'], created__month = self.kwargs['month'] )
		elif 'year' in self.kwargs:
			return qs.filter( created__year = self.kwargs['year'] )
		else:
			return Bookmark.objects.none()

class TagSearchView(generics.ListCreateAPIView):
	""" Search for bookmarks that are tagged with a specific word.
	    Supports only one query tag at the moment.
	"""
	serializer_class = BookmarkSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly , )
	pagination_class = BMPagination

	def get_queryset( self ):
		# Grab logged in user's bookmarks, ordered by creation date
		if self.request.user.is_anonymous:
			# Or, if user is not logged in, all public bookmarks
			qs = Bookmark.objects.all().filter(public = True).order_by('-created')
		else:
			qs = Bookmark.objects.all().filter(owner = self.request.user).order_by('-created')
		return qs.filter( tags__name = self.kwargs['term'] )


class TagListView(generics.ListCreateAPIView):
#	Return a list of all tags, associated with bookmarks of current user
	serializer_class = TagSerializer
	permission_classes =  (permissions.IsAuthenticatedOrReadOnly , IsOwnerOrReadOnly)
	pagination_class = BMPagination

	def get_queryset( self ):
		if self.request.user.is_anonymous:
			return Tag.objects.usage_for_model( Bookmark, filters=dict( public = True ) )
		else:
			# Examples : https://docs.djangoproject.com/en/3.0/topics/db/queries/#lookups-that-span-relationships
			return Tag.objects.filter( bookmark__owner__username = self.request.user.username )

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
	"""This class handles the http GET, PUT and DELETE requests."""
	serializer_class = BookmarkSerializer
	permission_classes =  (permissions.IsAuthenticatedOrReadOnly , IsOwnerOrReadOnly)
	pagination_class = pagination.PageNumberPagination

	def get_queryset( self ):
		return Bookmark.objects.all().filter(owner = self.request.user)

	def delete(self, request, *args, **kwargs):
		bm = self.get_object()

		# TODO Save list of this bookmark's tags in TAGS
		result = self.destroy(request, *args, **kwargs)

		# TODO If tags in TAGS are not used any more, delete them

		return result

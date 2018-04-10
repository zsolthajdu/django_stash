from django.shortcuts import render

from rest_framework import generics
from rest_framework import permissions
from rest_framework import pagination
from rest_framework.utils.urls import remove_query_param, replace_query_param
from django_filters.rest_framework import DjangoFilterBackend
from tagging.models import Tag, TaggedItem
from .serializers import BookmarkSerializer
from .permissions import IsOwnerOrReadOnly
from .models import Bookmark

def bm_main(request):
    return render( request, 'bm.html')

def bm_file(request, filename):
    return render( request, filename )

# Custom pagination class to
class BMPagination( pagination.PageNumberPagination ):
    """
    Custom pagination class to 
     - override default page_size.
     - to provide relative links to previous and next pages in return. The default pagination provides absolute urls, 
       including the same transfer protocol that the request used (ie http stays http). This can cause problems if on the server
       side a proxy forwards https requests as http to Django. The paginator will generate absolut URLs using http. But some browsers
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
    #queryset = Bookmark.objects.all()
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
        tags = self.request.query_params.get( "tags", None )
        req_url = self.request.query_params.get( "url", None )
        # Also filter on tag(s), value can be one or more - comma separated - tag
        if tags is not None:
            qs = TaggedItem.objects.get_by_model( qs, tags )
        elif req_url is not None:
            # Can also look if a bookmark already exists, using the url from query
            qs = qs.filter( url = req_url )
        return qs

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    #queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes =  (permissions.IsAuthenticatedOrReadOnly , IsOwnerOrReadOnly)
    pagination_class = pagination.PageNumberPagination

    def get_queryset( self ):
        return Bookmark.objects.all().filter(owner = self.request.user)

    def delete(self, request, *args, **kwargs):
        bm = self.get_object()
        # Remove tag associations first
        Tag.objects.update_tags( bm, None)
        # 
        return self.destroy(request, *args, **kwargs)

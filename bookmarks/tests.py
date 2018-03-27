from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from .models import Bookmark

class ModelTestCase(TestCase):
    """This class defines the test suite for the bookmark model."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="anonymous")
        self.bookmark_title = "New York Times"
        self.bookmark_description = "A longer description comes here."
        self.bookmark_url = "http://nytimes.com"
        self.bookmark = Bookmark(title=self.bookmark_title, description=self.bookmark_description,
            url=self.bookmark_url, owner=user )

    def test_model_can_create_a_bookmark(self):
        """Test the bookmark model can create a bookmark."""
        old_count = Bookmark.objects.count()
        self.bookmark.save()
        new_count = Bookmark.objects.count()
        self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="anonymous")
        
        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        # Bare minimum
        self.bookmark_data = { 'url':'http://cbsnews.com', 'owner': user.id }
        self.response = self.client.post( reverse('create'), self.bookmark_data, format="json")
        # With description and tags
        self.bookmark_data = { 'url':'https://cnn.com', 
                        'description':'Global news network', 'owner': user.id, 'tags': ['tv,news']}
        self.response = self.client.post( reverse('create'), self.bookmark_data, format="json")
        # with title and public
        self.bookmark_data = { 'url':'http://abcnews.com', 'title':'ABC news division', 'public' : 'True',
                        'description':'Global news network', 'owner': user.id, 'tags': ['tv,news']}
        self.response = self.client.post( reverse('create'), self.bookmark_data, format="json")

    def test_api_can_create_a_bookmark(self):
        """Test the api has bookmark creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        
    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.get( reverse('create'), kwargs={'pk': 1}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_api_can_get_a_bookmark(self):
        """Test the api can get a given bookmark."""
        bookmark = Bookmark.objects.get( id=1 )
        response = self.client.get(
            reverse('details', kwargs={'pk': bookmark.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bookmark)

    def test_api_can_find_existing_bookmark(self):
        """Test the api can find existing bookmark based on URL."""
        bookmark = Bookmark.objects.get( id=1 )
        response = self.client.get( reverse('create') + "?url=https://cnn.com", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bookmark)

    def test_api_can_update_bookmark(self):
        """Test the api can update a given bookmark."""
        bookmark = Bookmark.objects.get( id=2 )
        changed_bookmark = { 'title': 'CNN.com', 'url':'https://cnn.com', 'description':'Quality news network', 'tags': ['tv,news,cnn,tag4'] }
        res = self.client.put( reverse('details', kwargs={'pk': bookmark.id}), changed_bookmark, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        bm1 = Bookmark.objects.get( id=1 )
        print( bm1.tags )

    def test_api_can_delete_bookmark(self):
        """Test the api can delete a bookmark."""
        
        response = self.client.delete(
            reverse('details', kwargs={'pk': 1}),format='json', follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)    
        
        
            

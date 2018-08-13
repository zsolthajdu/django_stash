from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from .models import Bookmark
import json


class ModelTestCase(TestCase):
    """This class defines the test suite for the bookmark model."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="anonymous")
        self.bookmark_title = "New York Times"
        self.bookmark_description = "A longer description comes here."
        self.bookmark_url = "http://nytimes.com"
        self.bookmark = Bookmark(title=self.bookmark_title, description=self.bookmark_description,
            url=self.bookmark_url, owner=user, public=True )

    def test_model_can_create_a_bookmark(self):
        """Test the bookmark model can create a bookmark."""
        old_count = Bookmark.objects.count()
        self.bookmark.save()
        new_count = Bookmark.objects.count()
        self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test clients and other test variables."""
        self.alice = User.objects.create(username="Alice")
        bob = User.objects.create(username="Bob")

        # Initialize clientss and force it to use authentication
        self.clientA = APIClient()
        self.clientA.force_authenticate(user=self.alice)
        self.clientB = APIClient()
        self.clientB.force_authenticate(user=bob)

        # Bare minimum
        self.bookmark_data = { 'url':'http://cbsnews.com', 'owner': self.alice.id, 'public':'false' }
        self.response = self.clientA.post( reverse('create'), self.bookmark_data, format="json")
        # With description and tags
        self.bookmark_data = { 'url':'https://cnn.com', 
                        'description':'Global news network', 'owner': self.alice.id, 'tags': ['tv,news'], 'public':'true'}
        self.response = self.clientA.post( reverse('create'), self.bookmark_data, format="json")
        # with title and public
        self.bookmark_data = { 'url':'http://linux.com', 'title':'Linux News',
                        'description':'Linux Foundation website', 'owner': self.alice.id, 'tags': ['tv,news'], 'public':'true' }
        self.response = self.clientB.post( reverse('create'), self.bookmark_data, format="json")

    def test_api_can_create_a_bookmark(self):
        """Test the api has bookmark creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        
    def test_create_authorization_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        self.bookmark_data = { 'url':'http://opensource.com', 'title':'Open source software News', 'public' : 'true',
                        'description':'Open source information', 'tags': ['software,news'] }
        res = new_client.post( reverse('create'), self.bookmark_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_nonauthorized_user_only_gets_public(self):
        """Test that if user is not logged in, only gets public bookmarks"""
        new_client = APIClient()
        res = new_client.get( reverse('create'), format="json" )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual( res.data['count'], 2 )
        
    def test_api_can_get_a_bookmark(self):
        """Test the api can get a given bookmark."""
        bookmark = Bookmark.objects.get( id=1 )
        response = self.clientA.get(
            reverse('details', kwargs={'pk': bookmark.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bookmark)

    def test_api_can_find_existing_bookmark(self):
        """Test the api can find existing bookmark based on URL."""
        bookmark = Bookmark.objects.get( id=1 )
        response = self.clientA.get( reverse('create') + "?url=https://cnn.com", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bookmark)

    def test_api_can_update_bookmark(self):
        """Test the api can update user's own bookmark."""
        bookmark = Bookmark.objects.get( id=2 )
        changed_bookmark = { 'title': 'CNN.com', 'url':'https://cnn.com', 'description':'Quality news network', 'tags': ['tv,news,cnn,tag4'] }
        res = self.clientB.put( reverse('details', kwargs={'pk': bookmark.id}), changed_bookmark, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        bm1 = Bookmark.objects.get( id=2 )
        print( bm1.tags )

    def test_api_cannot_update_another_users_bookmark(self):
        """Test the api can't update someone else's bookmark."""
        bookmark = Bookmark.objects.get( id=2 )
        changed_bookmark = { 'title': 'cbs.com', 'url':'https://cnn.com', 'description':'Quality news network', 'tags': ['tv,news,cnn,tag4,tag5'] }
        res = self.clientA.put( reverse('details', kwargs={'pk': bookmark.id}), changed_bookmark, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_can_delete_bookmark(self):
        """Test the api can delete a bookmark."""
        response = self.clientA.delete(
            reverse('details', kwargs={'pk': 1}),format='json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_nonauthorized_cannot_delete_private_bookmark(self):
        """Test that unauthorized users cannot delete a private bookmark."""
        new_client = APIClient()
        response = new_client.delete( reverse('details', kwargs={'pk': 1}), format='json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_nonauthorized_cannot_delete_public_bookmark(self):
        """Test that unauthorized users cannot delete a public bookmark."""
        new_client = APIClient()
        response = new_client.delete( reverse('details', kwargs={'pk': 2}), format='json', follow=True)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_using_emoji_in_bookmark_info(self):
        """Test using emoji in bookmark title"""
        emoji_title = "Tutorial: Build a Basic CRUD App with Node.js - DEV Community 👩‍💻👨‍💻"
        emoji_url = "https://dev.to/oktadev/tutorial-build-a-basic-crud-app-with-nodejs-1ohn"
        self.bookmark_data = { 'url':emoji_url, 'owner': self.alice.id,
            'description':'Learn how to securely store, update, and display user data in a simple Node.js / Express.js app.',
            'tags': ['software development, inclusive, community,engineering,javascript, webdev, beginners, node'],
            'title' : emoji_title, 'public':'false' }
        response = self.clientA.post( reverse('create'), self.bookmark_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Find bookmark that was just created
        response = self.clientA.get( reverse('create') + "?url="+emoji_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jsonResponse = json.loads( response.content.decode('UTF-8') )
        self.assertEqual( jsonResponse['results'][0]['title'], emoji_title )
        print( jsonResponse['results'][0]['title'] )

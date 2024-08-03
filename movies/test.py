import threading
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Collection, Movie
import uuid
from django.core.cache import cache
from .factories import UserFactory, CollectionFactory, MovieFactory
import logging
logger = logging.getLogger(__name__)


class UserRegistrationTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

    def test_user_registration(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        user_exists = User.objects.filter(username=self.user_data['username']).exists()
        self.assertTrue(user_exists)
        print("User registration testing completed")

class MoviesAPITest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.url = reverse('movies')

    def test_movies_list(self):
        # Creating some movie instances using Factory Boy
        for _ in range(10):
            MovieFactory()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('count', data)
        self.assertIn('next', data)
        self.assertIn('previous', data)
        self.assertIn('results', data)

        self.assertIsInstance(data['results'], list)
        for movie in data['results']:
            self.assertIn('title', movie)
            self.assertIn('description', movie)
            self.assertIn('genres', movie)
            self.assertIn('uuid', movie)

        print("Get movies list testing completed")

class CollectionTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.collection = CollectionFactory(user=self.user)
        self.movie = MovieFactory()
        self.collection.movies.add(self.movie)

    def test_create_collection(self):
        url = reverse('collection')
        data = {
            "title": "New Collection",
            "description": "New Description",
            "movies": [
                {
                    "title": "New Movie",
                    "description": "New Description",
                    "genres": "Drama",
                    "uuid": str(uuid.uuid4())
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('collection_uuid', response.data)
        print("Create movies list testing completed")

    def test_get_collection(self):
        url = reverse('collection', kwargs={'collection_uuid': self.collection.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.collection.title)
        self.assertEqual(response.data['description'], self.collection.description)
        self.assertEqual(len(response.data['movies']), 1)
        print("Get movies list testing completed")

    def test_update_collection(self):
        url = reverse('collection', kwargs={'collection_uuid': self.collection.uuid})
        data = {
            "title": "Updated Collection",
            "description": "Updated Description",
            "movies": [
                {
                    "title": "Updated Movie",
                    "description": "Updated Description",
                    "genres": "Thriller",
                    "uuid": str(uuid.uuid4())
                }
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.title, "Updated Collection")
        self.assertEqual(self.collection.description, "Updated Description")
        print("Updating movies list testing completed")

    def test_delete_collection(self):
        url = reverse('collection', kwargs={'collection_uuid': self.collection.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Collection.objects.filter(uuid=self.collection.uuid).exists())
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Deleting movies list testing completed")

    def test_get_all_collections(self):
        url = reverse('collection')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['collections']), 0)
        print("Get all movies list testing completed")


class RequestCountTest(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.get_request_count_url = reverse('request-count')
        self.reset_request_count_url = reverse('request-count-reset')

    def test_request_count(self):
        cache.set('request_count', 0)

        for _ in range(5):
            self.client.get(self.get_request_count_url)
        
        response = self.client.get(self.get_request_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['request_count'], 6) #asserting 6 because one more req will be set for getting the count
        print("Get request count testing completed")

    def test_reset_request_count(self):        
        cache.set('request_count', 0)

        for _ in range(5):
            self.client.get(self.get_request_count_url)

        # Reset the request count
        response = self.client.post(self.reset_request_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'request count reset successfully')

        response = self.client.get(self.get_request_count_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['request_count'], 1) #asserting 1 because one more req will be set for getting the count
        print("Resetting request count testing completed")

# Using threading to test request count for concurrent requests
class ParallelRequestTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.request_count_url = '/request-count/'
        self.reset_count_url = '/request-count/reset/'

        # Reset the request count before running tests
        self.client.post(self.reset_count_url)

    def make_request(self):
        self.client.get(self.request_count_url)

    def test_parallel_requests(self):
        num_threads = 10

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self.make_request)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        response = self.client.get(self.request_count_url)
        self.assertEqual(response.data['request_count'], num_threads+1) #asserting +1 because one more req will be set for getting the count
        print("Get request count for concurrent requests testing completed")
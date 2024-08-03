from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .serializers import MovieSerializer, CollectionSerializer, UserCollectionsSerializer
from django.conf import settings
from .models import Movie, Collection
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import logging
logger = logging.getLogger(__name__)

class GetMovies(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    def get(self, request):
        session = self.create_session()
        api_url = 'https://demo.credy.in/api/v1/maya/movies/'

        try:
            response = session.get(api_url, auth=(settings.API_USERNAME, settings.API_PASSWORD), verify=False)
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return [], None

        print("Movie list response received from external API")
        return Response(response.json())

    # creating retry mechanism for trying multiple times for external api
    def create_session(self):
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('https://', adapter)
        return session

class CollectionViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, collection_uuid=None):
        data = request.data
        movies_data = data.pop('movies', [])
        
        serializer = CollectionSerializer(data=data)
        if serializer.is_valid():
            collection = serializer.save(user=self.request.user)
            
            for movie_data in movies_data:
                movie_serializer = MovieSerializer(data=movie_data)
                if movie_serializer.is_valid():
                    # movie = movie_serializer.save()
                    movie, created = Movie.objects.update_or_create(uuid=movie_data['uuid'], defaults=movie_data)
                    collection.movies.add(movie)
                else:
                    collection.delete()
                    print('Collection does not created.')
                    return Response(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            collection.save()
            print("Collection created by user - {0} & collection uuid - {1}".format(str(self.request.user), collection.uuid))
            return Response({"collection_uuid":collection.uuid}, status=status.HTTP_201_CREATED)
        else:
            print("Invalid data came in for request payload {}".format(data))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, collection_uuid=None): #updateCollection(self, request, collection_uuid=None)
        if not collection_uuid:
            print("Collection uuid missing for put request")
            return Response({"messgage":"collection uui missing"}, status=status.HTTP_400_BAD_REQUEST)
        collection = get_object_or_404(Collection, uuid=collection_uuid, user=self.request.user)
        data = request.data

        # Update the collection's title and description if provided
        collection.title = data.get('title', collection.title)
        collection.description = data.get('description', collection.description)
        
        movies_data = data.get('movies', [])
        if movies_data:
            # Clear the current movies and add the new list of movies
            collection.movies.clear()
            for movie_data in movies_data:
                movie_serializer = MovieSerializer(data=movie_data)
                if movie_serializer.is_valid():
                    movie, created = Movie.objects.update_or_create(uuid=movie_data['uuid'], defaults=movie_data)
                    collection.movies.add(movie)
                else:
                    print(f"Movie serializer errors: {movie_serializer.errors}")
                    return Response(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        collection.save()
        serializer = CollectionSerializer(collection)
        print("Collection updated for collection uuid - {0}".format(collection.uuid))
        return Response({"message":"Collection updated successfully"}, status=status.HTTP_200_OK)

    def get(self, request, collection_uuid=None):
        collections = Collection.objects.filter(user=self.request.user)
        if collection_uuid:
            try:
                collections = collections.get(uuid=collection_uuid)
            except Collection.DoesNotExist as e:
                print('Collection does not exists for uuid - {0} and error - {1}'.format(collection_uuid, str(e)))
                return Response({"message":"Collection does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CollectionSerializer(collections)
            print("Collection get request for collection uuid - {0}".format(collection_uuid))
            return Response(serializer.data)
        
        serializer = UserCollectionsSerializer({'collections': collections}, context={'request': request})
        print("Collection get request for all collections for user - {0}".format(str(self.request.user)))
        return Response(serializer.data)

    def delete(self, request, collection_uuid=None):
        if not collection_uuid:
            print("Collection uuid missing for put request")
            return Response({"messgage":"collection uui missing"}, status=status.HTTP_404_NOT_FOUND)

        # We can also use get_object_or_404
        try:
            collection = Collection.objects.get(uuid=collection_uuid)
            collection.delete()
            print("Collection delete request for collection uuid - {0}".format(collection_uuid))
            return Response({"message":"Collection deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print('Collection does not exists for uuid - {0} and error - {1}'.format(collection_uuid, str(e)))
            return Response({"message":"Collection does not exists"}, status=status.HTTP_404_NOT_FOUND)
from rest_framework import serializers
from .models import Movie, Collection
from collections import Counter

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

    def to_representation(self, instance):
        """
        Convert the instance to a dictionary representation.
        """
        representation = super().to_representation(instance)
        # Customize the response format
        return {
            'title': representation['title'],
            'description': representation['description'],
            'movies': representation['movies']
        }

# class ResponseCollectionSerializer(serializers.ModelSerializer):
#     movies = MovieSerializer(many=True, read_only=True)

#     class Meta:
#         model = Collection
#         fields = ['title', 'description', 'movies']
#         extra_kwargs = {'user': {'read_only': True}}

class UserCollectionsSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    collections = CollectionSerializer(many=True)
    favourite_genres = serializers.SerializerMethodField()

    def get_favourite_genres(self, obj):
        user = self.context['request'].user
        collections = Collection.objects.filter(user=user)
        genre_counter = Counter()

        for collection in collections:
            for movie in collection.movies.all():
                genres = movie.genres.split(', ')
                genre_counter.update(genres)

        top_genres = [genre for genre, _ in genre_counter.most_common(3)]
        return ', '.join(top_genres)
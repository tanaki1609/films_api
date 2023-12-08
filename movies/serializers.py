from rest_framework import serializers
from .models import Movie, Director, Genre
from rest_framework.exceptions import ValidationError


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id year name age'.split()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    # genres = GenreSerializer(many=True)
    genre_list_copy = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        # fields = 'title rating'.split()  # ['title', 'rating']
        fields = 'id director title rating genre_list genre_list_copy reviews'.split()
        depth = 1

    def get_genre_list_copy(self, movie):
        return [genre.name for genre in movie.genres.all()]


class MovieValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100, min_length=3)
    text = serializers.CharField(required=False)
    rating = serializers.FloatField(min_value=0, max_value=10)
    year = serializers.IntegerField(min_value=1800)
    director_id = serializers.IntegerField(min_value=1)
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_genres(self, genres):  # [1,2,3]
        genres_from_db = Genre.objects.filter(id__in=genres)  # [1,2]
        if len(genres) != len(genres_from_db):
            raise ValidationError('Genre does not exist!')
        return genres

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exists!')
        return director_id

    def validate_name(self, name):
        # validation
        return name

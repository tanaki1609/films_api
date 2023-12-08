from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Director, Genre
from .serializers import MovieSerializer, MovieValidateSerializer, DirectorSerializer, GenreSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class GenreAPIViewSet(ModelViewSet):  # GET, POST, GET, PUT, DELETE
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class DirectorListAPIView(ListCreateAPIView):  # GET, POST
    queryset = Director.objects.all()  # queryset -> list of objects from DB
    serializer_class = DirectorSerializer  # serializer inherited by ModelSerializer
    pagination_class = PageNumberPagination


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):  # GET, PUT, DELETE
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'


class MovieListAPIView(ListCreateAPIView):
    queryset = Movie.objects.select_related('director') \
            .prefetch_related('genres', 'reviews').all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # 1 step. Get data from request(body)
        title = request.data.get('name')
        text = request.data.get('text')
        rating = request.data.get('rating')
        year = request.data.get('year')
        director_id = request.data.get('director_id')
        genres = request.data.get('genres')

        # 2 step. Create Film by client data
        movie = Movie.objects.create(
            title=title, text=text, rating=rating, year=year,
            director_id=director_id
        )
        movie.genres.set(genres)
        movie.save()

        # 3 step. Return to client created data
        return Response(data={'movie_id': movie.id},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # 1 step. Collect data from DB
        movie_list = Movie.objects.select_related('director') \
            .prefetch_related('genres', 'reviews').all()

        # 2 step. Reformat data from db to DICT(LIST)
        data = MovieSerializer(instance=movie_list, many=True).data

        # 3 step. Return as JSON
        return Response(data=data)
    elif request.method == 'POST':
        # 0 step. Validation of data
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # 1 step. Get data from request(body)
        title = request.data.get('name')
        text = request.data.get('text')
        rating = request.data.get('rating')
        year = request.data.get('year')
        director_id = request.data.get('director_id')
        genres = request.data.get('genres')

        # 2 step. Create Film by client data
        movie = Movie.objects.create(
            title=title, text=text, rating=rating, year=year,
            director_id=director_id
        )
        movie.genres.set(genres)
        movie.save()

        # 3 step. Return to client created data
        return Response(data={'movie_id': movie.id},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    # 1 step. Collect data from DB
    try:
        movie_detail = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'message': 'Movie not found!'})
    if request.method == 'GET':
        # 2 step. Reformat data from db to DICT
        data = MovieSerializer(instance=movie_detail, many=False).data

        # 3 step. Return as JSON
        return Response(data=data)
    if request.method == 'PUT':
        serializer = MovieValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie_detail.title = request.data.get('name')
        movie_detail.text = request.data.get('text')
        movie_detail.rating = request.data.get('rating')
        movie_detail.year = request.data.get('year')
        movie_detail.director_id = request.data.get('director_id')
        movie_detail.genres.set(request.data.get('genres'))
        movie_detail.save()
        return Response(data={'movie_id': movie_detail.id},
                        status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        movie_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def test_api_view(request):
    dict_ = {
        'text': 'Hello world',
        'integer': 1000,
        'bool': True,
        'list': [1, 2, 3],
        'dict': {'key': 'value'}
    }
    return Response(data=dict_)

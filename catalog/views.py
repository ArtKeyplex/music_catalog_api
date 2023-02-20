from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Album, Artist, Song, SongAlbum
from .serializers import (AlbumSerializer, ArtistSerializer,
                          SongAlbumSerializer, SongSerializer)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongAlbumViewSet(viewsets.ModelViewSet):
    queryset = SongAlbum.objects.all()
    serializer_class = SongAlbumSerializer

    @action(detail=True, methods=['get'])
    def song_by_albums(self, request, pk=None):
        """Позволяет получить все песни в определенном альбоме"""
        album = self.get_object()
        song_albums = SongAlbum.objects.filter(album=album.album)
        songs = [song_album.song.title for song_album in song_albums]
        return Response({'songs': songs})


schema_view = get_schema_view(
    openapi.Info(
        title="Music Catalog API",
        description="API for managing music artists, albums, and songs",
        default_version="1.0.0",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'artists', views.ArtistViewSet)
router.register(r'albums', views.AlbumViewSet)
router.register(r'songs', views.SongViewSet)
router.register(r'song_albums', views.SongAlbumViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

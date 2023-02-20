from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Album, Artist, Song, SongAlbum


class ArtistSerializer(serializers.ModelSerializer):
    """Сериализатор для исполнителей"""
    class Meta:
        model = Artist
        fields = ['id', 'name']


class AlbumSerializer(serializers.ModelSerializer):
    """Сериализатор для альбомов"""
    artist = serializers.CharField(source='artist.name')

    class Meta:
        model = Album
        fields = ['id', 'title', 'year', 'artist']

    def create(self, validated_data):
        artist_name = validated_data.pop('artist')['name']
        try:
            artist = Artist.objects.get(name=artist_name)
        except Artist.DoesNotExist:
            raise serializers.ValidationError(
                f'Artist with name "{artist_name}" does not exist.')
        return Album.objects.create(artist=artist, **validated_data)


class SongSerializer(serializers.ModelSerializer):
    """Сериализатор для песен"""
    albums = serializers.SerializerMethodField()

    def get_albums(self, obj):
        albums = []
        for album in obj.albums.all():
            song_album = SongAlbum.objects.get(song=obj, album=album)
            albums.append({
                'title': album.title,
                'artist': album.artist.name,
                'year': album.year,
                'sequence_number': song_album.sequence_number,
            })
        return albums

    class Meta:
        model = Song
        fields = ['id', 'title', 'albums']


class SongAlbumSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления песен в альбомы"""
    album = serializers.CharField(source='album.title')
    song = serializers.CharField(source='song.title')

    class Meta:
        model = SongAlbum
        fields = ['id', 'song', 'album', 'sequence_number']

    def create(self, validated_data):
        album_title = validated_data.pop('album')['title']
        song_title = validated_data.pop('song')['title']
        album = get_object_or_404(Album, title=album_title)
        song = get_object_or_404(Song, title=song_title)
        sequence_number = validated_data.get('sequence_number')
        if SongAlbum.objects.filter(song=song, album=album).exists():
            raise serializers.ValidationError(
                f'Песня "{song_title}" уже находится в альбоме "{album_title}"'
            )
        if SongAlbum.objects.filter(album=album,
                                    sequence_number=sequence_number).exists():
            raise serializers.ValidationError(
                f'Номер песни "{sequence_number}"'
                f' в альбоме "{album_title}" уже занят'
            )
        if SongAlbum.objects.filter(song=song,
                                    sequence_number=sequence_number).exists():
            raise serializers.ValidationError(
                f'Песня "{song_title}" уже находится в другом альбоме'
                f' под таким же номером'
            )
        return SongAlbum.objects.create(song=song, album=album,
                                        sequence_number=sequence_number)

from django.db import models

from .validators import validate_sequence_number


class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=255, unique=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    year = models.IntegerField()


class Song(models.Model):
    title = models.CharField(max_length=255, unique=True)
    albums = models.ManyToManyField(Album, through='SongAlbum')


class SongAlbum(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    sequence_number = models.IntegerField(
        validators=[validate_sequence_number])

    class Meta:
        unique_together = [('song', 'sequence_number'),
                           ('song', 'album'),
                           ('album', 'sequence_number')]

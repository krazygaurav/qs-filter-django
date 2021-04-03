from django.db import models

class TopSongPoularity(models.Model):
	title = models.CharField(max_length = 220)
	artist = models.CharField(max_length = 220)
	top_genre = models.CharField(max_length = 220)
	year = models.IntegerField()
	pop = models.IntegerField()
	duration = models.IntegerField()
	country = models.CharField(max_length = 100)

	def __str__(self):
		return self.title

from django.db import models


class NewsItem(models.Model):
    main_url = models.URLField()
    name_of_group = models.CharField(max_length=200)
    title = models.CharField(max_length=200, unique=True)
    authors = models.CharField(max_length=200)
    date = models.DateTimeField()
    text = models.TextField()
    name_of_subgroup = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

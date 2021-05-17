from django.db import models
from django.db.models import indexes

# Create your models here.

# assumes that author's name is unique


class Author(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    dob = models.DateField(null=True)
    pob = models.CharField(max_length=100, null=True)
    profilelink = models.URLField(null=True)

# assumes that quote can exist without author
class Quote(models.Model):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=2000)
    author = models.ForeignKey(Author,
                               on_delete=models.SET_NULL,
                               null=True,
                               db_index=True)
    createdtime = models.DateTimeField()
    modifiedtime = models.DateTimeField()


class Tag(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class QuoteAndTag(models.Model):
    id = models.UUIDField(primary_key=True)
    quote = models.ForeignKey(Quote,
                              on_delete=models.CASCADE,
                              db_index=True)
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            db_index=True)

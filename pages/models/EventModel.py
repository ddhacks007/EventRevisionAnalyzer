from django.db import models
from django.utils.timezone import now
from pages.models.TagModel import Tag

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=200)
    date = models.DateField(default=now())
    description = models.TextField(max_length=400)
    tags = models.ManyToManyField(Tag, related_name='events')

    def __str__(self):
        return self.name
    class Meta:
        unique_together = (('name', 'date'))
        db_table = 'event'
        
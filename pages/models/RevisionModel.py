from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from pages.models.TitleModel import Titles
from pages.models.TagModel import Tag

class Revision(models.Model):
    id = models.BigIntegerField(default=0, unique=True, primary_key=True)  
    title = models.ForeignKey(Titles, on_delete=models.CASCADE, db_column='title_id', default=1)
    parent_id = models.BigIntegerField(default=0)  
    timestamp = models.DateTimeField() 
    month = models.SmallIntegerField(default=1)
    year = models.SmallIntegerField(default=1)
    day = models.SmallIntegerField(default=1)
    tags = models.ManyToManyField(Tag, related_name='revisions')
    comment = models.TextField(default="*")

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(day__range=(1, 31)),
                name="%(app_label)s_%(class)s_day_check"
            ),
            models.CheckConstraint(
                check=models.Q(month__range=(1, 12)),
                name="%(app_label)s_%(class)s_month_check"
            ),
            models.CheckConstraint(
                check=models.Q(year__gte=1),
                name="%(app_label)s_%(class)s_year_check"
            )
        ]
        db_table = 'revision'

    def __str__(self):
        return str(self.id)
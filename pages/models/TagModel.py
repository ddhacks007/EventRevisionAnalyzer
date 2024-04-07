from django.db import models

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'tag'
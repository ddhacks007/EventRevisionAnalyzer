from django.db import models

class Titles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'titles'

    def __str__(self):
        return self.name
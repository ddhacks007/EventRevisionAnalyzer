from pages.models.TitleModel import Titles
from django.db import IntegrityError

def get_title_id(title):
    try:
        return Titles.objects.filter(name=title)[0].id
    except IntegrityError as e:
        print(e)

def create_title(name):
    try:
        Titles(name=name).save()
    except IntegrityError as e:
        print(e)
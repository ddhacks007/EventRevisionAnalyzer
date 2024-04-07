from pages.models.EventModel import Event
from pages.models.TagModel import Tag
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError

def create_event(event_details):
    try:
        with transaction.atomic():
            event = Event(
                name=event_details.get('name'),  
                date=event_details.get('date'),
                description=event_details.get('description')
            )
            event.save()

            tags = event_details.get('tags')  
            for tag_name in tags.split(","):
                tag, created = Tag.objects.get_or_create(name=tag_name)
                event.tags.add(tag)

    except ValidationError as e:
        print(f"Validation error while creating event or tag: {e}")
        
    except IntegrityError as e:
        print(f"Database integrity error while creating event or tag: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


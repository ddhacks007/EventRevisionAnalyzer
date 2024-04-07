from django.db import transaction
from  pages.models.RevisionModel import Revision  
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from datetime import datetime
from django.db.models import Q


def convert_timestamp(timestamp_str):
    try:
        return datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as e:
        print(f"Error converting timestamp: {e}")
        return None 

def insert_revisions(title_id, revisions):
    try:
        with transaction.atomic():
            revision_objects = []
            for revision in revisions:
                timestamp = convert_timestamp(revision['timestamp'])
                if timestamp is None:  
                    continue
                rev = Revision(
                    title_id=title_id,
                    id=revision['revid'],
                    parent_id=revision['parentid'],
                    timestamp=timestamp,
                    month=timestamp.month,
                    year=timestamp.year,
                    day=timestamp.day,
                    comment=revision['comment']
                )
                revision_objects.append(rev)
            
            Revision.objects.bulk_create(revision_objects, ignore_conflicts=True)
            
               
    except IntegrityError as e:
        print(e)
       
    except ValidationError as e:
        print(f"Data validation error: {e}")
    except Exception as e:
        print(f"Unexpected error during insertion: {e}")



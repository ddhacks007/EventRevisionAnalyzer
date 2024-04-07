from django.db import connection
from django.db.utils import IntegrityError, OperationalError

def insert_revision_tag(revision_tag):
    if revision_tag:
        values = []
        for rev_id, tag_ids in revision_tag.items():
            values.extend(f"({rev_id}, {tag_id})" for tag_id in tag_ids)
        query = f"INSERT INTO revision_tags (revision_id, tag_id) VALUES {', '.join(values)} ON CONFLICT DO NOTHING"
        try:
            with connection.cursor() as cursor:
                print(query)
                cursor.execute(query)
                print('executed!')
        except IntegrityError as e:
            print(f"An integrity error occurred: {e}")
        except OperationalError as e:
            print(f"An operational error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    


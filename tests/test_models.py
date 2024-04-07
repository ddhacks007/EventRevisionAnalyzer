from pages.components.CRUD.Event import create_event
from pages.models.EventModel import Event
from pages.components.CRUD.Title import create_title
from pages.models.TitleModel import Titles
from pages.models.TagModel import Tag
from pages.components.CRUD.Revision import insert_revisions
from pages.components.CRUD.RevisionTag import insert_revision_tag
from pages.models.RevisionModel import Revision
from django.test import TestCase
import datetime

class TestModels(TestCase):
    
    def test_if_event_is_created_correctly(self):
        event_details = {'name': 'test-event', 'date': datetime.date(2019, 8, 20), 'description': 'test event', 'tags': 'test,test1'}
        create_event(event_details)
        assert Event.objects.filter(name='test-event')[0].name == 'test-event'
    
    def test_if_revision_are_getting_inserted_in_bulk_with_ignore_conflicts(self):
        
        create_title('title')
        
        title = Titles.objects.filter(name='title')[0]
        
        revisions = [{'timestamp': '2018-7-14T00:00:00Z', 'revid': 124124, 'parentid': 124124, 'month': 7, 'day': 14, 'year': 2018, 'comment': '*'}
                     ,{'timestamp': '2018-7-14T00:00:00Z', 'revid': 124124, 'parentid': 124124, 'month': 7, 'day': 14, 'year': 2018, 'comment': '*'},
                     ]
        insert_revisions(title.id, revisions)
        assert len(Revision.objects.all()) == 1

    def test_if_revision_tags_are_getting_inserted_in_bulk_with_ignore_conflicts(self):
        event_details = {'name': 'test-event', 'date': datetime.date(2019, 8, 20), 'description': 'test event', 'tags': 'test,test1'}
        create_event(event_details)
        create_title('title')
        title = Titles.objects.filter(name='title')[0]
        tag1 = Tag.objects.all()[0].id
        tag2 = Tag.objects.all()[1].id

        revisions = [{'timestamp': '2018-7-14T00:00:00Z', 'revid': 124124, 'parentid': 124124, 'month': 7, 'day': 14, 'year': 2018, 'comment': '*'}]
        insert_revisions(title.id, revisions)
        insert_revision_tag({'124124': [tag1, tag2]})
        queryset = Revision.objects.prefetch_related('tags')
        for obj in queryset:
            assert len(obj.tags.all()) == 2
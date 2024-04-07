from pages.components.RevisionManager import RevisionManager
from pages.components.CRUD.Revision import insert_revisions
from pages.components.CRUD.Title import get_title_id
from pages.components.Tasks.TagAssigner import assign_tags
from django_q.tasks import async_task

def initiate_rev_fetch(args):
    print(args)
    rm = RevisionManager()
    revisions = rm.get_revisions(args['title'], args['event_date'])
    title_id = get_title_id(args['title'])
    insert_revisions(title_id, revisions)
    n = len(revisions)
    print('total-length of revisions are', n, 'for the title', args['title'], args['event_date'])
    for i in range(0, n, 50):
        print(i, i+50)
        async_task(assign_tags, {'revisions': revisions[i:i+50], 'event_name': args['event_name']})
    print('task ended successfully!!')
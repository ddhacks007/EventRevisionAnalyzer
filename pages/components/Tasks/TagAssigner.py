from pages.models.TagModel import Tag
from pages.components.TagManager import TagManager
from pages.components.CRUD.RevisionTag import insert_revision_tag

def assign_tags(args):
    revs = args['revisions']
    tags = {}
    for tag in Tag.objects.all():
        tags[tag.id] = tag.name
    tag_manager = TagManager()
    print('Trying to assign tags to the revisions', len(revs))
    print(tags)
    revision_tag = tag_manager.assign_tags_to_revisions(revs, tags)
    print('Assigned......')
    print(revision_tag)
    insert_revision_tag(revision_tag)
    print('Assigned and Inserted.')

    

from bs4 import BeautifulSoup
from pages.components.API.Wiki import WikiAPI
import collections

class TagManager:
    def __init__(self):
        self.api = WikiAPI()

    @staticmethod
    def find_tags_from_word_list(words, tags):
        result = set()
        for word in words:
            word_lower = word.lower()
            for id_, name in tags.items():
                if name.lower() in word_lower:
                    result.add(id_)
        return list(result)

    def assign_tags(self, revision_tags, rev_id, words, tags):
        ext_tags = TagManager.find_tags_from_word_list(words, tags)
        if ext_tags:
            revision_tags[rev_id].extend(ext_tags)
            revision_tags[rev_id] = list(set(revision_tags[rev_id]))  

    def extract_content_from_html(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        added_lines = soup.find_all(class_='diff-addedline diff-side-added')
        result = [ins.get_text() for line in added_lines for ins in line.find_all('ins')] or [line.get_text() for line in added_lines]
        return result

    def assign_tags_on_content(self, revision_tags, revision, tags):
        revid = revision['revid']
        parentid = revision['parentid']
        response = self.api.get_revision_diff_content(revid, parentid)
        
        if 'compare' in response:
            content = response['compare']['*']
            result = self.extract_content_from_html(content)
            self.assign_tags(revision_tags, revid, result, tags)


    def assign_tags_on_comment(self, revision_tags, revision, tags):
        revid = revision['revid']
        words = revision['comment'].lower().split()
        self.assign_tags(revision_tags, revid, words, tags)

    def assign_tags_on_rev_tags(self, revision_tags, revision, tags):
        revid = revision['revid']
        self.assign_tags(revision_tags, revid, revision['tags'], tags)

    def assign_tags_to_revisions(self, revisions, tags):
        revision_tags = collections.defaultdict(list)
        for i, rev in enumerate(revisions):
            # print(i)
            if 'comment' in rev:
                self.assign_tags_on_comment(revision_tags, rev, tags)
            
            self.assign_tags_on_content(revision_tags, rev, tags)
            self.assign_tags_on_rev_tags(revision_tags, rev, tags)
        return revision_tags

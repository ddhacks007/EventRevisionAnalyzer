from pages.components.API.Wiki import WikiAPI

class RevisionManager:
    def __init__(self):
        self.api = WikiAPI()

    def get_revisions(self, title, event_date):
        continue_param = None
        result = []
        while True:
            continue_param, revisions = self.api.get_revisions_from_wiki(title, event_date, continue_param)
            result.extend(revisions)
            if not continue_param:
                break
        return result


from pages.components.ClassType.SingletonMeta import SingletonMeta
from pages.components.API.SessionManager import SessionManager
from datetime import timedelta
import os
from dotenv import load_dotenv
from eventrevisionanalyzer.settings import max_day_limit
class WikiAPI(metaclass=SingletonMeta):
    url = "https://en.wikipedia.org/w/api.php"

    def get_revision_diff_content(self, revid, parentid):
        with SessionManager() as session:
            response = session.get(url=self.url, params={
                'action': 'compare', 
                'fromrev': parentid, 
                'torev': revid, 
                'format': 'json'
            })
            return response.json()

    def get_revisions_from_wiki(self, title, event_date, continue_param=None):
        with SessionManager() as session:
            params = {
                'action': 'query', 
                'prop': 'revisions', 
                'rvprop': 'ids|timestamp|comment|tags', 
                'rvslots': 'main', 
                'rvdir': 'newer',
                'formatversion': '2', 
                'rvstart': event_date.strftime('%Y-%m-%dT%H:%M:%S') + 'Z',
                'rvend': (event_date + timedelta(days=max_day_limit)).strftime('%Y-%m-%dT%H:%M:%S') + 'Z',
                'format': 'json', 
                'rvlimit': 'max', 
                'titles': title
            }
            if continue_param:
                params.update(continue_param)
            
            response = session.get(url=self.url, params=params)
            data = response.json()
            
            result = []
            for page in data.get('query', {}).get('pages', []):
                result.extend(page.get('revisions', []))
            
            return data.get('continue'), result

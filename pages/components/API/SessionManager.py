import requests

class SessionManager:
    def __enter__(self):
        self.session = requests.Session()
        return self.session
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

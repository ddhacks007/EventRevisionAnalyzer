from pages.components.CRUD.EventRevision import get_rev_count_by_event_title, get_rev_count_by_event_tag, get_days_from_period
from django.test import TestCase
import datetime

class TestDashboardQueries(TestCase):
    fixtures = ['tests/static/testdata.json']
    
    def get_total_count(self, event_title_count):
        total_count = 0
        for event in event_title_count:
            total_count += event_title_count[event]['total_count']
        return total_count

    def get_total_count_from_event_tag(self, event_tag):
        total_count = 0
        for event in event_tag:
            for tag in event_tag[event]:
                total_count += event_tag[event][tag]
        return total_count
    
    def test_filters_for_event_title_fetcher(self):
        filters = {'timeperiod': '1 year', 'event': 'First perovskite solar cell reported'}
        count = self.get_total_count(get_rev_count_by_event_title(filters))
        assert count == 17
        filters = {'timeperiod': '1 month'}
        count = self.get_total_count(get_rev_count_by_event_title(filters))
        assert count == 28
        filters = {'timeperiod': '1 year'}
        count = self.get_total_count(get_rev_count_by_event_title(filters))
        assert count == 42
        filters = {'timeperiod': '1 month', 'event': "1% of global energy demands met by solar"}
        count = self.get_total_count(get_rev_count_by_event_title(filters))
        assert count == 1
        count = self.get_total_count(get_rev_count_by_event_title(filters))
    
    def test_filters_for_event_tag_fetcher(self):
        filters = {'timeperiod': '15 day', 'event': 'First perovskite solar cell reported'}
        count = self.get_total_count_from_event_tag(get_rev_count_by_event_tag(filters))
        assert count == 16
        filters = {'timeperiod': '4 week', 'event': 'SunShot initiative announced'}
        count = self.get_total_count_from_event_tag(get_rev_count_by_event_tag(filters))
        assert count == 9
        filters = {'timeperiod': '6 month', 'event': "Dual-layer solar cell reaches efficiency of nearly 30% "}
        count = self.get_total_count_from_event_tag(get_rev_count_by_event_tag(filters))
        assert count == 11


    def test_days_from_time_part(self):
        assert get_days_from_period('4 day') == 4
        assert get_days_from_period('1 year') == 365
        assert get_days_from_period('4 months') == 120
        assert get_days_from_period('6 months') == 180
        assert get_days_from_period('12 months') == 360
        assert get_days_from_period('3 week') == 21
        assert get_days_from_period('5 year') == 5*365
        assert get_days_from_period('1 day') == 1


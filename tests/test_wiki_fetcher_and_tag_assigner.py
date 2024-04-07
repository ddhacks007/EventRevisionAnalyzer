from django.test import TestCase
import unittest
from pages.components.RevisionManager import RevisionManager
from pages.components.TagManager import TagManager

from pages.models.TagModel import Tag

import os
import datetime
import collections

class RevisionFetcherTest(TestCase):
    
    def test_revision_count_does_not_change_for_given_param(self):
        os.environ['max_day_limit'] = '30'
        rm = RevisionManager()

        event_date = datetime.date(2009, 4, 14)
        
        titles = ["Semiconductor", "Perovskite_solar_cell", "Solar_cell"]
        values = [15, 0, 73]
        for i, title in enumerate(titles):
            assert len(rm.get_revisions(title, event_date)) >= values[i]
    
class TagAssignerTest(TestCase):
    def test_the_tags_are_correctly_found_from_the_word_list(self):
        tm = TagManager()
        res = tm.find_tags_from_word_list(['tock', 'ding', 'dong'], {1: 'tick', 2: 'tock'})
        assert res == [2]
        res = tm.find_tags_from_word_list(['tock', 'ding', 'omblette'], {1: 'omblette', 2: 'tock'})
        assert res == [1, 2] 
        res = tm.find_tags_from_word_list(['dd', 'gg', 'awesome'], {1: 'aa', 2: 'bb'})
        assert  res == []

    def test_the_tags_are_correctly_found_from_the_comment_passed(self):
        tm = TagManager()
        revision_tags = collections.defaultdict(list)
        tm.assign_tags_on_comment(revision_tags, {'revid': '12412', 'comment': 'Swift SolaR is doing awesome'}, {1: 'swift', 2: 'great', 3: 'impeccable!'})
        tm.assign_tags_on_comment(revision_tags, {'revid': '12345', 'comment': 'undertaker is doing great'}, {1: 'swift', 2: 'haha', 3: 'superb!!!'})
        assert revision_tags['12345'] == []
        assert revision_tags['12412'] == [1]

    def test_partial_tags_are_not_picked_from_the_comment(self):
        tm = TagManager()
        revision_tags = collections.defaultdict(list)
        tm.assign_tags_on_comment(revision_tags, {'revid': '12412', 'comment': 'swift Solar launching there ground breaking technology to the wold'}, {1: 'peaceful world', 2: 'blessed world', 3: 'ground shaking'})
        assert revision_tags['12412'] == []
        
    def test_subword_with_tag_are_picked_from_the_comment(self):
        tm = TagManager()
        revision_tags = collections.defaultdict(list)
        tm.assign_tags_on_comment(revision_tags, {'revid': '12412', 'comment': 'swiftsolar launching there ground breaking technology to the wold'}, {1: 'swift', 2: 'blessed world', 3: 'ground shaking'})
        assert revision_tags['12412'] == [1]
          
    def test_subword_with_tag_are_picked_from_the_comment(self):
        tm = TagManager()
        revision_tags = collections.defaultdict(list)
        tm.assign_tags_on_comment(revision_tags, {'revid': '12412', 'comment': 'swiftsolar launching there ground breaking technology to the wold'}, {1: 'swift', 2: 'blessed world', 3: 'ground shaking'})
        assert revision_tags['12412'] == [1]

    def test_if_added_line_is_properly_extracted_from_content_diff_html(self):
        tm = TagManager()
        result = ['===ADVANTAGES===', 'Renewable Energy Source. Among all the benefits of solar panels, the most important thing is that solar energy is a truly renewable energy source. ...', 'Reduces Electricity Bills. ...', 'Diverse Applications. ...', 'Low Maintenance Costs. ...', 'Technology Development.', '===DISADVANTAGES===', 'Cost. The initial cost of purchasing a solar system is fairly high. ...', 'Weather-Dependent. Although solar energy can still be collected during cloudy and rainy days, the efficiency of the solar system drops. ...', 'Solar Energy Storage Is Expensive. ...', 'Uses a Lot of Space. ...', 'Associated with Pollution.']
        html = open('./tests/static/test1.txt').read()
        assert tm.extract_content_from_html(html) == result

    def test_if_added_word_is_extracted_From_ins_tag(self):
        tm = TagManager()
        
        result = ['|bibcode=2016EnPro..92..785D ', '|bibcode=2011EnPro...8..648H ']
        html = open('./tests/static/test2.txt').read()
        assert tm.extract_content_from_html(html) == result
    



    
        
        
if __name__ == '__main__':
    # Use test discovery to execute all test classes
    unittest.main()

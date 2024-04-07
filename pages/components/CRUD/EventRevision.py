from django.db import connection
from pages.models.RevisionModel import Revision
from django.db.models import Count
from django.db.models import Q, F
from datetime import timedelta
from eventrevisionanalyzer.settings import max_day_limit
import collections

def get_days_from_period(period):
    time_to_days = {
        'day': 1,
        'week': 7,
        'month': 30,
        'year': 365,
    }
    number, unit = period.split()
    unit = unit.rstrip('s')
    return int(number) * time_to_days[unit] if unit in time_to_days else 0

def group_event_title_count(data):
    transformed_data = {}

    for item in data:
        title_name = item['title_name']
        event_name = item['event_name']
        total_count = item['total_count']

        if event_name not in transformed_data:
            transformed_data[event_name] = {'total_count': 0}

        if title_name not in transformed_data[event_name]:
            transformed_data[event_name][title_name] = {'count': 0}
        transformed_data[event_name]['total_count'] += total_count
        transformed_data[event_name][title_name]['count'] += total_count

    return transformed_data

def group_event_tag_count(data):
    transformed_data = {}

    for item in data:
        tag_name = item['tag_name']
        event_name = item['event_name']

        if event_name not in transformed_data:
            transformed_data[event_name] = {}
        if tag_name not in transformed_data[event_name]:
             transformed_data[event_name][tag_name] = 0

        transformed_data[event_name][tag_name] += item['total_count']

    return transformed_data


def generate_condition(filters):
        conditions = Q(tags__events__date__lt=F('timestamp')) 
        max_year = max_day_limit//365
        time_part = f"{max_year} year" if filters.get('timeperiod', "all") == "all" else filters['timeperiod']
        days_ = get_days_from_period(time_part)
        conditions &= Q(timestamp__lt=F('tags__events__date') + timedelta(days=days_+1))
        if 'event' in filters and filters['event'] != 'all':
            conditions &= Q(tags__events__name=filters['event'])
       
        if 'title' in filters and filters['title'] != 'all':
            conditions &= Q(title__name=filters['title'])

        return conditions

def get_rev_count_by_event_title(filters):
    
    conditions = generate_condition(filters)
    return group_event_title_count((Revision.objects
    .filter(
        conditions
    )
    .annotate(
        event_name=F('tags__events__name'),
        title_name=F('title__name')  
    )
    .values('title_name', 'event_name')
    .annotate(total_count=Count('id', distinct=True)) 
    .values('title_name', 'event_name', 'total_count')
    ).order_by('title_name', 'event_name'))


def get_rev_count_by_event_tag(filters):
    conditions = generate_condition(filters)
    return group_event_tag_count((Revision.objects
    .filter(
        conditions
    )
    .annotate(
        event_name=F('tags__events__name'),
        tag_name = F('tags__name')  
    )
    .values('event_name', 'tag_name')
    .annotate(total_count=Count('id', distinct=True)) 
    .values('tag_name', 'event_name', 'total_count')
    ).order_by('event_name', 'tag_name'))

def get_rev_count(filters):
    event_title = get_rev_count_by_event_title(filters)
    event_tag = get_rev_count_by_event_tag(filters)
    return event_title, event_tag
    


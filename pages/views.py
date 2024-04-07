from django_q.tasks import async_task
from pages.components.CRUD.Event import create_event
from pages.models.EventModel import Event
from pages.models.TitleModel import Titles
from pages.models.TagModel import Tag
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
from pages.components.CRUD.EventRevision import get_rev_count
from pages.components.CRUD.Title import create_title
from django.shortcuts import render
import json
from pages.components.Tasks.RevisionFetcher import initiate_rev_fetch
from collections import defaultdict
import uuid

@require_http_methods(["POST"])
def schedule_title_fetch_from_wiki_api(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        for title in data['titles']:
            create_title(title)

        return JsonResponse({"result": "Job scheduled successfully!!"})
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500) 

@require_http_methods(["POST"])
def setup_event(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        data['date'] = datetime.strptime(data.get('date'), "%m/%d/%Y")
        create_event(data)
        for title in Titles.objects.all():
            args = {'title': title.name, "event_date": data['date'], 'event_name': data['name']}
            print('enquing data..')
            async_task(initiate_rev_fetch, args, task_name=uuid.uuid4())
        
        return JsonResponse({"result": "Event created successfully!"}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"message": str(e)}, status=500)

@require_http_methods(["GET"])
def get_revision_correlation(request):
    try:
        filters = dict(request.GET.items())
        event_title_count, event_tag_count = get_rev_count(filters)
        default_filters = {
            'timeperiod':  ['1 day', '1 week', '2 weeks', '3 weeks', '1 month', '2 months', '6 months', '1 year'][::-1], 
            'time_part': ['day', 'all', 'month', 'year'], 
            'title': ['all'] + [title.name for title in Titles.objects.all()], 
            'event': ['all'] + [event.name for event in Event.objects.all()], 
            'tag': ['all'] + [tag.name for tag in Tag.objects.all()]
        }
    
        return render(request, 'Dashboard.html', {"eventTitle": json.dumps(event_title_count),
                                                  "eventTag": json.dumps(event_tag_count),
                                                  "filters":json.dumps(default_filters, default=str) })
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
    
@require_http_methods(["GET"])
def get_manual_doc(request):
    return render(request, 'Manual.html')
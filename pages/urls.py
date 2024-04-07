from django.urls import path
from . import views

urlpatterns = [
    path('create', views.setup_event, name='index'),
    path('get_event_revision_relation', views.get_revision_correlation),
    path('manual', views.get_manual_doc),
    path('schedule_title_fetch', views.schedule_title_fetch_from_wiki_api)
]
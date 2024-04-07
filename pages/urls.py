from django.urls import path
from . import views

urlpatterns = [
    path('create', views.setup_event, name='index'),
    path('dashboard', views.get_event_revision_count),
    path('manual', views.get_manual_doc),
    path('schedule_title_fetch', views.schedule_title_fetch_from_wiki_api)
]
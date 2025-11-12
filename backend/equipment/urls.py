from django.urls import path
from .views import UploadCSVView, DatasetHistoryView

urlpatterns = [
    path('upload/', UploadCSVView.as_view(), name='upload'),
    path('history/', DatasetHistoryView.as_view(), name='history'),
]

from django.urls import path
from .views import UploadCSVView, DatasetHistoryView , DownloadPDFView

urlpatterns = [
    path('upload/', UploadCSVView.as_view(), name='upload'),
    path('history/', DatasetHistoryView.as_view(), name='history'),
    path('download/', DownloadPDFView.as_view(), name='download_pdf'),
]

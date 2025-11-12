import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer

class UploadCSVView(APIView):
    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        # Read CSV with pandas
        df = pd.read_csv(file_obj)

        # Compute summary stats
        summary = {
            'total_equipment': len(df),
            'average_flowrate': df['Flowrate'].mean(),
            'average_pressure': df['Pressure'].mean(),
            'average_temperature': df['Temperature'].mean(),
            'type_distribution': df['Type'].value_counts().to_dict(),
        }

        # Save dataset record
        dataset = EquipmentDataset.objects.create(file=file_obj, summary=summary)

        # Keep only last 5 datasets
        all_datasets = EquipmentDataset.objects.all().order_by('-uploaded_at')
        if len(all_datasets) > 5:
            for old in all_datasets[5:]:
                old.delete()

        return Response(EquipmentDatasetSerializer(dataset).data, status=status.HTTP_201_CREATED)


class DatasetHistoryView(APIView):
    def get(self, request):
        datasets = EquipmentDataset.objects.all().order_by('-uploaded_at')[:5]
        serializer = EquipmentDatasetSerializer(datasets, many=True)
        return Response(serializer.data)

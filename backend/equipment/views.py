import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EquipmentDataset
from .serializers import EquipmentDatasetSerializer
import tempfile, os
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

from rest_framework.permissions import AllowAny

class PublicView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Hello, world!"})

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

class DownloadPDFView(APIView):
    def get(self, request):
        dataset_id = request.GET.get("id")
        print(request)
        if not dataset_id:
            return Response({"error": "Missing dataset ID"}, status=400)

        dataset = EquipmentDataset.objects.filter(id=dataset_id).first()
        if not dataset or not dataset.summary:
            return Response({"error": "Dataset not found or no summary available"}, status=404)

        summary = dataset.summary
        print(summary)
        total = summary.get("total_equipment", 0)
        flow = summary.get("average_flowrate", 0)
        pressure = summary.get("average_pressure", 0)
        temp = summary.get("average_temperature", 0)
        dist = summary.get("type_distribution", {})

        # Create temp PDF file
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(tmpfile.name, pagesize=A4)
        width, height = A4

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1 * inch, height - 1 * inch, "Chemical Equipment Summary Report")

        # Summary numbers
        c.setFont("Helvetica", 12)
        y = height - 1.5 * inch
        for line in [
            f"Total Equipments: {total}",
            f"Average Flowrate: {flow:.2f}",
            f"Average Pressure: {pressure:.2f}",
            f"Average Temperature: {temp:.2f}",
        ]:
            c.drawString(1 * inch, y, line)
            y -= 0.3 * inch

        # Type distribution text
        y -= 0.3 * inch
        c.setFont("Helvetica-Bold", 13)
        c.drawString(1 * inch, y, "Equipment Type Distribution")
        y -= 0.3 * inch
        c.setFont("Helvetica", 11)
        for k, v in dist.items():
            c.drawString(1 * inch, y, f"{k}: {v}")
            y -= 0.25 * inch

        # Generate bar chart using matplotlib
        if dist:
            fig, ax = plt.subplots(figsize=(6,3))
            ax.bar(dist.keys(), dist.values(), color="skyblue")
            ax.set_title("Equipment Type Distribution")
            ax.set_ylabel("Count")
            ax.set_xlabel("Equipment Type")
            fig.tight_layout()

            # Save chart to temporary PNG
            chart_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            fig.savefig(chart_file.name, bbox_inches="tight")
            plt.close(fig)

            # Embed chart in PDF
            chart_width = 5.5 * inch
            chart_height = 3 * inch
            if y - chart_height < 0.5 * inch:
                c.showPage()
                y = height - 1 * inch
            c.drawImage(chart_file.name, 1 * inch, y - chart_height, width=chart_width, height=chart_height)

            # Clean up temp chart
            chart_file.close()
            os.remove(chart_file.name)

        c.showPage()
        c.save()

        return FileResponse(open(tmpfile.name, "rb"), as_attachment=True, filename="equipment_summary.pdf")

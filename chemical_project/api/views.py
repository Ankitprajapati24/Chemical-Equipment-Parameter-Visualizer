
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import pandas as pd
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
from .serializers import FileUploadSerializer
from .models import EquipmentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer


# --- AUTHENTICATION VIEWS ---

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    return Response({'error': 'Invalid Credentials'}, status=400)


class AnalyzeData(APIView):
    parser_classes = [MultiPartParser]

    # 1. GET: Fetch History
    def get(self, request):
        history = EquipmentFile.objects.all().order_by('-uploaded_at')[:5]
        data = []
        for item in history:
            data.append({
                "id": item.id,
                "date": item.uploaded_at.strftime("%Y-%m-%d %H:%M"),
                "total_count": item.total_count,
                "avg_temp": item.avg_temp,
                "avg_pressure": item.avg_pressure
            })
        return Response(data)

    # 2. POST: Upload & Analyze
    def post(self, request):
        print("--- NEW REQUEST RECEIVED ---") # Debug 1
        serializer = FileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # A. Save File
                file_obj = serializer.save()
                print(f"File saved: {file_obj.file.path}") # Debug 2
                
                # B. Analyze with Pandas
                df = pd.read_csv(file_obj.file.path)
                
                # C. Calculate Stats
                stats = {
                    "total_count": len(df),
                    "avg_temp": df['Temperature'].mean() if 'Temperature' in df else 0,
                    "avg_pressure": df['Pressure'].mean() if 'Pressure' in df else 0,
                    "avg_flow": df['Flowrate'].mean() if 'Flowrate' in df else 0,
                }

                # D. Save Stats to DB
                file_obj.total_count = stats["total_count"]
                file_obj.avg_temp = stats["avg_temp"]
                file_obj.avg_pressure = stats["avg_pressure"]
                file_obj.avg_flow = stats["avg_flow"]
                file_obj.save()
                
                # E. Response Data
                response_data = {
                    "id": file_obj.id,
                    "total_equipment_count": stats["total_count"],
                    "average_temperature": stats["avg_temp"],
                    "average_pressure": stats["avg_pressure"],
                    "average_flowrate": stats["avg_flow"],
                    "type_counts": df['Type'].value_counts().to_dict() if 'Type' in df else {},
                    "preview": df.head(5).to_dict(orient='records')
                }
                return Response(response_data)

            except Exception as e:
                print(f"CRASH ERROR: {str(e)}") # Debug 3
                return Response({"error": str(e)}, status=400)
        
        else:
            print(f"VALIDATION ERROR: {serializer.errors}") # Debug 4
            return Response(serializer.errors, status=400)


class GeneratePDF(APIView):
    def get(self, request, file_id):
        # 1. Get the specific file record from the database
        try:
            record = EquipmentFile.objects.get(id=file_id)
        except EquipmentFile.DoesNotExist:
            return Response({"error": "File not found"}, status=404)

        # 2. Create the PDF Response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="report_{file_id}.pdf"'

        # 3. Draw on the Canvas
        p = canvas.Canvas(response, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "Chemical Equipment Analysis Report")

        p.setFont("Helvetica", 12)
        p.drawString(100, 730, f"Generated for Upload ID: {record.id}")
        p.drawString(100, 715, f"Date: {record.uploaded_at.strftime('%Y-%m-%d %H:%M')}")

        # Draw the Line
        p.line(100, 700, 500, 700)

        # Draw the Stats
        p.drawString(100, 670, f"Total Equipment Count: {record.total_count}")
        p.drawString(100, 650, f"Average Temperature: {record.avg_temp:.2f} C")
        p.drawString(100, 630, f"Average Pressure: {record.avg_pressure:.2f} atm")
        p.drawString(100, 610, f"Average Flowrate: {record.avg_flow:.2f} L/min")

        # Footer
        p.setFont("Helvetica-Oblique", 10)
        p.drawString(100, 50, "Generated by Hybrid Visualizer App")

        # 4. Close and Return
        p.showPage()
        p.save()
        return response

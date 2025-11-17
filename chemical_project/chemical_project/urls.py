from django.contrib import admin
from django.urls import path
from api.views import AnalyzeData  # Import your view\
from api.views import AnalyzeData, GeneratePDF
from api.views import AnalyzeData, GeneratePDF, register_user, login_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/analyze/', AnalyzeData.as_view()),
    path('api/report/<int:file_id>/', GeneratePDF.as_view()), 
    path('api/register/', register_user),
    path('api/login/', login_user),
]
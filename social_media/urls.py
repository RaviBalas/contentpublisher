from django.urls import path
from .views import Testview, InstagramView

urlpatterns = [
    path('test/', Testview.as_view()),
    path('instagram/', InstagramView.as_view()),
]

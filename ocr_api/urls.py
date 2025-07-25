from django.urls import path
from . import views

app_name = 'ocr_api'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/captcha/ddddocr/classification/', views.ocr_classification, name='ocr_classification'),
    # 可选的类视图版本
    # path('api/captcha/ddddocr/classification/', views.OCRClassificationView.as_view(), name='ocr_classification'),
]
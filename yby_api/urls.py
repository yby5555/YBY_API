from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def handler404(request, exception):
    return JsonResponse({
        'status': 0,
        'msg': f'api:{request.build_absolute_uri()} not found'
    }, status=404)

def handler500(request):
    return JsonResponse({
        'status': 0,
        'errorMsg': 'internal error'
    }, status=500)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ocr_api.urls')),
    path('data_export/', include('data_export.urls')),
]

# 自定义错误处理
handler404 = handler404
handler500 = handler500

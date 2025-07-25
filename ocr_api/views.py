import base64
import json
import traceback
import warnings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import ddddocr

warnings.filterwarnings("ignore")

# 全局OCR实例，避免重复初始化
ocr = ddddocr.DdddOcr(show_ad=False)


def index(request):
    """首页"""
    return JsonResponse({
        'message': 'Welcome to DdddOcr Crack System',
        'status': 'success'
    })


@csrf_exempt
@require_http_methods(["POST"])
def ocr_classification(request):
    """OCR验证码识别接口"""
    try:
        img_bytes = None
        
        # 处理form-data中的img_data字段
        if 'img_data' in request.POST:
            img_bytes = request.POST.get('img_data')
        
        # 处理文件上传
        elif request.FILES:
            # 获取第一个上传的文件
            for file_key in request.FILES:
                uploaded_file = request.FILES[file_key]
                img_bytes = uploaded_file.read()
                break
        
        # 处理JSON请求体
        elif request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                img_bytes = data.get('img_data')
            except json.JSONDecodeError:
                pass
        
        if not img_bytes:
            return JsonResponse({
                'status': 0,
                'msg': 'No image data provided'
            })
        
        # 如果是base64字符串，进行解码
        if isinstance(img_bytes, str):
            try:
                img_bytes = base64.b64decode(img_bytes)
            except Exception as e:
                return JsonResponse({
                    'status': 0,
                    'msg': f'Base64 decode error: {str(e)}'
                })
        
        # 执行OCR识别
        result = ocr.classification(img_bytes)
        
        return JsonResponse({
            'status': 1,
            'msg': 'success',
            'ret': result
        })
        
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({
            'status': 0,
            'msg': str(e)
        })


# 基于类的视图版本（可选，用于更复杂的逻辑）
@method_decorator(csrf_exempt, name='dispatch')
class OCRClassificationView(View):
    """OCR识别类视图"""
    
    def post(self, request):
        return ocr_classification(request)

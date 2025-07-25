import json
import csv
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import tempfile
import zipfile
from io import BytesIO

class MongoDBExporter:
    def __init__(self, mongo_uri, db_name=None, collection_name=None):
        """初始化MongoDB导出器"""
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        
    def connect(self):
        """连接到MongoDB"""
        try:
            self.client = MongoClient(self.mongo_uri)
            if self.db_name:
                self.db = self.client[self.db_name]
                if self.collection_name:
                    self.collection = self.db[self.collection_name]
            # 测试连接
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"连接MongoDB失败: {e}")
            return False
    
    def close(self):
        """关闭MongoDB连接"""
        if self.client:
            self.client.close()
    
    def get_databases(self):
        """获取所有数据库列表"""
        try:
            return self.client.list_database_names()
        except Exception as e:
            print(f"获取数据库列表失败: {e}")
            return []
    
    def get_collections(self, db_name):
        """获取指定数据库的所有集合"""
        try:
            db = self.client[db_name]
            return db.list_collection_names()
        except Exception as e:
            print(f"获取集合列表失败: {e}")
            return []
    
    def get_fields(self, db_name, collection_name, sample_size=100):
        """获取集合的字段信息"""
        try:
            db = self.client[db_name]
            collection = db[collection_name]
            
            # 获取样本文档来分析字段
            sample_docs = list(collection.find().limit(sample_size))
            if not sample_docs:
                return []
            
            # 收集所有字段
            all_fields = set()
            field_types = {}
            
            for doc in sample_docs:
                for key, value in doc.items():
                    all_fields.add(key)
                    if key not in field_types:
                        field_types[key] = type(value).__name__
            
            return [{'name': field, 'type': field_types[field]} for field in sorted(all_fields)]
        except Exception as e:
            print(f"获取字段信息失败: {e}")
            return []
    
    def datetime_handler(self, obj):
        """处理日期时间对象的JSON序列化"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def export_data(self, db_name, collection_name, query={}, fields=None, limit=None, export_format='json'):
        """导出数据"""
        try:
            db = self.client[db_name]
            collection = db[collection_name]
            
            # 构建查询
            if fields:
                # 构建字段投影
                projection = {field: 1 for field in fields}
                cursor = collection.find(query, projection)
            else:
                cursor = collection.find(query)
            
            if limit:
                cursor = cursor.limit(limit)
            
            # 转换为列表
            data = list(cursor)
            
            print(f"查询结果数量: {len(data)}")
            print(f"查询条件: {query}")
            print(f"字段选择: {fields}")
            
            # 处理ObjectId和datetime
            for doc in data:
                for key, value in doc.items():
                    if isinstance(value, ObjectId):
                        doc[key] = str(value)
                    elif isinstance(value, datetime):
                        doc[key] = value.isoformat()
            
            return data
        except Exception as e:
            print(f"导出数据失败: {e}")
            import traceback
            traceback.print_exc()
            return []

def index(request):
    """数据导出主页面"""
    return render(request, 'data_export/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def get_databases(request):
    """获取数据库列表"""
    try:
        data = json.loads(request.body)
        mongo_uri = data.get('mongo_uri')
        
        if not mongo_uri:
            return JsonResponse({'error': 'MongoDB URI is required'}, status=400)
        
        exporter = MongoDBExporter(mongo_uri)
        if not exporter.connect():
            return JsonResponse({'error': 'Failed to connect to MongoDB'}, status=500)
        
        databases = exporter.get_databases()
        exporter.close()
        
        return JsonResponse({'databases': databases})
    except Exception as e:
        print(f"获取数据库列表失败: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def get_collections(request):
    """获取集合列表"""
    try:
        data = json.loads(request.body)
        mongo_uri = data.get('mongo_uri')
        db_name = data.get('db_name')
        
        if not mongo_uri or not db_name:
            return JsonResponse({'error': 'MongoDB URI and database name are required'}, status=400)
        
        exporter = MongoDBExporter(mongo_uri)
        if not exporter.connect():
            return JsonResponse({'error': 'Failed to connect to MongoDB'}, status=500)
        
        collections = exporter.get_collections(db_name)
        exporter.close()
        
        return JsonResponse({'collections': collections})
    except Exception as e:
        print(f"获取集合列表失败: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def get_fields(request):
    """获取字段列表"""
    try:
        data = json.loads(request.body)
        mongo_uri = data.get('mongo_uri')
        db_name = data.get('db_name')
        collection_name = data.get('collection_name')
        
        if not mongo_uri or not db_name or not collection_name:
            return JsonResponse({'error': 'MongoDB URI, database name and collection name are required'}, status=400)
        
        exporter = MongoDBExporter(mongo_uri)
        if not exporter.connect():
            return JsonResponse({'error': 'Failed to connect to MongoDB'}, status=500)
        
        fields = exporter.get_fields(db_name, collection_name)
        exporter.close()
        
        return JsonResponse({'fields': fields})
    except Exception as e:
        print(f"获取字段列表失败: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

def convert_date_strings_to_datetime(obj):
    """递归转换查询条件中的日期字符串为datetime对象"""
    import re
    from datetime import datetime
    
    # ISO日期格式的正则表达式
    iso_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$')
    # 简单日期格式的正则表达式
    simple_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            result[key] = convert_date_strings_to_datetime(value)
        return result
    elif isinstance(obj, list):
        return [convert_date_strings_to_datetime(item) for item in obj]
    elif isinstance(obj, str):
        # 尝试转换ISO格式日期字符串
        if iso_date_pattern.match(obj):
            try:
                # 处理带毫秒的情况
                if '.' in obj:
                    return datetime.fromisoformat(obj.replace('Z', '+00:00'))
                else:
                    return datetime.fromisoformat(obj)
            except ValueError:
                pass
        # 尝试转换简单日期格式
        elif simple_date_pattern.match(obj):
            try:
                return datetime.strptime(obj, '%Y-%m-%d')
            except ValueError:
                pass
        return obj
    else:
        return obj

@csrf_exempt
@require_http_methods(["POST"])
def export_data(request):
    """导出数据"""
    try:
        data = json.loads(request.body)
        mongo_uri = data.get('mongo_uri')
        db_name = data.get('db_name')
        collection_name = data.get('collection_name')
        query_conditions = data.get('query_conditions', {})
        selected_fields = data.get('selected_fields', [])
        limit = data.get('limit')
        export_format = data.get('export_format', 'json')
        
        if not mongo_uri or not db_name or not collection_name:
            return JsonResponse({'error': 'MongoDB URI, database name and collection name are required'}, status=400)
        
        # 处理查询条件
        query = {}
        if query_conditions:
            try:
                query = json.loads(query_conditions) if isinstance(query_conditions, str) else query_conditions
                # 转换查询条件中的日期字符串为datetime对象
                query = convert_date_strings_to_datetime(query)
                print(f"转换后的查询条件: {query}")
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid query conditions format'}, status=400)
        
        # 处理限制条数
        if limit:
            try:
                limit = int(limit)
            except ValueError:
                limit = None
        
        exporter = MongoDBExporter(mongo_uri)
        if not exporter.connect():
            return JsonResponse({'error': 'Failed to connect to MongoDB'}, status=500)
        
        # 导出数据
        exported_data = exporter.export_data(
            db_name, 
            collection_name, 
            query=query, 
            fields=selected_fields if selected_fields else None,
            limit=limit,
            export_format=export_format
        )
        exporter.close()
        
        if not exported_data:
            return JsonResponse({'error': 'No data found or export failed'}, status=404)
        
        # 根据格式返回文件
        filename = f"{collection_name}_export"
        
        if export_format == 'json':
            # 创建datetime处理函数
            def datetime_handler(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                elif isinstance(obj, ObjectId):
                    return str(obj)
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
            
            # 每条数据一行的格式
            if isinstance(exported_data, list):
                json_lines = [json.dumps(item, ensure_ascii=False, separators=(',', ':'), default=datetime_handler) for item in exported_data]
                json_content = '\n'.join(json_lines)
            else:
                json_content = json.dumps(exported_data, ensure_ascii=False, separators=(',', ':'), default=datetime_handler)
            
            response = HttpResponse(
                json_content,
                content_type='application/json'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}.json"'
            
        elif export_format == 'csv':
            if exported_data:
                df = pd.DataFrame(exported_data)
                csv_buffer = BytesIO()
                df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
                csv_buffer.seek(0)
                
                response = HttpResponse(
                    csv_buffer.getvalue(),
                    content_type='text/csv'
                )
                response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
            else:
                return JsonResponse({'error': 'No data to export'}, status=404)
                
        elif export_format == 'excel':
            if exported_data:
                df = pd.DataFrame(exported_data)
                excel_buffer = BytesIO()
                df.to_excel(excel_buffer, index=False, engine='openpyxl')
                excel_buffer.seek(0)
                
                response = HttpResponse(
                    excel_buffer.getvalue(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
            else:
                return JsonResponse({'error': 'No data to export'}, status=404)
        else:
            return JsonResponse({'error': 'Unsupported export format'}, status=400)
        
        return response
        
    except Exception as e:
        print(f"导出数据失败: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

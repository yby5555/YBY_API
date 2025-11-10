import os
import re
import argparse
import sys
from pathlib import Path
col_name ={
    'DiseaseItem':'疾病表',
    'CheckItem':'检查表',
    'MedicineItem':'药品表',
    'TreatmentItem':'治疗表',
    'VaccineItem':'疫苗表',
}


def parse_field_comments(file_content):
    """解析Scrapy Item文件的字段注释，只返回有注释的字段"""
    fields = []
    
    # 匹配字段定义和注释
    field_pattern = r'^(\s*)(\w+)\s*=\s*scrapy\.Field\(\)\s*(#\s*(.*))?$'
    
    lines = file_content.split('\n')
    for line in lines:
        match = re.match(field_pattern, line.strip())
        if match:
            field_name = match.group(2)
            comment = match.group(4) or ''
            
            # 只处理有注释的字段
            if comment.strip():
                # 解析注释格式: 类型-含义-具体信息
                comment_parts = comment.split('-')
                data_type = comment_parts[0].strip() if len(comment_parts) > 0 else ''
                meaning = comment_parts[1].strip() if len(comment_parts) > 1 else ''
                details = comment_parts[2].strip() if len(comment_parts) > 2 else ''
                
                fields.append({
                    'name': field_name,
                    'data_type': data_type,
                    'meaning': meaning,
                    'details': details
                })
    
    return fields

def generate_html_doc(fields, title, output_file):
    """生成HTML文档"""
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        
        .container {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
            margin-bottom: 30px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 20px;
        }}
        
        .header h1 {{
            color: #2c3e50;
            margin: 0;
            font-size: 2.5em;
        }}
        
        .header .back-link {{
            display: inline-block;
            margin-top: 15px;
            color: #6c757d;
            text-decoration: none;
        }}
        
        .header .back-link:hover {{
            color: #495057;
        }}
        
        .stats {{
            background: #e8f5e8;
            border: 1px solid #c3e6c3;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }}
        
        th {{
            background: #2c3e50;
            color: white;
            font-weight: 600;
        }}
        
        tr:hover {{
            background-color: #f8f9fa;
        }}
        
        .field-name {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        .data-type {{
            color: #e74c3c;
            font-family: 'Courier New', monospace;
        }}
        
        .details {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        
        .no-comment {{
            color: #adb5bd;
            font-style: italic;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <a href="index.html" class="back-link">← 返回首页</a>
        </div>
        
        <div class="stats">
            共找到 {len(fields)} 个字段 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>字段名</th>
                    <th>数据类型</th>
                    <th>字段含义</th>
                    <th>具体信息</th>
                </tr>
            </thead>
            <tbody>'''
    
    for field in fields:
        html_content += f'''
                <tr>
                    <td class="field-name">{field['name']}</td>
                    <td class="data-type">{field['data_type'] or '<span class="no-comment">未指定</span>'}</td>
                    <td>{field['meaning'] or '<span class="no-comment">未指定</span>'}</td>
                    <td class="details">{field['details'] or '<span class="no-comment">无</span>'}</td>
                </tr>'''
    
    html_content += '''
            </tbody>
        </table>
        
        <div class="footer">
            由 Scrapy 字段文档生成器自动生成
        </div>
    </div>
</body>
</html>'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

def scan_scrapy_items_folder(folder_path):
    """扫描scrapy_items文件夹中的Python文件"""
    items = []
    
    for file_path in Path(folder_path).glob('*.py'):
        if file_path.name != '__init__.py':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找类名
            class_match = re.search(r'class\s+(\w+)\s*\(\s*scrapy\.Item\s*\):', content)
            if class_match:
                class_name = class_match.group(1)
                items.append({
                    'filename': file_path.name,
                    'class_name': class_name,
                    'file_path': str(file_path)
                })
    
    return items

def generate_index_page(items, output_file):
    """生成首页"""
    html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scrapy 字段文档中心</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.8em;
            font-weight: 300;
        }
        
        .header p {
            margin: 10px 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .items-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .item-card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid #e9ecef;
        }
        
        .item-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }
        
        .item-card h3 {
            margin: 0 0 10px;
            color: #2c3e50;
            font-size: 1.3em;
        }
        
        .item-card .filename {
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 15px;
        }
        
        .item-card .link {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            font-size: 0.9em;
            transition: background 0.2s;
        }
        
        .item-card .link:hover {
            background: #218838;
        }
        
        .instructions {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
        }
        
        .instructions h3 {
            margin: 0 0 15px;
            color: #856404;
        }
        
        .instructions ol {
            margin: 0;
            padding-left: 20px;
        }
        
        .instructions li {
            margin-bottom: 8px;
        }
        
        .instructions code {
            background: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #6c757d;
            font-size: 0.9em;
            border-top: 1px solid #e9ecef;
            padding-top: 20px;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #6c757d;
        }
        
        .empty-state h3 {
            margin: 0 0 10px;
            color: #495057;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Scrapy 字段文档中心</h1>
        <p>集中管理所有 Scrapy Item 字段说明文档</p>
    </div>
    
    <div class="instructions">
        <h3>使用说明</h3>
        <ol>
            <li>将 Scrapy Item 文件放入 <code>scrapy_items</code> 文件夹</li>
            <li>文件格式要求：包含 <code>class 类名(scrapy.Item):</code></li>
            <li>字段注释格式：<code># 类型-含义-具体信息</code></li>
            <li>保存文件后，文档会自动生成并显示在此页面</li>
        </ol>
    </div>'''
    
    if items:
        html_content += '''
    <div class="items-grid">'''
        
        for item in items:
            doc_filename = f"{Path(item['filename']).stem}_docs.html"
            html_content += f'''
        <div class="item-card">
            <h3>{col_name[item['class_name']]}</h3>
            <div class="filename">文件: {item['filename']}</div>
            <a href="{doc_filename}" class="link">查看字段说明 →</a>
        </div>'''
        
        html_content += '''
    </div>'''
    else:
        html_content += '''
    <div class="empty-state">
        <h3>暂无 Scrapy Item 文件</h3>
        <p>请将 Scrapy Item 文件放入 scrapy_items 文件夹</p>
    </div>'''
    
    html_content += '''
    <div class="footer">
        共发现 {} 个 Scrapy Item 文件 | 最后更新: {}
    </div>
</body>
</html>'''.format(len(items), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    parser = argparse.ArgumentParser(description='Scrapy 字段文档生成器')
    parser.add_argument('input_file', nargs='?', help='Scrapy Item 文件路径')
    parser.add_argument('-o', '--output', help='输出HTML文件路径')
    parser.add_argument('-t', '--title', help='文档标题')
    parser.add_argument('--scan', action='store_true', help='扫描scrapy_items文件夹并生成首页')
    
    args = parser.parse_args()
    
    if args.scan:
        # 扫描文件夹并生成首页
        items_folder = Path(__file__).parent / 'scrapy_items'
        items = scan_scrapy_items_folder(items_folder)
        
        # 为每个Item生成文档
        for item in items:
            with open(item['file_path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            fields = parse_field_comments(content)
            doc_filename = f"{Path(item['filename']).stem}_docs.html"
            doc_title = f"{item['class_name']} 字段说明"
            
            generate_html_doc(fields, doc_title, doc_filename)
            print(f"已生成: {doc_filename} ({len(fields)} 个字段)")
        
        # 生成首页
        generate_index_page(items, 'index.html')
        print(f"已生成首页: index.html (共 {len(items)} 个Item)")
        
    elif args.input_file:
        # 单个文件处理模式
        if not os.path.exists(args.input_file):
            print(f"错误: 文件不存在 - {args.input_file}")
            sys.exit(1)
        
        with open(args.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fields = parse_field_comments(content)
        
        # 确定输出文件名和标题
        output_file = args.output or f"{Path(args.input_file).stem}_docs.html"
        title = args.title or f"{Path(args.input_file).stem} 字段说明"
        
        generate_html_doc(fields, title, output_file)
        print(f"已生成: {output_file} (共 {len(fields)} 个字段)")
        
    else:
        print("请提供输入文件或使用 --scan 参数扫描文件夹")
        parser.print_help()

if __name__ == '__main__':
    from datetime import datetime
    main()
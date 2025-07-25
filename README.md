# YBY API

一个基于Django的API项目，提供OCR识别和MongoDB数据导出功能。

## 功能特性

- **OCR识别**: 使用ddddocr库进行图像文字识别
- **数据导出**: 支持MongoDB数据导出为JSON、CSV、Excel格式
- **Web界面**: 提供友好的Web操作界面

## 技术栈

- Python 3.8+
- Django 5.2.4
- MongoDB
- ddddocr
- pandas
- pymongo

## 安装部署

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd YBY_API
```

### 2. 创建虚拟环境
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# 或
source .venv/bin/activate  # Linux/Mac
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 运行项目
```bash
# Windows
.\start.bat

# 或手动启动
python manage.py runserver 0.0.0.0:20125
```

### 5. 访问应用
- OCR识别: http://localhost:20125/ocr/
- 数据导出: http://localhost:20125/data_export/

## 项目结构

```
YBY_API/
├── data_export/          # 数据导出模块
├── ocr_api/             # OCR识别模块
├── yby_api/             # Django主配置
├── requirements.txt     # 依赖包列表
├── start.bat           # Windows启动脚本
└── manage.py           # Django管理脚本
```

## 使用说明

### OCR识别
1. 访问 `/ocr/` 页面
2. 上传图片文件
3. 获取识别结果

### 数据导出
1. 访问 `/data_export/` 页面
2. 输入MongoDB连接信息
3. 选择数据库和集合
4. 选择要导出的字段
5. 选择导出格式并下载

## 注意事项

- 确保MongoDB服务正在运行
- 首次运行需要安装所有依赖包
- 生产环境请修改Django的SECRET_KEY和DEBUG设置

## 更新代码

### 推送更新
```bash
git add .
git commit -m "描述你的更改"
git push origin main
```

### 拉取更新
```bash
git pull origin main
pip install -r requirements.txt  # 如果有新依赖
```

## 许可证

本项目仅供学习和研究使用。
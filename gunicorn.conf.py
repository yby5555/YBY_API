# Gunicorn配置文件
import multiprocessing

# 服务器socket
bind = "0.0.0.0:20125"
backlog = 2048

# Worker进程
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# 重启
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# 日志
accesslog = "access.log"
errorlog = "error.log"
loglevel = "info"

# 进程命名
proc_name = 'yby_api'

# 用户权限
# user = "www-data"
# group = "www-data"

# 临时目录
tmp_upload_dir = None
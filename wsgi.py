'启动开发环境配置的服务器'
from app import create_app
from app.setting import Config

app = create_app(config=Config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='56789')

# gunicorn 运行命令
# gunicorn -w 20 -b 0.0.0.0:56789 wsgi:app --reload -t 500 -D
# 需要在此文件夹下运行该命令

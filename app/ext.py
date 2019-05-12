# flask 相关扩展

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager


# 实例化
db = SQLAlchemy()
cors = CORS(supports_credentials=True)
loginmanaer = LoginManager()
loginmanaer.session_protection = 'strong'

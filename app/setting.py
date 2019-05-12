'默认设置'

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # "mysql+pymysql://root:Manyan189@rm-bp185n4mr88761p188o.mysql.rds.aliyuncs.com:3306/hmh_db"
    # "mysql+pymysql://root:123456@127.0.0.1:3306/kanman_test"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Manyan189@rm-bp185n4mr88761p188o.mysql.rds.aliyuncs.com:3306/hmh_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'w:{S:D72@$de(*&85'

    # flask_cookies 保留cookies7天
    REMEMBER_COOKIE_DURATION = 60*60*24*7
    REMEMBER_COOKIE_HTTPONLY = True


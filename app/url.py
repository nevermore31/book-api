# 所有url存放此处

from flask_restful import Api
from app.search.views import BookInfoApi, BookVolumeApi


kanman_api = Api(prefix='/book')


# 查询小说类
kanman_api.add_resource(BookInfoApi, '/all')
kanman_api.add_resource(BookVolumeApi, '/info/<book_id>')

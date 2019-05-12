# 所有url存放此处

from flask_restful import Api
from app.search.views import GetComic, ComicInfoBody


kanman_api = Api(prefix='/book')


# 查询漫画类
kanman_api.add_resource(GetComic, '/all')
kanman_api.add_resource(ComicInfoBody, '/body/<comic_id>')

# 账号类
kanman_api.add_resource(CreatAcoount, '/account/create')
kanman_api.add_resource(Login, '/account/login')
kanman_api.add_resource(Logout, '/account/logout')
kanman_api.add_resource(RevicePassword, '/account/revice')
kanman_api.add_resource(CheckoutAccount, '/account/checkout')

# 用户收藏
kanman_api.add_resource(Colle, '/colle')

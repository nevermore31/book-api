from app.models.search import BookInfo, BookVolume, BookChapter
from app.ext import db
from app.tool import PaginationMixin, AbortMsg
from flask import request
from flask_restful import Resource
import json


class GetBook(PaginationMixin, AbortMsg, Resource):

    def get(self):
        """
        所有小说信息, 并根据关键字进行分页, 过滤等......
        :return:
        """

        # 男生小说, 女生小说, 默认为男生
        gender = request.args.get('gender', 1)

        # 标签搜索
        tag = request.args.get('tag', None)

        # 漫画名称模糊搜索
        book_name = request.args.get('name', None)

        # status 根据状态码返回(1:连载中, 2:以完结)
        book_status = request.args.get('status', None)
        if book_status not in ['1', '2']:
            self.abort(400, {'msg': '状态码只能为1 或者2'})

        # order_by 根据返回
        comic_order_by = request.args.get('order_by', None)
        if comic_order_by not in ['hot', 'time', 'col']:
            self.abort(400, {'msg': '排序参数只能为<hot, time, col>'})

        # 定义排序
        query = db.session.query(BookInfo).order_by(BookInfo.id.desc())

        # 定义男生女生排序
        query = query.filter(BookInfo.book_gender == int(gender))

        # 定义标签
        if tag:
            query = query.filter(BookInfo.book_type == tag)

        # 模糊搜索结果
        if book_name:
            query = query.filter(BookInfo.book_name.like("%" + book_name + "%"))

        # 状态码过滤
        if book_status:
            if book_status == '1':
                query = query.filter(BookInfo.book_status == '连载中')
            elif book_status == '2':
                query = query.filter(BookInfo.book_status == '以完结')

        # 返回结果进行分页分页
        data, paging_data = self.paginate_query(query)
        results = []

        for d in data:
            result = {
                'book_id': d.book_id,
                'book_name': d.book_name,
                'book_author': d.book_author,
                'book_cover': d.book_cover,
                'book_type': d.book_type,
                'book_status': d.book_status,
                'book_wordsnub': d.book_wordsnub,
                'book_desc': d.book_desc,
                'book_gender': d.book_gender,
                'book_new_chapter': d.book_new_chapter,
            }

            results.append(result)

        return {'data': results, 'paging': paging_data}


class ComicInfoBody(PaginationMixin, AbortMsg, Resource):

    def get(self, comic_id):
        """
        根据特定漫画id获取漫画所有信息或部分信息
        :param comic_id: 漫画id
        :return:
        """
        # 限定是否传输图片地址, 默认为不传输
        img_adr = request.args.get('img_adr', 'False')
        chapter_id = request.args.get('chapter_id', None)

        query_data = db.session.query(ComicData).filter(ComicData.comic_name_id == comic_id).order_by(ComicData.id.desc())
        if query_data.count() == 0:
            return self.abort(400, {'msg': '无此漫画id, 请核对后在查询'})
        query_name = db.session.query(ComicName).\
            filter(ComicName.comic_id == comic_id)

        if chapter_id:
            query_data = query_data.filter(ComicData.chapter_id == chapter_id)

        if query_data.count() == 0:
            return self.abort(400, {'msg': '无此漫画章节id, 请获取所有漫画章节 http:/comic/<漫画id>'})

        results = {
            'comic_id': query_name.one().comic_id,
            'comic_name': query_name.one().comic_name,
            'comic_author': query_name.one().comic_author,
            'comic_desc': query_name.one().comic_desc,
            'comic_local_collec': query_name.one().comic_local_collec,
            'comic_chapter_details': []
        }

        # 返回结果进行分页分页
        data, paging_data = self.paginate_query(query_data)

        for d in data:
            if img_adr == 'False':
                result = {
                    'chapter_name': d.chapter_name,
                    'chapter_id': d.chapter_id,
                    'comic_cover': d.comic_cover,
                    'comic_is_buy': d.comic_is_buy,
                    'create_date': d.create_date,
                }
                results['comic_chapter_details'].append(result)

            elif img_adr == 'True':
                result = {
                    'chapter_name': d.chapter_name,
                    'chapter_id': d.chapter_id,
                    'comic_cover': d.comic_cover,
                    'comic_is_buy': d.comic_is_buy,
                    'create_date': d.create_date,
                    'chapter_image_url': json.loads(d.chapter_image_url)
                }
                results['comic_chapter_details'].append(result)

            else:
                return self.abort(400, {'msg': '必须填入img_adr 参数<False> <True>, 默认为<False>,'
                                               'False : 不返回漫画图片地址, True : 返回漫画图片地址'})
        return {'data': results, 'paging': paging_data}

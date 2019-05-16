from app.models.search import BookInfo, BookVolume, BookChapter
from app.ext import db
from app.tool import PaginationMixin, AbortMsg, PaginationMax
from flask import request
from flask_restful import Resource



class BookInfoApi(PaginationMixin, AbortMsg, Resource):

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

        # # order_by 根据返回
        # comic_order_by = request.args.get('order_by', None)
        # if comic_order_by not in ['hot', 'time', 'col']:
        #     self.abort(400, {'msg': '排序参数只能为<hot, time, col>'})

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


class BookVolumeApi(PaginationMax, AbortMsg, Resource):

    def get(self, book_id):
        """
        根据小说id获取漫画所有信息或部分信息
        :param book_id: 小说id
        :return:
        """
        # 根据章节id查找
        chapter_id = request.args.get('chapter_id', None)

        query_info = db.session.query(BookInfo).filter(BookInfo.book_id == book_id).order_by(BookInfo.id.desc())
        if query_info.count() == 0:
            return self.abort(400, {'msg': '无此小说id, 请核对后在查询'})

        query_volume = db.session.query(BookVolume).\
            filter(BookVolume.book_info_id == book_id)

        query_chapter = db.session.query(BookChapter).filter(BookChapter.book_info_id_chapter == book_id)

        if chapter_id:
            query_chapter = query_chapter.filter(BookChapter.book_chapter_id == chapter_id)

            if query_chapter.count() == 0:
                return self.abort(400, {'msg': '无此小说章节id, 请获取所有小说章节'})

            book_volume_name = query_volume.filter(BookVolume.id == query_chapter.one().book_valume_id_chapter).\
                one().book_volume_name

            chapter_results = {
                'book_name': query_info.one().book_name,
                'book_author': query_info.one().book_author,
                'book_name_chapter': query_chapter.one().book_name_chapter,
                'book_chapter_is_free': query_chapter.one().book_chapter_is_free,
                'book_chapter_content': query_chapter.one().book_chapter_content,
                'book_chapter_id': query_chapter.one().book_chapter_id,
                'book_volume_name': book_volume_name,
            }

            return {'data': chapter_results}

        results = {
            'book_id': query_info.one().book_id,
            'book_name': query_info.one().book_name,
            'book_author': query_info.one().book_author,
            'book_cover': query_info.one().book_cover,
            'book_type': query_info.one().book_type,
            'book_status': query_info.one().book_status,
            'book_wordsnub': query_info.one().book_wordsnub,
            'book_desc': query_info.one().book_desc,
            'book_new_chapter': query_info.one().book_new_chapter,
            'book_volume_chapter': []
        }

        # 返回结果进行分页分页
        data, paging_data = self.paginate_query(query_chapter)
        # 返回数据中看一共包含几个章节
        result_volume = list(set([d.book_valume_id_chapter for d in data]))

        volume_ = query_volume.filter(BookVolume.id.in_(result_volume)).all()
        for v in volume_:
            result = {
                'book_volume_is_free': v.book_volume_is_free,
                'book_volume_name': v.book_volume_name,
                'book_volume_in_chapternub': v.book_volume_in_chapternub,
                'book_volume_wordnub': v.book_volume_wordnub,
                'book_chapter_data': []
            }

        # 添加章节数据至目录
            for d in data:
                chapter_data = {
                    'book_chapter_id': d.book_chapter_id,
                    'book_name_chapter': d.book_name_chapter,
                    'book_chapter_is_free': d.book_chapter_is_free,
                }
                result['book_chapter_data'].append(chapter_data)
            results['book_volume_chapter'].append(result)
        return {'data': results, 'paging': paging_data}

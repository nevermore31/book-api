# 工具类
import re
import unittest
from flask import request, abort, Flask, jsonify
from math import ceil


class PaginationMixin:
    """
    分页, 传入query对象，返回查询结果和paging_data,
    :per_page : 设置每页页数
    """
    page = None
    per_page = None

    def paginate_query(self, query):
        page = self.get_page()
        per_page = self.get_per_page()
        total = self.get_total(query)

        if per_page:
            query = query.limit(per_page)
        else:
            per_page = total if total < 100 else 100

        try:
            total_pages = ceil(total / per_page)
            if total_pages == 0:
                total_pages = 1
        except ZeroDivisionError:
            total_pages = 1

        if page > 1:
            query = query.offset((page - 1) * per_page)

        if page > total_pages:
            # Reduce unnecessary database access.
            results = []
        else:
            results = query.all()

        paging_data = {
            'total': total,
            'total_pages': total_pages,
            'page': page,
            'per_page': per_page,
            'next': page < total_pages,
        }
        return results, paging_data

    def get_page(self):
        page = request.args.get('page', self.page)
        try:
            if page is not None:
                page = int(page)
                if page < 1:
                    raise ValueError
            else:
                page = 1
        except ValueError:
            abort(404, {'msg': "Invalid page, page must be an Positive integer"})
        return page

    def get_per_page(self):
        per_page = request.args.get('per_page', 20)
        try:
            if per_page is not None:
                per_page = int(per_page)
                if per_page < 1:
                    raise ValueError
        except ValueError:
            abort(404, {'msg': "Invalid page size, page size must be an Positive integer"})
        return per_page

    def get_total(self, query):
        return query.order_by(None).count()


class PaginationMax(PaginationMixin):
    def get_per_page(self):
        per_page = request.args.get('per_page', 100)
        try:
            if per_page is not None:
                per_page = int(per_page)
                if per_page < 1:
                    raise ValueError
        except ValueError:
            abort(404, {'msg': "Invalid page size, page size must be an Positive integer"})
        return per_page


class FlaskTestCase(unittest.TestCase):
    '''
    使用方法：
    from app import create_app, db

    class SomeTestCase(FlaskTestCase):
        app = create_app()
        db = db

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_1(self):
            pass
    '''
    app = None
    db = None
    TEST_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/kanman_test"

    def setUp(self):
        if isinstance(self.app, Flask):
            self.app.config['SQLALCHEMY_DATABASE_URI'] = self.TEST_DATABASE_URI
            self.app.testing = True
            self.client = self.app.test_client()
            self.app_context = self.app.app_context()
            self.app_context.push()

            if self.db:
                self.db.create_all()
                self.db.session.remove()

    def tearDown(self):
        # 清除用户表, 便于测试
        pass
        # self.db.session().query(Account).delete()
        # self.db.session().commit()
        #
        # self.db.session.remove()
        # self.db.engine.dispose()
        # self.app_context.pop()


def convert_error(func):
    def validator(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
        except Exception as e:
            raise ValueError(str(e))
        return value
    return validator


class LengthValidator:
    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length
        if self.min_length is not None:
            if self.max_length is not None:
                self.message = "字符串长度应在 %d 和 %d 之间" % (min_length, max_length)
            else:
                self.message = "字符串长度应大于等于 %d" % min_length
        elif self.max_length is not None:
            self.message = "字符串长度应小于等于 %d" % max_length

    @convert_error
    def __call__(self, string, name=None, op=None):
        string = str(string)
        if self.min_length is not None:
            assert len(string) >= self.min_length, self.message
        if self.max_length is not None:
            assert len(string) <= self.max_length, self.message
        return string


class AbortMsg:
    def __call__(self, s, message):
        response = jsonify(message)
        response.status_code = s
        return response

    def abort(self, s, message):
        """
        定义错误方法
        :param message: 传入错误信息
        :return:
        """
        response = jsonify(message)
        response.status_code = s
        return response


class PasswordValidator:
    def __init__(self, minlength, maxlength, special_chars='_'):
        self.minlength = minlength
        self.maxlength = maxlength
        self.special_chars = special_chars

    @convert_error
    def __call__(self, password, name=None, op=None):
        assert len(password) >= self.minlength and len(password) <= self.maxlength, \
            '字符串长度应大于 %d 并小于 %d' \
            % (self.minlength, self.maxlength)

        have_number, have_letter = False, False
        for c in password:
            if c in '1234567890':
                have_number = True
            elif re.match('[a-zA-z]', c):
                have_letter = True
            elif c in self.special_chars:
                pass
            else:
                assert False, \
                    '非法字符 "%s", 密码应该只包含数字、字母和特殊字符： "%s"' \
                    % (c, self.special_chars)
        assert have_number and have_letter, "密码应该同时包含数字和字母"
        return password


@convert_error
def username_validator(value, name=None, op=None):
    assert re.match('^[a-zA-z0-9]{5,15}$', value), '用户名必须为数字或字母，且长度必须在5~15个之间'
    return value


@convert_error
def email_validator(value, name=None, op=None):
    assert re.match('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', value)
    return value


password_validator = PasswordValidator(6, 20, ',.?_!@#$%^&*?')

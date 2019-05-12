from app import create_app, db
from app.tool import FlaskTestCase
from unittest import skip


class SearchTestCase(FlaskTestCase):
    app = create_app()
    db = db

    @skip('本测试没有添加数据, 而是从网络爬取数据, 数据会更新, 所以本测试只适合在本机数据使用')
    def test_getcomic(self):
        """
        本地测试 GetComic view, 数据库采用本地端.
        :return: None
        """
        rsp = self.client.get('/comic/all')
        # 对比漫画作品个数
        self.assertEqual(len(rsp.get_json()['data']), 19)

        rsp = self.client.get('/comic/all?page=2')
        # 对比下一页数据是否为空
        self.assertEqual(rsp.get_json()['paging']['next'], False)

        rsp = self.client.get('/comic/all?tag=xiuzhen')
        # 判断标签时候都包含 <修真> 标签
        for t in rsp.get_json()['data']:
            self.assertIn('xiuzhen', t['comic_type'])

        rsp = self.client.get('/comic/all?tag=D')
        # 判断标签时候都包含 <D(头字母为D)> 标签
        for t in rsp.get_json()['data']:
            self.assertIn('D', t['comic_type'])

        rsp = self.client.get('/comic/all?tag=xiuzhen,D')
        # 判断标签时候都包含 <xiuzhen D> 标签
        for t in rsp.get_json()['data']:
            self.assertIn('xiuzhen', t['comic_type']) and self.assertIn('D', t['comic_type'])

        rsp = self.client.get('/comic/all?tag=xiuzhen,D&name=斗罗大陆')
        # 判断标签时候都包含 <xiuzhen D> 标签 name = 斗罗大陆
        for t in rsp.get_json()['data']:
            self.assertIn('xiuzhen', t['comic_type']) and \
            self.assertIn('D', t['comic_type']) and self.assertIn('斗罗大陆', t['comic_name'])

    @skip('本测试没有添加数据, 而是从网络爬取数据, 数据会更新, 所以本测试只适合在本机数据使用')
    def test_comicinfobody(self):
        """
        测试返回详细数据测试
        :return: None
        """

        # 错误测试

        rsp = self.client.get('/comic/body/')
        self.assertEqual(rsp.status_code, 404)
        self.assertEqual(rsp.get_json(), None)

        rsp = self.client.get('/comic/body/32131')
        self.assertEqual(rsp.status_code, 400)
        self.assertEqual(rsp.get_json(), {'msg': '无此漫画id, 请核对后在查询'})

        rsp = self.client.get('/comic/body/7119?chapter_id=123')
        self.assertEqual(rsp.status_code, 400)
        self.assertEqual(rsp.get_json(), {'msg': '无此漫画章节id, 请获取所有漫画章节 http:/comic/<漫画id>'})

        rsp = self.client.get('/comic/body/7119?chapter_id=170&img_adr=31')
        self.assertEqual(rsp.status_code, 400)
        self.assertEqual(rsp.get_json(), {'msg': '必须填入img_adr 参数<False> <True>, 默认为<False>,'
                                          'False : 不返回漫画图片地址, True : 返回漫画图片地址'})

        # 正确测试  <17745>
        # 查看是否是正序列
        rsp = self.client.get('/comic/body/17745')
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.get_json()['data']['comic_chapter_details'][0]['chapter_name'], '第1话 神秘的黑玉1')

        # 判断地址是否return
        rsp = self.client.get('/comic/body/17745?img_adr=True')
        self.assertEqual(rsp.status_code, 200)
        self.assertIn('chapter_image_url', rsp.get_json()['data']['comic_chapter_details'][0].keys())

    def test_for_local(self):
        data = {
            'nickname': '会飞的猪11',
            'email': '10048893@qq.com',
            'username': 'chenqican111',
            'password': 'chenqican222'
        }
        rsp = self.client.post('/comic/account/create', json=data)
        print(rsp.get_json())
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.get_json()['msg'], '用户创建成功')

        data.pop('nickname')
        data.pop('email')
        print(data)
        rsp = self.client.post('/comic/account/login', json=data)
        print(rsp.get_json())
        self.assertEqual(rsp.status_code, 200)

        rsp = self.client.get('/comic/body/96981')
        print(rsp.get_json())
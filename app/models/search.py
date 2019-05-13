from sqlalchemy import Column, String, Text, Integer, ForeignKey, BigInteger
from app.ext import db


class BookInfo(db.Model):
    __tablename__ = 'book_info'

    id = Column(Integer, primary_key=True)          # 主键
    book_id = Column(BigInteger, unique=True)       # 小说id
    book_name = Column(String(200))                 # 小说名称
    book_author = Column(String(100))               # 小说作者
    book_cover = Column(String(200))                # 小说封面地址
    book_type = Column(String(300))                 # 小说类型
    book_status = Column(String(100))               # 小说状态   连载, 完结
    book_wordsnub = Column(String(100))             # 小说字数
    book_desc = Column(Text)                        # 小说简介
    book_gender = Column(Integer, nullable=False)   # 小说性别 (1:男, 2:女)
    book_new_chapter = Column(String(100))          # 小说最新更新章节

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.book_name)


class BookVolume(db.Model):
    __tablename__ = 'book_volume'

    id = Column(Integer, primary_key=True)              # 主键
    book_volume_is_free = Column(Integer)               # 小说目录是否免费 (1:免费, 2:收费)
    book_volume_name = Column(String(200))              # 小说目录名称
    book_volume_in_chapternub = Column(Integer)         # 小说目录有多少章节
    book_volume_wordnub = Column(String(200))           # 小说目录文字总数

    book_info_id = Column(BigInteger, ForeignKey('book_info.book_id'))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.book_volume_name)


class BookChapter(db.Model):
    __tablename__ = 'book_chapter'

    id = Column(Integer, primary_key=True)                  # 主键
    book_chapter_id = Column(BigInteger, unique=True)       # 小说章节id
    book_name_chapter = Column(String(200))                 # 小说章节名称
    book_chapter_content = Column(Text)                     # 小说章节内容
    book_chapter_is_free = Column(Integer)                  # 小说章节是否免费 (1:免费, 2:收费)

    book_info_id_chapter = Column(BigInteger, ForeignKey('book_info.book_id'))
    book_valume_id_chapter = Column(Integer, ForeignKey('book_volume.id'))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.book_name_chapter)
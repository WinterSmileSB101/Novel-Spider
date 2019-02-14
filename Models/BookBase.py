#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bson import Binary


class BookBase:
    '书籍基类'

    bookId: str
    name: str
    athour: str
    length: str
    intro: str
    latestChapter: str
    tags: list
    cover: str
    status: str
    link: str
    category: str
    updateTime: str
    contentLink: str
    chapters: list
    salt: Binary # 二进制需要通过这种方式保存到 Mongo

    def __init__(self):
        self.name = ''
        self.athour = ''
        self.length = ''
        self.intro = ''
        self.latestChapter = ''
        self.tags = []
        self.cover = ''
        self.status = ''
        self.link = ''
        self.category = ''
        self.updateTime = ''
        self.contentLink = ''
        self.chapters = []
        self.bookId = ''
        self.salt = Binary(b'') # 二进制需要通过这种方式保存到 Mongo


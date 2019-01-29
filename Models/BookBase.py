#!/usr/bin/python
# -*- coding: UTF-8 -*-

class BookBase:
    '书籍基类'

    name:str
    athour:str
    length:str
    intro:str
    latestChapter:str
    tags:list
    cover:str
    status:str
    link:str
    category:str
    updateTime:str
    contentLink:str
    chapters:list

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


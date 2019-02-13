#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Chapter:
    'Book Chapter'
    link:str
    title:str
    content:str
    length:str

    def __init__(self):
        self.link = ''
        self.title = ''
        self.content = ''
        self.length = ''
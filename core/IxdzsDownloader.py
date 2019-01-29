#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import os

from Models.BookBase import BookBase


def start():
    host = "https://www.ixdzs.com"
    page = 0
    urlTemplate = "{host}/new.html?page={page}"
    hasNext = True

    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSTE 5.5; Windows NT)'
    }

    proxies = {
        'http': "http://172.22.8.39:3128",
        'https': "http://172.22.8.39:3128"
    }

    while hasNext:
        page += 1
        url = str.format(urlTemplate, host=host, page=page)
        res = requests.get(url, headers=headers, proxies = proxies)
        res.encoding = 'UTF-8'
        # print(res.text)
        pageDom = BeautifulSoup(res.text, features="lxml-xml") # 加上 lxml-xml 可以去掉自己选择解析器可能造成差异的提醒
        handBookBase(pageDom)


        hasNext = hasNextPage(pageDom)
        # hasNext = False

def handBookBase(dom: BeautifulSoup):
    """
    handle to get book base info
    :param dom: A BeautifulSoup Dom for parse
    :return: BookBase
    """
    books = []
    bookDoms:list = dom.select("div.box_k > ul > li")
    for bookDom in bookDoms:
        book = BookBase()
        book.cover = bookDom.select('.list_img > a > img')[0]['src']
        book.name = bookDom.select('.list_info > .b_name > a')[0].text
        book.athour = bookDom.select('.list_info > .b_info > span > a')[0].text
        book.length = bookDom.select('.list_info > .b_info > span')[1].text
        book.status = bookDom.select('.list_info > .b_info > span > .cp')[0].text
        book.latestChapter = bookDom.select('.list_info > p.b_info')[1].text
        book.intro = bookDom.select('.list_info > p.b_intro')[0].text
        books.append(book)


def hasNextPage(dom: BeautifulSoup):
    next = dom.find_all("a", title=["下一页"], limit=1)
    # print(next.__len__() > 0)
    if(next.__len__() > 0):
        # split /new.html?page=
        page = next[0]['href']
        page = int(str.split(page, "=")[1])
        print("Now Page: " + str(page-1))
    return next.__len__() > 0


# 入口
start()
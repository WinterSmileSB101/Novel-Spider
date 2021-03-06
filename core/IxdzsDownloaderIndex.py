#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import time

import requests
from bs4 import BeautifulSoup
import os

import bson.binary

from DataAccess.StoreToDb import StoreToDB
from Models.BookBase import BookBase
from Models.BookChapter import Chapter
from Utils.Helper import Helper


class IxdzsDownloader:

    path: list
    host: str
    urlTemplate: str
    url: str
    headers: object
    proxies: object
    dataAccess: StoreToDB
    inCompany: bool

    def __init__(self):
        self.path = '/ditu/a.html'
        self.host = 'https://www.ixdzs.com'
        self.urlTemplate = '{host}{path}'

        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSTE 5.5; Windows NT)'
        }

        self.proxies = {
            'http': "http://172.22.8.39:3128",
            'https': "http://172.22.8.39:3128"
        }
        self.inCompany = True

        self.dataAccess = StoreToDB()

    def start(self):
        print("handle page : "+self.path)
        self.url = str.format(self.urlTemplate, host=self.host, path=self.path)
        res = None
        if(self.inCompany):
            res = requests.get(self.url, headers=self.headers, proxies=self.proxies)
        else:
            res = requests.get(self.url, headers=self.headers)

        if(res.status_code==200):
            res.encoding = 'UTF-8'
            pageDom = BeautifulSoup(res.text, features="lxml-xml")
            dbName = "NovelMongo"
            books = self.parsePageBook(pageDom)
            self.dataAccess.store_novel_base_infos(books, dbName)
            allPage = self.parseAllPage(pageDom)
            allPage.remove(self.path)
            Helper.sleep_while(scends=20)
            for page in allPage:
                pageBooks = self.getPageBook(page)
                books = books + pageBooks
                self.dataAccess.store_novel_base_infos(pageBooks, dbName)
                percent = ((allPage.index(page)+1)/allPage.__len__())*100
                print("Process : %.2f%%" % percent)
                if(percent<100):
                    Helper.sleep_while(scends=20)

            self.dataAccess.find_all(dbName,"BookBaseInfo")
            # finalBooks = []
            # for book in books:
             #   finalBooks.append(self.getPerBook(book))

    def parseAllPage(self, dom: BeautifulSoup):
        """
        get all page index
        :param dom: BeautifulSoup Dom
        :return: page index list
        """
        allPages = []
        allPageDoms = dom.select('div.letter > a')
        for pageDom in allPageDoms:
            page = pageDom['href']
            allPages.append(page)
        # allPages = ['/ditu/a.html', '/ditu/b.html']
        return allPages

    def parsePageBook(self, dom: BeautifulSoup):
        """
        get book(name,link) of per page
        :param dom: BeautifulSoup Dom
        :return: Book list
        """
        titleDoms = dom.select('ul.ditu > li')
        books = []
        for titleDom in titleDoms:
            book = BookBase()
            book.link = titleDom.select('a')[0]['href']
            book.name = titleDom.select('a')[0].text
            md5Info = Helper.md5_hash(book.name, False)
            book.bookId = md5Info.MD5
            book.salt = bson.binary.Binary(md5Info.Salt)
            books.append(book)
        return list(books)


    def getPageBook(self, page:str):
        """
        get books of per page
        :param page: page index
        :return: page books
        """
        print("handle page : " + page)
        url = str.format(self.urlTemplate, host = self.host, path = page)
        if(self.inCompany):
            res = requests.get(url, headers=self.headers, proxies=self.proxies)
        else:
            res = requests.get(url, headers=self.headers)
        if(res.status_code==200):
            res.encoding = 'UTF-8'
            pageDom = BeautifulSoup(res.text, features="lxml-xml")
            books = self.parsePageBook(pageDom)
            return books
        return []


    def getPerBook(self, book:BookBase):
        """
        get book information of per book
        :param book: book
        :return: book information
        """
        url = str.format(self.urlTemplate, host = self.host, path = book.link)
        if(self.inCompany):
            res = requests.get(url, headers=self.headers, proxies=self.proxies)
        else:
            res = requests.get(url, headers=self.headers)
        if(res.status_code==200):
            res.encoding = 'UTF-8'
            dom = BeautifulSoup(res.text, features="lxml-xml")
            book = self.parsePerBook(dom,book)
        return book


    def parsePerBook(self, dom:BeautifulSoup, book:BookBase):
        """
        get book info of per book
        :param dom: book BeautifulSoup
        :param book: book
        :return: book
        """
        info = dom.select('div.d_info')[0]
        book.cover = info.select('div.d_af > img')[0]['src']
        statuslist = info.select('div.d_ac > ul > li')
        book.athour = statuslist[0].select('a')[0].text
        book.category = statuslist[1].select('a')[0].text
        book.length = statuslist[2].text
        book.status = statuslist[3].text
        hot = statuslist[4].text
        book.updateTime = statuslist[5].text
        book.contentLink = statuslist[6].select('a.d_ot')[1]['href']
        book.intro = dom.select('div.d_intro > div.d_co')[0].text

        return book


    def getPerBookChapter(self, book:BookBase):
        url = book.contentLink
        res = requests.get(url, headers=self.headers, proxies=self.proxies)
        if(res.status_code==200):
            res.encoding = 'UTF-8'
            dom = BeautifulSoup(res.text, features="lxml-xml")
            book = self.parsePerBookChapter(dom, book)
        return book


    def parsePerBookChapter(self, dom:BeautifulSoup, book:BookBase):
        chapters = dom.select('div.catalog > ul > li')
        bookChaps = []
        for chapter in chapters:
            print(chapter)
            bookChap = Chapter()
            capDom = chapter.select('a')[0]
            bookChap.link = str.format("{host}{path}", host=book.contentLink, path=capDom['href'])
            bookChap.length = capDom['title']
            bookChap.title = capDom.text
            print(bookChap.link)
            bookChaps.append(bookChap)
        return book


spider = IxdzsDownloader()
spider.start()
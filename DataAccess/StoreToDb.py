#!/usr/bin/python
# -*- coding: UTF-8 -*-
import itertools
import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient

from Models import BookBase
from Utils.Helper import Helper


class StoreToDB:
    host: str
    port: int
    client: MongoClient

    def __init__(self):
        self.host = 'localhost'
        self.port = 27017

    def _connect_(self, db_name: str):
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        return self.client[db_name]

    def _close_(self):
        self.client.close()

    def store_novel_base_info(self, book: BookBase, db_name: str):
        db = self._connect_(db_name)
        bookTable = db.BookBaseInfo
        condition = {'bookId': Helper.md5_hash(book.name, False).MD5}
        print(condition)
        record = bookTable.find_one(condition)
        print(record)
        if(record is None):
            # insert
            print(book.__dict__)
            insertRes = bookTable.insert_one(book.__dict__)
            print("Insert Success:"+str(insertRes.inserted_id))
        else:
            # update
            insertRes = bookTable.update(condition, book.__dict__)
            print("Update Success:"+str(insertRes))
        self._close_()

    def store_novel_base_infos(self, books: list, db_name: str):
        db = self._connect_(db_name)
        bookTable = db.BookBaseInfo
        # condition = {'bookId': Helper.md5_hash(book.name, False).MD5}
        # print(condition)
        # record = bookTable.find_one(condition)
            # insert
        print(books)
        insertRes = bookTable.insert_many(books) # 转换list 为 dict
        print("Insert Success:"+str(insertRes.inserted_ids))
        self._close_()

    def find_all(self, db_name: str, collection: str):
        db = self._connect_(db_name)
        collect = db[collection]
        datas = collect.find()
        for data in datas:
            print(data)
        self._close_()

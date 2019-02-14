#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient

from Models import BookBase


class StoreToDB:
    host: str
    port: int
    client: MongoClient

    def __init__(self):
        self.host = 'localhost'
        self.port = 27017

    def _connect_(self, db_name: str):
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        return self.client.db_name

    def _close_(self):
        self.client.close()

    def store_novel_base_info(self, book: BookBase, db_name: str):
        db = self._connect_(db_name)
        bookTable = db.BookBaseInfo
        insertRes = bookTable.insert_one(book)
        print(insertRes.inserted_id)
        self._close_()

    def find_all(self, db_name: str, collection: str):
        db = self._connect_(db_name)
        collect = db[collection]
        datas = collect.find()
        for data in datas:
            print(data)
        self._close_()

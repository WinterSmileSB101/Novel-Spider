#!/usr/bin/python
# -*- coding: UTF-8 -*-
import itertools
from logging import RootLogger

import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from Models import BookBase
from Utils import Logger
from Utils.Helper import Helper


class StoreToDB:
    """
    start mongo db in docker:
    docker pull mongo
    docker run --name cool-mongo -p 27017:27017 -d mongo
    """
    host: str
    port: int
    client: MongoClient
    logger: RootLogger

    def __init__(self):
        self.host = 'localhost'
        self.port = 27017
        self.logger = Logger.get_info_logger(name='dbinsert')

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
            self.logger.info("Insert Success: "+str(insertRes.inserted_id))
        else:
            # update
            insertRes = bookTable.update(condition, book.__dict__)
            self.logger.info("Update Success: "+str(insertRes))
        self._close_()

    def store_novel_base_infos(self, books: list, db_name: str):
        db = self._connect_(db_name)
        bookTable = db.BookBaseInfo
        for book in books:
            try:
                condition = {'bookId': Helper.md5_hash(book.name, False).MD5}
                record = bookTable.find_one(condition)
                if(record is None):
                    bookTable.insert_one(book.__dict__)  # 转换为 dict
                    self.logger.info("Insert Success:" + book.name)
                else:
                    self.logger.warning("Insert Failed: Duplicate id --" +book.name)
            except DuplicateKeyError as dke:
                self.logger.error("Insert Failed: DuplicateKeyError objectId --\n"+dke)

        self._close_()

    def find_all(self, db_name: str, collection: str):
        db = self._connect_(db_name)
        collect = db[collection]
        datas = collect.find()
        print("Find All Mongo: " + db_name + " & Table: " + collection)
        for data in datas:
            print(data)
        self._close_()

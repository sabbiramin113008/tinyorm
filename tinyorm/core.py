# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 03 Feb 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
import pymysql
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Database:

    def __init__(self,
                 db_name: str,
                 user: str,
                 password: str,
                 host: str = 'localhost',
                 port: int = 3307,
                 autocommit: bool = True,
                 connect_timeout: int = 5
                 ):
        self.table_name = None
        try:
            self.conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                db=db_name,
                port=port,
                connect_timeout=connect_timeout,
                autocommit=autocommit,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()
            self.LOGGER = logging.getLogger("DatabaseLog")
        except Exception as e:
            self.LOGGER.error(str(e))
            if self.conn is not None:
                self.conn.close()

    def table(self, table_name: str):
        self.table_name = table_name
        return self

    def insert(self, **kwargs):

        keys = ','.join(k for k in kwargs.keys())
        place_holder = ','.join(['%s' for _ in kwargs.keys()])
        params = ()
        for v in kwargs.values():
            params += (v,)

        sql = '''
        INSERT INTO {} ({}) VALUES({})
        '''.format(self.table_name, keys, place_holder)

        print('sql:', sql, params)

        result = None
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            result = self.cursor.lastrowid
        except Exception as error:
            self.LOGGER.error(str(error))
        finally:
            self.cursor.close()
            self.conn.close()
            return result

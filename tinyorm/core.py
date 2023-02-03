# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 03 Feb 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
from typing import List

import pymysql
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
_AND = 'AND'
_OR = 'OR'


class Field:
    def __init__(self, name):
        self.name = name

    def eq(self, value) -> str:
        sql = '{}={}'.format(self.name, value)
        return sql

    def lt(self, value) -> str:
        sql = '{}<{}'.format(self.name, value)
        return sql

    def gt(self, value) -> str:
        sql = '{}>{}'.format(self.name, value)
        return sql

    def find_in(self, values: List) -> str:
        sql = '{} in {}'.format(self.name, values)
        return sql

    def like(self, value: str) -> str:
        sql = '{} like {}'.format(self.name, value)
        return sql


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
        self.sql = None
        self.table_name = None
        self.params = None
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

    def select(self, fields: List[str] = None):
        if not fields or not len(fields):
            self.sql = '''
            SELECT * from {};
            '''.format(self.table_name)

        return self

    def where(self, conditions: List = None) -> str:
        if not conditions or not len(conditions):
            return self

    def execute(self):
        result = None
        try:
            self.cursor.execute(self.sql, self.params)
            print('SQL:', self.sql, 'params:', self.params)
            result = self.cursor.fetchall()
        except Exception as error:
            self.LOGGER.error(str(error))
        finally:
            self.cursor.close()
            self.conn.close()
            return result

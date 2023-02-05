# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 03 Feb 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
from typing import List

import pymysql
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
_AND = 'AND'
_OR = 'OR'
_NOT = 'NOT'


class Field:
    def __init__(self, name):
        self.name = name

    def cast_type(self, value):
        if isinstance(value, int):
            return int(value)
        if isinstance(value, float):
            return float(value)
        if isinstance(value, str):
            return '\'{}\''.format(value)
        else:
            return value

    def eq(self, value) -> str:
        sql = '{}={}'.format(self.name, self.cast_type(value))
        return sql

    def lt(self, value) -> str:
        sql = '{}<{}'.format(self.name, self.cast_type(value))
        return sql

    def gt(self, value) -> str:
        sql = '{}>{}'.format(self.name, self.cast_type(value))
        return sql

    def find_in(self, values: List) -> str:
        sql = '{} in ({})'.format(self.name, ','.join([str(self.cast_type(v)) for v in values]))
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
        self.SELECT = True
        self.UPDATE = False
        self.DELETE = False
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

    def cast_type(self, value):
        if isinstance(value, int):
            return int(value)
        if isinstance(value, float):
            return float(value)
        if isinstance(value, str):
            return '\'{}\''.format(value)
        else:
            return value

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

    def insert_many(self, rows: List[dict]):
        init_obj = rows[0]
        keys = ','.join(k for k in init_obj.keys())
        place_holder = ','.join(['%s' for _ in init_obj.keys()])
        prep_rows = []
        for row in rows:
            entity = ()
            for k, v in row.items():
                entity += (v,)
            prep_rows.append(entity)

        params = prep_rows

        sql = '''
                INSERT INTO {} ({}) VALUES({})
                '''.format(self.table_name, keys, place_holder)

        print('sql:', sql)
        print('params:', params)

        result = None
        try:
            count = self.cursor.executemany(sql, params)
            self.conn.commit()
            result = count
        except Exception as err:
            self.LOGGER.error(str(err))
        finally:
            self.cursor.close()
            self.conn.close()
            return result

    def select(self, fields: List[str] = None):
        if not fields or not len(fields):
            self.sql = ''' SELECT * from {} '''.format(self.table_name)

        return self

    def update(self, **kwargs):
        set_conditions = []
        for k, v in kwargs.items():
            set_condition = '{}={}'.format(k, self.cast_type(v))
            set_conditions.append(set_condition)
        set_condition_joiner = ','.join(set_conditions)
        self.sql = '''
        UPDATE {} SET {}
        '''.format(self.table_name, set_condition_joiner)
        self.UPDATE = True
        return self

    def delete(self):
        self.sql = ''' DELETE from {}'''.format(self.table_name)
        self.DELETE = True
        return self

    def where(self, conditions: List = None):
        if not conditions or not len(conditions):
            return self
        pre_sql = self.sql
        curr_sql = ' '.join([cond for cond in conditions])
        self.sql = pre_sql + ' WHERE ' + curr_sql
        print('final sql:', self.sql)
        return self

    def execute(self):
        result = None
        try:
            affected_row_count = self.cursor.execute(self.sql, self.params)
            print('sql:', self.sql)
            print('params:', self.params)

            if self.UPDATE:
                self.conn.commit()
                result = affected_row_count
                return result
            if self.DELETE:
                self.conn.commit()
                result = True
                return result
            result = self.cursor.fetchall()
        except Exception as error:
            self.LOGGER.error(str(error))
        finally:
            self.cursor.close()
            self.conn.close()
            return result

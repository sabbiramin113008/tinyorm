# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 03 Feb 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com 

"""
import os
import unittest
from dotenv import load_dotenv
from tinyorm.core import Database

load_dotenv()


class TestTinyOrm(unittest.TestCase):
    table_name = os.environ.get('TABLE_NAME')
    db = Database(
        db_name=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=int(os.environ.get('DB_PORT'))
    )

    def test_insert(self):
        person = {
            'name': 'John doe',
            'age': 30,
            'address': 'Dhaka',
            'hobby': 'Art'
        }
        row_id = self.db.table(self.table_name).insert(**person)
        print('row-id:', row_id)


if __name__ == '__main__':
    unittest.main()

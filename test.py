# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 03 Feb 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com 

"""
import os
import unittest
from dotenv import load_dotenv
from tinyorm.core import Database, Field, _AND

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
            'name': 'Janine doe',
            'age': 33,
            'address': 'Sylhet',
            'hobby': 'Art'
        }
        row_id = self.db.table(self.table_name).insert(**person)
        print('row-id:', row_id)

    def test_get_users(self):
        users = self.db.table(self.table_name).select().where().execute()
        print('users:', users)

    def test_get_user_by_age_and_hobby(self):
        users = self.db.table(self.table_name).select().where([
            Field('age').eq(33), _AND,
            Field('hobby').eq('art')
        ]).execute()
        print('users:', users)

    def test_get_users_where_age_lt_33(self):
        users = self.db.table(self.table_name).select().where([
            Field('age').lt(33)
        ]).execute()
        print('users:', users)

    def test_get_users_where_age_is_in_list_30(self):
        users = self.db.table(self.table_name).select().where([
            Field('age').find_in([33])
        ]).execute()
        print('users:', users)

    def test_get_user_where_address_is_in_dhaka_or_sylhet(self):
        users = self.db.table(self.table_name).select().where([
            Field('address').find_in(['Dhaka', 'Khulna'])
        ]).execute()
        print('users:', users)

    def test_update_users_age_to_50_if_address_is_dhaka(self):
        v_set = {
            'age': 40,
            'hobby': 'Nap'
        }
        user_count = self.db.table(self.table_name).update(**v_set).where([
            Field('address').eq('Dhaka')
        ]).execute()
        print('Affected Row:', user_count)

    def test_delete_users_where_hobby_eq_art(self):
        delete_flag = self.db.table(self.table_name).delete().where([
            Field('hobby').eq('Art')
        ]).execute()
        print('Delete-Flag:', delete_flag)

    if __name__ == '__main__':
        unittest.main()

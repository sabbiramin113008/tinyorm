# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 03 Feb 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com 

"""
import os
import random
import unittest
from dotenv import load_dotenv
from lightorm.core import Database, Field, _AND

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
    first_name = ['John', 'Jane', 'Jason', 'Guido', 'Martin', 'Rob']
    last_name = ['Doe', 'Dee', 'Mraz', 'Van Russom', 'Fowler', 'Pike']
    addresses = ['Dhaka', 'LA', 'Kentucky', 'Madrid', 'Khulna', 'Sylhet']
    hobbies = ['singing', 'art', ' gaming', 'programming', 'writing', 'sleeping']

    def get_name(self):
        name = '{} {}'.format(random.choice(self.first_name),
                              random.choice(self.last_name))
        return name

    def get_age(self):
        return random.choice([i for i in range(25, 60)])

    def get_address(self):
        return random.choice(self.addresses)

    def get_hobby(self):
        return random.choice(self.hobbies)

    def test_insert(self):
        person = {
            'name': self.get_name(),
            'age': self.get_age(),
            'address': self.get_address(),
            'hobby': self.get_hobby()
        }
        row_id = self.db.table(self.table_name).insert(**person)
        print('row-id:', row_id)

    def test_insert_many(self):
        persons = []
        for i in range(1, 50):
            person = {
                'name': self.get_name(),
                'age': self.get_age(),
                'address': self.get_address(),
                'hobby': self.get_hobby()
            }
            persons.append(person)
        count = self.db.table(self.table_name).insert_many(rows=persons)
        print('recored created:', count)

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
            Field('age').lt(35)
        ]).execute()
        print('users:', users)

    def test_get_users_where_age_is_in_list_33(self):
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
            'age': 65,
            'hobby': 'sleeping'
        }
        user_count = self.db.table(self.table_name).update(**v_set).where([
            Field('address').eq('Dhaka')
        ]).execute()
        print('Affected Row:', user_count)

    def test_delete_users_where_hobby_eq_art(self):
        delete_flag = self.db.table(self.table_name).delete().where([
            Field('hobby').eq('sleeping')
        ]).execute()
        print('Delete-Flag:', delete_flag)

    def test_find_not_in(self):
        users = self.db.table(self.table_name).select().where([
            Field('age').find_not_in([49, 39, 28])
        ]).execute()
        print('users:', len(users))


if __name__ == '__main__':
    unittest.main()

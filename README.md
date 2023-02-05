# LightORM
It is what the name means. (Experimental) .
Yet another, super lightweight MySQL ORM in Python. 

## How to Install
`pip install lightorm`

## Connecting and Querying
`LightORM` is designed to reduce the overhead of doing everything and focus on
doing  things in a very light way. First connect with the database, 

```python
import os
from dotenv import load_dotenv

load_dotenv()

from lightorm import Database, Field, _AND

table_name = 'person_table'
db = Database(
    db_name=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=int(os.environ.get('DB_PORT'))
)
```
Here, the `database` configs are read from `.env` file. And the db is instantiated.


## Insert a Record
Inserting a record is quiet simple. 
```python
person = {
    'name': 'John Doe',
    'age': 23,
    'address': 'LA',
    'hobby': 'writing'
    }
row_id = db.table(table_name).insert(**person)
```
If successful, the `insert(**person)` will return the `row-id`


## Insert Multiple Records
Inserting multiple record is simply feeding the `insert_many` method with the
list of the dictionary of the records to be inserted. 
```python
persons = [
    {
    'name': 'John Doe',
    'age': 23,
    'address': 'LA',
    'hobby': 'writing'
    },
    {
    'name': 'Jane Doe',
    'age': 27,
    'address': 'Kentucky',
    'hobby': 'sleeping'
    }
]
record_inserted = db.table(table_name).insert_many(rows=persons)
```
Upon successful insertion, `insert_many` returns the number of rows inserted. 

## Getting Data Back [SELECT/RETRIEVE]
For getting all data back, simply
```python
users = db.table(table_name).select().execute()
```
or simply with empty `where` clause [ not suggested, but it will work]
```python
users = db.table(table_name).select().where().execute()
```
Note, there is an extra method `execute`, required for the operation.



## Filtering
`lightorm` is tested with several filtering, and it is simply chaining 
filtering clauses. Let's see

### Filtering users by `age` and `hobby`
```python
from lightorm import Field,_AND

...
...

users = db.table(table_name).select().where([
    Field('age').eq(33), _AND,
    Field('hobby').eq('programming')
]).execute()

```
### Filtering `users` where `age` is less than 33
```python
users = db.table(table_name).select().where([
    Field('age').lt(35)
]).execute()
print('users:', users)
```
### Filtering users where `adress` is in `['Dhaka','Khulna']
```python
users = db.table(table_name).select().where([
    Field('address').find_in(['Dhaka', 'Khulna'])
]).execute()
print('users:', users)
```

## Updating the Records
`update()` method receivers `key-val` dict for fields to be changed. Simply,
```python
v_set = {
    'age': 65,
    'hobby': 'sleeping'
}
user_count = db.table(table_name).update(**v_set).where([
    Field('address').eq('Dhaka')
]).execute()
print('Affected Row:', user_count)
```
`v_set` is the `dict` that is the followed by `SET` value in `sql` query. 
After successful query, it returns rows affected. 

## Deleting Records
`delete()` works just like the `select()` method. It returns `boolean` `True` if 
is the query is successfully executed. 
```python
delete_flag = self.db.table(self.table_name).delete().where([
    Field('hobby').eq('sleeping')
]).execute()
print('Delete-Flag:', delete_flag)
```

### Almost Full Example
```python
import os
import random
import unittest
from dotenv import load_dotenv
from lightorm import Database, Field, _AND

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


if __name__ == '__main__':
    unittest.main()

```
## Upcoming Features
1. Raw `SQL` execution. 
2. Adding proper Logging and debugging messages.
3. Adding `Aggregate Function` function in the ORM. 

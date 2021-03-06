# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy import Table
from utils.constants import default_engine


class DBInterfaceError(Exception):
    pass


class DBConn(object):
    """DB connection class.
    Args: db_name (str): Default=edw
    """

    def __init__(self, db_name='qiancheng', auto_commit=True):
        self._db_name = db_name
        self._engine = self._get_engine()
        self._connection = self._engine.connect()
        if not auto_commit:
            self._transaction = self._connection.begin()

    def __del__(self):
        if self._connection:
            self._connection.close()

    def get_connect(self):
        return self._connection

    def roll_back(self):
        self._transaction.rollback()

    def commit(self):
        self._transaction.commit()

    def _get_engine(self):
        if self._db_name == 'qiancheng':
            engine = default_engine
        return engine

    def transaction(self):

        return self._transaction

    def execute(self, cmd, get_all=True):
        """
        Execute a sql and return result, fetch one if not get_all.
        :param cmd: str, raw sql string.
        :param get_all: boolean. True if want to fetch all else fetch one.
        :return: Fetch all if get_all else fetch one.
        """
        try:
            result = self._connection.execute(cmd)
            try:
                result = result.fetchall() if get_all else result.fetchone()
            except Exception as e:
                result = result.rowcount
                print(e)
            return result
        except Exception as ex:
            self._connection.close()
            raise DBInterfaceError(ex)

    def insert(self, table_name, data_dict):
        """
        Insert data_dict to table_name.
        :param table_name: str, table to insert into.
        :param data_dict: dict, {key: value} for insert.
        :return: primary keys of inserted elements if insert successfully.
        """
        try:
            table = Table(table_name, sqlalchemy.MetaData(), autoload=True, autoload_with=self._engine)
            stmt = table.insert().values(**data_dict)
            result = self._connection.execute(stmt)
            return result.inserted_primary_key[0] if result.inserted_primary_key else 0
        except Exception as ex:
            self._connection.close()
            print('table_name: ', table_name)
            import traceback
            traceback.print_exc()
            raise DBInterfaceError(ex)

    def update(self, table_name, condition_dict, update_dict):
        """
        Update table_name by update_dict where condition_dict.
        :param table_name: str, table to update.
        :param condition_dict: dict, update condition.
        :param update_dict: dict, {key: value} for update.
        :return: Updated rows count.
        """
        try:
            table = Table(table_name, sqlalchemy.MetaData(), autoload=True, autoload_with=self._engine)
            stmt = table.update().values(**update_dict)
            for key, value in condition_dict.items():
                if key in table.c:
                    where_column = table.c[key]
                    stmt = stmt.where(where_column == value)
            result = self._connection.execute(stmt)
            return result.rowcount
        except Exception as ex:
            self._connection.close()
            raise DBInterfaceError(ex)

    def delete(self, table_name, condition_dict):
        """
        Delete from table_name where condition_dict.
        :param table_name: str, table to delete from.
        :param condition_dict: dict, delete condition.
        :return: Deleted rows count.
        """
        try:
            table = Table(table_name, sqlalchemy.MetaData(), autoload=True, autoload_with=self._engine)
            stmt = table.delete()
            for key, value in condition_dict.items():
                if key in table.c:
                    where_column = table.c[key]
                    stmt = stmt.where(where_column == value)
            result = self._connection.execute(stmt)
            return result.rowcount
        except Exception as ex:
            self._connection.close()
            raise DBInterfaceError(ex)


if __name__ == "__main__":
    from utils.db import DBConn

    db = DBConn()
    results = db.execute("SELECT area_code FROM QianCheng.area_code")
    print(results)


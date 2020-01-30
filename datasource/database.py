# -*- coding: utf-8 -*-
import pg8000
import logging
from DBUtils.PersistentDB import PersistentDB

'''数据库连接池'''

class DataBase(object):

    def __init__(self, user_account):
        try:
            self.__pool = PersistentDB(pg8000, maxusage=1, **user_account).connection()
        except Exception as e:
            logging.exception(e)
    # 获取数据库连接
    def __obtain_connect(self):
        return self.__pool

    # 执行查询类操作
    def query(self, sql):
        results=''
        try:
            db = self.__obtain_connect()
            cursor = db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            print("查询失败->%s" % e)
        finally:
            return results
    #执行插入数据操作,为列表元组数据
    def insert(self, sql, data): #执行插入数据操作
        flag = False
        try:
            db = self.__obtain_connect()
            cursor = db.cursor()
            cursor.executemany(sql, data)
            db.commit()
            cursor.close()
            db.close()
            flag = True
        except Exception as e:
            flag = False
            db.rollback()
            print("执行失败->%s" % e)
        finally:
            return flag
    #执行插入数据操作,json数据
    def insert_json(self, table, data={}):
        flag = False
        try:
            db = self.__obtain_connect()
            cursor = db.cursor()
            keys = ','.join(data.keys())
            values = ','.join(['%s']*len(data))
            sql='insert into {table}({keys}) values ({values})'.format(table=table,keys=keys,values=values)
            cursor.execute(sql,tuple(data.values()))
            db.commit()
            cursor.close()
            db.close()
            flag = True

        except Exception as e:
            flag = False
            db.rollback()
            print("执行失败->%s" % e)
        finally:
            return flag

    def nonquery(self, sql):#执行非查询类操作
        flag = False
        try:
            db = self.__obtain_connect()
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            flag = True
        except Exception as e:
            flag = False
            db.rollback()
            print("执行失败->%s" % e)
        finally:
            return flag

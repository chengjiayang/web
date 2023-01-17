import logging
logging.basicConfig(level=logging.INFO)
import pymysql
from  saas.saas_program import readConfig
import redis
from redis import  StrictRedis ,ConnectionPool
import pymongo
import bson
from bson.objectid import  ObjectId
import datetime
from dateutil import parser
import re
class db():
    def __init__(self,host=None,account=None,password=None,database=None):
        self.host,self.account,self.password,self.database=(readConfig.get_db()["host"],
                                                            readConfig.get_db()["account"],
                                                            readConfig.get_db()["password"],
                                                            readConfig.get_db()["database"]
                                                            )





        #.ini读取，待写
        self.db=None
        self.cursor=None

        self.redis_host,self.redis_port,self.redis_password=(readConfig.get_redis()["host"],
                                                             readConfig.get_redis()["port"],
                                                             readConfig.get_redis()["password"])

        self.mongoDB_host, self.mongoDB_port, self.mongoDB_user, self.mongoDB_password, self.mongoDB_dbname =(readConfig.get_mongoDB()["host"],
                                                                 readConfig.get_mongoDB()["port"],
                                                                 readConfig.get_mongoDB()["user"],
                                                                 readConfig.get_mongoDB()["password"],
                                                                readConfig.get_mongoDB()["dbname"] )

        # self.mongoDB_host, self.mongoDB_port, self.mongoDB_user, self.mongoDB_password, self.mongoDB_dbname = ('dds-2ze3042dc0825064-pub.mongodb.rds.aliyuncs.com',3717,"saastest","EcaJMNOiU85VzpL3","saas_test")


        # self.host, self.account, self.password, self.database = (
        #     host, account, password, database
        # )


    def connect(self):
        db=pymysql.Connect(host=self.host,user=self.account,password=self.password,database=self.database)
        cursor=db.cursor(cursor=pymysql.cursors.DictCursor)
        self.db=db
        self.cursor=cursor




    def excute(self,sql):
        # logging.info(sql)
        result={}
        if ';'in sql:
            sqls=tuple(sql.split(";"))
            for sql in sqls:
                # logging.info(sql)
                if sql != '':
                    if  sql.lower().startswith("select"):
                        self.database = list(filter(lambda x: '.' in x, sql[sql.lower().find('from'):].split(' ')))[0].split('.')[0]
                    elif sql.lower().startswith("insert"):
                        self.database =list(filter(lambda x: '.' in x, sql[sql.lower().find('into'):].split(' ')))[0].split('.')[0]
                    elif sql.lower().startswith("delete"):
                        self.database = list(filter(lambda x: '.' in x, sql[sql.lower().find('from'):].split(' ')))[0].split('.')[0]
                    elif sql.lower().startswith("update"):
                        self.database = list(filter(lambda x: '.' in x, sql[sql.lower().find('update'):].split(' ')))[0].split('.')[0]
                    self.connect()
                    # logging.info(sql)
                    self.cursor.execute(sql)
                    if sql.lower().startswith("select"):
                        # logging.info(self.cursor.fetchone())
                        result = self.cursor.fetchone()
                    elif sql.lower().startswith("insert"):
                        self.db.commit()
                        # result = self.cursor.lastrowid()
                    elif sql.lower().startswith("delete"):
                        self.db.commit()
                    elif sql.lower().startswith("update"):
                        self.db.commit()
        else:
            if sql.lower().startswith("select"):
                self.database = list(filter(lambda x: '.' in x, sql[sql.lower().find('from'):].split(' ')))[0].split('.')[0]
            elif sql.lower().startswith("insert"):
                self.database = list(filter(lambda x: '.' in x, sql[sql.lower().find('into'):].split(' ')))[0].split('.')[0]
            elif sql.lower().startswith("delete"):
                self.database =list(filter(lambda x: '.' in x, sql[sql.lower().find('from'):].split(' ')))[0].split('.')[0]
            elif sql.lower().startswith("update"):
                self.database =list(filter(lambda x: '.' in x, sql[sql.lower().find('update'):].split(' ')))[0].split('.')[0]
            # logging.info(self.database)
            self.connect()
            # logging.info(sql)
            self.cursor.execute(sql)
            if sql.lower().startswith("select"):
                # logging.info(self.cursor.fetchone())
                result = self.cursor.fetchone()
                # result = self.cursor.fetchall()
            elif sql.lower().startswith("insert"):
                self.db.commit()
                result = self.cursor.lastrowid()
            elif sql.lower().startswith("delete"):
                self.db.commit()
            elif sql.lower().startswith("update"):
                self.db.commit()


        # logging.info(result)
        # logging.info(type(result))
        return result

    def close(self):
        self.cursor.close()
        self.db.close()


    def redis_excute(self,db,method,key,key_type):
        pool=ConnectionPool(host=self.redis_host,port=self.redis_port,db=db,password=self.redis_password,decode_responses=True)
        redis=StrictRedis(connection_pool=pool)


        if method.lower()=='delete':
            redis.delete(key)
        # elif type.lower()=='select':
        #     if key_type.lower()=='set':
        #         value = redis.smembers(key)



        # pipe=r.pipeline()



    def mongoDB_excute(self,table,method,condition,results,condition_value=None,sorts=None):


        client=pymongo.MongoClient(host=self.mongoDB_host,port=int(self.mongoDB_port))

        db=client[self.mongoDB_dbname]
        db.authenticate(self.mongoDB_user, self.mongoDB_password,mechanism='SCRAM-SHA-1')
        # collection=db.user_exam_task
        collection = db[table]

        if method=='update':

            # exam_one=collection.find_one({value["condition"].keys[0]:bson.int64.Int64(value["condition"].values[0])})

            # print(condition)
            # condition_new={}
            # for k,v in condition.items():
            #     if str(v).isdigit():
            #         condition_new[k]=bson.int64.Int64(v)
            #     elif  'time' in k.lower():
            #         condition_new[k] = parser.parse(v)
            #     else:
            #         condition_new[k]=v
            #
            condition_new = {}

            for k, v in condition.items():
                if condition_value:
                    v = re.sub('{[0-9A-Za-z_.:]+}', str(condition_value), v)
                    if str(v).isdigit():
                        condition_new[k] = bson.int64.Int64(v)
                    elif 'time' in k.lower():
                        condition_new[k] = parser.parse(v)
                    else:
                        condition_new[k] = v
                else:
                    if str(v).isdigit():
                        condition_new[k] = bson.int64.Int64(v)
                    elif 'time' in k.lower():
                        condition_new[k] = parser.parse(v)
                    else:
                        condition_new[k] = v
            # print(condition_new)
            target = collection.find_one(condition_new)
            # print(target)
            # target={}
            for k,v in results.items():
                if 'time' in k.lower():
                    target[k]=parser.parse(v)
                else:
                    target[k] =v
            result=collection.update_one(condition_new,{'$set':target})
            target = collection.find_one(condition_new)
            # print(target)
            result=None
        elif method=='select':
            condition_new = {}

            for k, v in condition.items():
                if condition_value:
                    v = re.sub('{[0-9A-Za-z_.:]+}', str(condition_value), v)
                    if str(v).isdigit():
                        condition_new[k] = bson.int64.Int64(v)
                    elif 'time' in k.lower():
                        condition_new[k] = parser.parse(v)
                    else:
                        condition_new[k] = v
                else:
                    if str(v).isdigit():
                        condition_new[k] = bson.int64.Int64(v)
                    elif 'time' in k.lower():
                        condition_new[k] = parser.parse(v)
                    else:
                        condition_new[k] = v
            # print(condition_new)


            target ={}
            target["_id"] = 0
            for k in list(results.keys()):
                target[k]=1
            if not sorts:
                result = collection.find_one(condition_new, target)
            else:
                # print(sorts)
                # print(type(sorts))
                result=collection.find(condition_new,target).sort(list(sorts.keys())[0],list(sorts.values())[0])[0]
            # print(condition_new, target)
            # print(result)
            if result:
                result_last = {}
                for r_k in list(results.keys()):
                    if '.' in r_k:
                        b = results[r_k]
                        r_k = r_k.split('.')
                        # print(r_k)
                        a = result
                        for i in range(0, len(r_k)):
                            a = a[r_k[i]]
                            if type(a) == list:
                                a = a[0]
                            # print(a)
                            result_last[b] = a
                    else:
                        result_last[results[r_k]] = result[r_k]

                result = result_last
            else:
                logging.info("MongoDB查询结果为空")











        # target=collection.find_one()
        # target={"candidates": bson.int64.Int64("1362967951648911360"), "companyId": bson.int64.Int64("1320634660929146880"), "deleted": False ,"biz": "NORMAL"}
        # print(str(results)+'结果'+str(result))
        # result=
        return result
























import json
from channels.generic.websocket import WebsocketConsumer
from myweb import settings
import time
from .tasks import runallcase,runallcases_by_one_thread
from celery.app.control import  Control
from myweb.celery import  app
from celery.result import AsyncResult
import os
class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()




    def disconnect(self, close_code):
        pass

    def websocket_receive(self, text_data):
        # print(text_data)
        # self.task_id=None
        # if text_data.get("text")=='start':
        for filea in os.listdir(r'./saas/saas_program/testFile/DownloadFiles'):
            file=os.path.join(r'./saas/saas_program/testFile/DownloadFiles', filea)
            os.remove(file)

        results = runallcase.delay()
        # self.task_id = results.id
        # print(self.task_id)

        # settings.log_path
        with open(r"D:\myweb\logs\myweb.log", 'r', encoding='UTF-8') as f:
            log_length = len(f.readlines())
            # time.sleep(1)

        # while not results.ready():
        #     with open(r"D:\myweb\logs\myweb.log", 'r', encoding='UTF-8') as f:
        #         contents = f.readlines()
        #         length_tmp = len(contents)
        #     if length_tmp != log_length:
        #         for i in range(log_length, length_tmp):
        #             self.send(contents[i])
        #         log_length = length_tmp
        #         time.sleep(0.1)
        # self.send("接口执行完成")

        while not results.ready():
            with open(r"D:\myweb\logs\myweb.log", 'r', encoding='UTF-8') as f:
                contents = f.readlines()
                length_tmp = len(contents)
            if length_tmp == log_length:
                time.sleep(0.001)
                continue
            else:
                for i in range(log_length, length_tmp):
                    self.send(contents[i])
                log_length = length_tmp
                time.sleep(0.1)

        self.send("接口执行完成")


        # if text_data.get("text")=='stop':
        #     print('stop')
        #     celery_control=Control(app=app)
        #     celery_control.revoke(self.task_id, terminate=True)
            # AsyncResult(self.task_id,app=app).revoke()









        # with open(r"D:\myweb\logs\info-2021-12-13.log", 'r', encoding='UTF-8') as f:
        #     contents = f.readlines()
        #     for i in range(len(contents)):
        #         self.send(contents[i].encode('utf-8'))

        #  回复
        # message = text_data['text']
        #
        # self.send(
        #      '123'
        # )



class ChatConsumer_one_thread(WebsocketConsumer):
    def connect(self):
        self.accept()



    def disconnect(self, close_code):
        pass

    def websocket_receive(self, text_data):

        results=runallcases_by_one_thread.delay()





        # settings.log_path
        with open(r"D:\myweb\logs\myweb.log", 'r', encoding='UTF-8') as f:
            log_length = len(f.readlines())
            # time.sleep(1)

        # while not results.ready():
        #     with open(r"D:\myweb\logs\myweb.log", 'r', encoding='UTF-8') as f:
        #         contents = f.readlines()
        #         length_tmp = len(contents)
        #     if length_tmp != log_length:
        #         for i in range(log_length, length_tmp):
        #             self.send(contents[i])
        #         log_length = length_tmp
        #         time.sleep(0.1)
        # self.send("接口执行完成")



        while  not results.ready():
            with open(r"D:\myweb\logs\myweb.log", 'r', encoding='UTF-8') as f:
                contents = f.readlines()
                length_tmp = len(contents)
            if length_tmp==log_length:
                time.sleep(0.1)
                continue
            else:
                for i in range(log_length, length_tmp):
                    self.send(contents[i])
                log_length = length_tmp
                time.sleep(0.1)

        self.send("接口执行完成")




        # with open(r"D:\myweb\logs\info-2021-12-13.log", 'r', encoding='UTF-8') as f:
        #     contents = f.readlines()
        #     for i in range(len(contents)):
        #         self.send(contents[i].encode('utf-8'))

        #  回复
        # message = text_data['text']
        #
        # self.send(
        #      '123'
        # )


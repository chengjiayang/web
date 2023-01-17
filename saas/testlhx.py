import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from . import tasks

COMMANDS = {
    'help': {
        'help': '命令帮助信息.',
    },
    'add': {
        'args': 2,
        'help': '计算两个数之和, 例子: `add 12 32`.',
        'task': 'add'
    },
    'search': {
        'args': 1,
        'help': '通过名字查找诗人介绍，例子: `search 李白`.',
        'task': 'search'
    },
}


class BotConsumer(WebsocketConsumer):
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        response_message = '请输入`help`获取命令帮助信息。'
        message_parts = message.split()
        if message_parts:
            command = message_parts[0].lower()
            if command == 'help':
                response_message = '支持的命令有:\n' + '\n'.join(
                    [f'{command} - {params["help"]} ' for command, params in COMMANDS.items()])
            elif command in COMMANDS:
                if len(message_parts[1:]) != COMMANDS[command]['args']:
                    response_message = f'命令`{command}`参数错误，请重新输入.'
                else:
                    getattr(tasks, COMMANDS[command]['task']).delay(self.channel_name, *message_parts[1:])
                    response_message = f'收到`{message}`任务.'

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'chat.message',
                'message': response_message
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': f'[机器人]: {message}'
        }))




from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from parsel import Selector
import requests

channel_layer = get_channel_layer()


@shared_task
def add(channel_name, x, y):
    message = '{}+{}={}'.format(x, y, int(x) + int(y))
    async_to_sync(channel_layer.send)(channel_name, {"type": "chat.message", "message": message})
    print(message)


@shared_task
def search(channel_name, name):
    spider = PoemSpider(name)
    result = spider.parse_page()
    async_to_sync(channel_layer.send)(channel_name, {"type": "chat.message", "message": str(result)})
    print(result)


class PoemSpider(object):
    def __init__(self, keyword):
        self.keyword = keyword
        self.url = "https://so.gushiwen.cn/search.aspx"

    def parse_page(self):
        params = {'value': self.keyword}
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            # 创建Selector类实例
            selector = Selector(response.text)
            # 采用xpath选择器提取诗人介绍
            intro = selector.xpath('//textarea[starts-with(@id,"txtareAuthor")]/text()').get()
            print("{}介绍:{}".format(self.keyword, intro))
            if intro:
                return intro

        print("请求失败 status:{}".format(response.status_code))
        return "未找到诗人介绍。"
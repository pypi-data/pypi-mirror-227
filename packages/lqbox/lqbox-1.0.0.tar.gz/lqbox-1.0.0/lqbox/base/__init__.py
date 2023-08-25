# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py
@Date    : 2023/8/25 10:58:45
@Author  : zhchen
@Desc    : 
"""
import base64

import requests


class BaseBox:
    base_url = None

    def __init__(self, cookies):
        self.cookies = cookies
        self.check()

    def check(self):
        if not self.base_url:
            raise ValueError("base_url is None")

        decoded_bytes = base64.b64decode(self.base_url)
        decoded_string = decoded_bytes.decode('utf-8')
        self.base_url = decoded_string

    def request(self, method, url, **kwargs):
        if kwargs.get('headers') is None:
            kwargs['headers'] = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/78.0.3904.70 Safari/537.36'
            }
        if kwargs.get("cookies") is None:
            kwargs['cookies'] = self.cookies
        return requests.request(method, url, **kwargs)

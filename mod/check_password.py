#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-29 22:59:56
# @Author  : yml_bright@163.com

from config import API_URL, CONNECT_TIME_OUT
from tornado.httpclient import HTTPRequest, HTTPClient, HTTPError
import IPython
import urllib

def check_password(cardnum, password):
    data = {
        'cardnum': cardnum,
        'password': password,
    }
    try:
        client = HTTPClient()
        request = HTTPRequest(
            API_URL+'auth',
            method='POST',
            body=urllib.urlencode(data),
            request_timeout=CONNECT_TIME_OUT)
        response = client.fetch(request)
        return True
    except HTTPError:
        pass
    return False

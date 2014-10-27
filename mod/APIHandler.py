#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 16:31:03
# @Author  : yml_bright@163.com

import urllib
import tornado.web
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from sqlalchemy.orm.exc import NoResultFound
from models.user import User
from models.privilege import Privilege
from models.app import Application
from config import *

class APIHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    @property
    def unitsmap(self):
        return {
            'srtp': self.srtp,
            'term': self.term,
            'sidebar': self.sidebar,
            'curriculum': self.curriculum,
            'gpa': self.gpa,
            'pe': self.pe,
            'simsimi': self.simsimi,
            'nic': self.nic,
            'card': self.card
        }

    def get(self, API):
        self.write('<form method="post"><input type="text" name="uuid"><input type="submit" name="submit"></form>')
        self.write('Herald Auth.')
        self.finish()

    @tornado.web.asynchronous
    def post(self, API):
        uuid = self.get_argument('uuid')
        if not uuid:
            self.write('param lack')

        try:
            pri = self.db.query(Privilege).filter(
                Privilege.uuid == uuid).one()
            app = self.db.query(Application).filter(
                Application.aid == pri.aid).one()
            user = self.db.query(User).filter(
                User.cardnum == pri.cardnum).one()
            if app.state == '1':
                try:
                    self.unitsmap[API](user)
                except KeyError:
                    self.write('api error')
        except NoResultFound:
            self.write('not auth')
        self.finish()
        

    @tornado.gen.engine
    def api_post(self, url, data):
        client = AsyncHTTPClient()
        request = HTTPRequest(
            url, body=urllib.urlencode(data),
            method='POST',
            request_timeout=CONNECT_TIME_OUT)
        response = yield tornado.gen.Task(client.fetch, request)
        body = response.body
        if body:
            self.write(body)
        else:
            self.write('time out')
        self.finish()

    def srtp(self, user):
        self.api_post(API_URL+'srtp', {'number':user.cardnum})

    def term(self, user):
        self.api_post(API_URL+'term', '')

    def sidebar(self, user):
        self.api_post(API_URL+'sidebar', {'cardnum':user.cardnum, 'term':TERM})

    def curriculum(self, user):
        self.api_post(API_URL+'sidebar', {'cardnum':user.cardnum, 'term':TERM})

    def gpa(self, user):
        self.api_post(API_URL+'gpa', {'username':user.cardnum, 'password':user.password})

    def pe(self, user):
        self.api_post(API_URL+'gpa', {'cardnum':user.cardnum, 'pwd':user.pe_password})

    def simsimi(self, user):
        self.api_post(API_URL+'simsimi', {'msg':self.get_argument('msg', default='xxxx')})

    def nic(self, user):
        self.api_post(API_URL+'nic', '')

    def card(self, user):
        self.api_post(API_URL+'card', '')

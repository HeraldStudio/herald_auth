#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 16:31:03
# @Author  : yml_bright@163.com

import urllib
import tornado.web
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPError
from sqlalchemy.orm.exc import NoResultFound
from models.user import User
from models.privilege import Privilege
from models.app import Application
from config import *
import time

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
            'card': self.card,
            'lecture':self.lecture,
        }

    def get(self, API):
        self.write('<form method="post"><input type="text" name="uuid"><input type="submit" name="submit"></form>')
        self.write('Herald Auth.')
        self.finish()

    @tornado.web.asynchronous
    def post(self, API):
        uuid = self.get_argument('uuid')
        #appid = self.get_argument('appid')
        if not (uuid):
            raise tornado.web.HTTPError(400)

        try:
            pri = self.db.query(Privilege).filter(
                Privilege.uuid == uuid).one()
            app = self.db.query(Application).filter(
                Application.aid == pri.aid).one()
            user = self.db.query(User).filter(
                User.cardnum == pri.cardnum).one()
            if app.state == '1' and user.state == 1:
                try:
                    self.unitsmap[API](user)
                    pri.last_access = int(time.time())
                    pri.access_count += 1
                    self.db.add(pri)
                    self.db.commit()
                except KeyError:
                    raise tornado.web.HTTPError(400)
            elif app.state == '2':
                if app.access_left <=0:
                    self.write('access denied')
                    self.finish()
                    self.db.close()
                    return
                app.access_left -= 1
                self.db.add(app)
                self.db.commit() 
                try:
                    self.unitsmap[API](user)
                    pri.last_access = int(time.time())
                    pri.access_count += 1
                    self.db.add(pri)
                    self.db.commit()
                except KeyError:
                    raise tornado.web.HTTPError(400)
            else:
                self.db.close()
                raise tornado.web.HTTPError(401)
        except NoResultFound:
            self.db.close()
            raise tornado.web.HTTPError(401) 

    @tornado.gen.engine
    def api_post(self, url, data):
        try:
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
            self.db.close()
            self.finish()
        except HTTPError:
            self.write('services are unreachable')
            self.db.close()
            self.finish()

    def srtp(self, user):
        self.api_post(API_URL+'srtp', {'number':user.number})

    def term(self, user):
        self.api_post(API_URL+'term', '')

    def sidebar(self, user):
        self.api_post(API_URL+'sidebar', {'cardnum':user.cardnum, 'term':TERM})

    def curriculum(self, user):
        self.api_post(API_URL+'curriculum', {'cardnum':user.cardnum, 'term':TERM})

    def gpa(self, user):
        self.api_post(API_URL+'gpa', {'username':user.cardnum, 'password':user.password})

    def pe(self, user):
        if not user.pe_password:
            pwd = user.cardnum
        else:
            pwd = user.pe_password
        self.api_post(API_URL+'pe', {'cardnum':user.cardnum, 'pwd':pwd})

    def simsimi(self, user):
        self.api_post(API_URL+'simsimi', {'msg':self.get_argument('msg', default='xxxx')})

    def nic(self, user):
        self.api_post(API_URL+'nic', {'cardnum':user.cardnum, 'password':user.password})

    def card(self, user):
        self.api_post(API_URL+'card', {'cardnum':user.cardnum, 'password':user.password, 'timedelta':self.get_argument('timedelta', default='0')})

    def lecture(self, user):
        self.api_post(API_URL+'lecture', {'cardnum':user.cardnum, 'password':user.password})

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 16:31:03
# @Author  : yml_bright@163.com

import sys
import time
import urllib

import tornado.web
from mod.models.app import Application
from mod.models.privilege import Privilege
from sqlalchemy.orm.exc import NoResultFound
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPError

from config import *
from mod.models.user import User

reload(sys)
sys.setdefaultencoding('utf8')


class APIHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def unitsmap(self):
        allAPI = {
            'srtp': self.srtp,
            'term': self.term,
            'sidebar': self.sidebar,
            'curriculum': self.curriculum,
            'gpa': self.gpa,
            'pe': self.pe,
            'pedetail': self.pedetail,
            'nic': self.nic,
            'card': self.card,
            'lecture': self.lecture,
            'library': self.library,
            'library_hot': self.library_hot,
            'renew': self.renew,
            'search': self.search,
            'pc': self.pc,
            'jwc': self.jwc,
            'schoolbus': self.schoolbus,
            'newbus': self.newbus,
            'week': self.week,
            'phylab': self.phylab,
            'emptyroom': self.emptyroom,
           # 'newemptyroom': self.newemptyroom,
            'lecturenotice': self.lecturenotice,
            'room': self.room,
            'yuyue': self.yuyue,
            'exam': self.exam,
            'tice': self.tice,
            'user': self.user
        }

        mapTable = {
            '1': allAPI,
            '2': allAPI,
            'a': {
                'week': self.week,
                'user': self.user
            }
        }

        return mapTable

    def get(self, API):
        raise tornado.web.HTTPError(404)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self, API):
        self.uuid = self.get_argument('uuid')
        # appid = self.get_argument('appid')
        if not (self.uuid):
            raise tornado.web.HTTPError(400)

        try:
            pri = self.db.query(Privilege).filter(
                Privilege.uuid == self.uuid).one()
            app = self.db.query(Application).filter(
                Application.aid == pri.aid).one()
            user = self.db.query(User).filter(
                User.cardnum == pri.cardnum).one()
            # check user state
            if user.state == 0:
                self.user_locked(user)

            # change app api access left
            if app.state == '2' or 64 < ord(app.state) < 91:
                if app.access_left <= 0:
                    self.api_deny()
                else:
                    app.access_left -= 1
                    self.db.add(app)
                    self.db.commit()

                    # call api
            try:
                self.unitsmap[app.state.lower()][API](user)
                pri.last_access = int(time.time())
                pri.access_count += 1
                self.db.add(pri)
                self.db.commit()
            except KeyError:
                self.api_error(user)

        except NoResultFound:
            raise tornado.web.HTTPError(401) 

    def api_error(self, user):
        raise tornado.web.HTTPError(400)

    def api_deny(self, user):
        raise tornado.web.HTTPError(404)

    def user_locked(self, user):
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
                raise tornado.web.HTTPError(408)  # time out
            self.finish()
        except HTTPError:
            self.write('services are unreachable')
            self.finish()

    def on_finish(self):
        self.db.close()

    @tornado.gen.engine
    def srtp(self, user):
        schoolnum = self.get_argument('schoolnum', default=None)
        user.number = schoolnum if schoolnum else user.number
        self.api_post(API_URL + 'srtp', {'number': user.number})

    @tornado.gen.engine
    def term(self, user):
        self.api_post(API_URL + 'term', '')

    @tornado.gen.engine
    def sidebar(self, user):
        self.api_post(API_URL + 'sidebar', {'cardnum': user.cardnum, 'term': TERM})

    @tornado.gen.engine
    def curriculum(self, user):
        curriculumTerm = self.get_argument('term', default=None)
        term = ""
        if curriculumTerm:
            term = curriculumTerm
        else:
            term = TERM
        date = self.get_argument('date', default=-1)
        self.api_post(API_URL + 'curriculum', {'cardnum': user.cardnum, 'term': term, 'date': date})

    @tornado.gen.engine
    def gpa(self, user):
        self.api_post(API_URL + 'gpa', {'username': user.cardnum, 'password': user.password})

    @tornado.gen.engine
    def pe(self, user):
        if not user.pe_password:
            pwd = user.cardnum
        else:
            pwd = user.pe_password
        self.api_post(API_URL + 'pe', {'cardnum': user.cardnum, 'pwd': pwd})

    def pedetail(self, user):
        self.api_post(API_URL + 'pedetail', {'cardnum': user.cardnum, 'password': user.password})

    @tornado.gen.engine
    def pedetail(self,user):
        self.api_post(API_URL+'pedetail', {'cardnum':user.cardnum, 'password':user.password})

    @tornado.gen.engine
    def nic(self, user):
        self.api_post(API_URL + 'nic', {'cardnum': user.cardnum, 'password': user.password})

    @tornado.gen.engine
    def card(self, user):
        self.api_post(API_URL + 'card', {'cardnum': user.cardnum, 'password': user.password,
                                         'timedelta': self.get_argument('timedelta', default='0')})

    @tornado.gen.engine
    def lecture(self, user):
        self.api_post(API_URL + 'lecture', {'cardnum': user.cardnum, 'password': user.password})

    @tornado.gen.engine
    def library(self, user):
        if not user.lib_username:
            self.api_post(API_URL + 'library', {'cardnum': user.cardnum, 'password': user.cardnum})
        else:
            self.api_post(API_URL + 'library', {'cardnum': user.lib_username, 'password': user.lib_password})

    def library_hot(self, user):
        self.api_post(API_URL + 'library_hot', {})

    @tornado.gen.engine
    def renew(self, user):
        self.api_post(API_URL + 'renew', {'cardnum': user.lib_username, 'password': user.lib_password,
                                          'barcode': self.get_argument('barcode')})

    @tornado.gen.engine
    def search(self, user):
        self.api_post(API_URL + 'search', {'book': self.get_argument('book')})

    @tornado.gen.engine
    def pc(self, user):
        self.api_post(API_URL + 'pc', '')

    @tornado.gen.engine
    def jwc(self, user):
        self.api_post(API_URL + 'jwc', '')

    @tornado.gen.engine
    def schoolbus(self, user):
        self.api_post(API_URL + 'schoolbus', '')

    @tornado.gen.engine
    def newbus(self, user):
        self.api_post(API_URL+'newbus', '')
    
    @tornado.gen.engine
    def week(self, user):
        self.api_post(API_URL + 'week', '')

    @tornado.gen.engine
    def phylab(self, user):
        self.api_post(API_URL + 'phylab', {'number': user.cardnum, 'password': user.password, 'term': TERM})

    @tornado.gen.engine
    def lecturenotice(self, user):
        self.api_post(API_URL + 'lecturenotice', '')

    def room(self, user):
        self.api_post(API_URL + 'room', {'number': user.cardnum, 'password': user.password})

    def yuyue(self, user):
        key = ['method', 'itemId', 'id', 'dayInfo', 'time', 'cardNo', 'orderVO.useMode', 'orderVO.useTime',
               'orderVO.itemId', 'orderVO.phone', 'useUserIds', 'orderVO.remark']
        data = {'cardnum': user.cardnum, 'password': user.password}
        for i in key:
            value = self.get_argument(i, default=None)
            if value:
                data[i] = value
        self.api_post(API_URL + 'yuyue', data)

    def exam(self, user):
        self.api_post(API_URL + 'exam', {'cardnum': user.cardnum, 'password': user.password})

    def tice(self, user):
        self.api_post(API_URL + 'tice', {'cardnum': user.cardnum, 'password': user.password})

    @tornado.gen.engine
    def yuyue(self,user):
	key = ['method','itemId','id','dayInfo','time','cardNo','orderVO.useMode','orderVO.useTime','orderVO.itemId','orderVO.phone','useUserIds','orderVO.remark']
        data = {'cardnum':user.cardnum, 'password':user.password}
        for i in key:
            value = self.get_argument(i,default=None)
            if value:
                data[i] = value
        self.api_post(API_URL+'yuyue',data)

    @tornado.gen.engine
    def exam(self,user):
        self.api_post(API_URL+'exam',{'cardnum':user.cardnum, 'password':user.password})

    @tornado.gen.engine
    def tice(self,user):
        self.api_post(API_URL+'tice',{'cardnum':user.cardnum, 'password':user.password})

    @tornado.gen.engine
    def user(self, user):
        self.api_post(API_URL + 'user', {'number': user.cardnum, 'password': user.password})

    def emptyroom(self, user):
        url = self.get_argument('url', None)
        method = self.get_argument('method', None)
        data = self.get_argument('data', None)
        self.api_post(API_URL + 'query', {'url': url, 'method': method, 'data': data})

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
import sys  
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
            'pedetail':self.pedetail,
            'simsimi': self.simsimi,
            'nic': self.nic,
            'card': self.card,
            'lecture': self.lecture,
            'library': self.library,
            'library_hot':self.library_hot,
            'renew': self.renew,
            'search': self.search,
            'pc': self.pc,
            'jwc': self.jwc,
            'schoolbus': self.schoolbus,
            'week': self.week,
            'phylab': self.phylab,
            'emptyroom': self.emptyroom,
            'lecturenotice': self.lecturenotice,
            'room':self.room,
            'yuyue':self.yuyue,
            'exam':self.exam,
            'tice':self.tice,
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
        self.render('index.htm',compress_whitespace=False)
        #self.finish()

    @tornado.web.asynchronous
    def post(self, API):
        self.uuid = self.get_argument('uuid')
        #appid = self.get_argument('appid')
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
            if app.state == '2' or 64<ord(app.state)<91:    
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
    @tornado.web.asynchronous
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
                raise tornado.web.HTTPError(408) # time out
            self.finish()
        except HTTPError:
            self.write('services are unreachable')
            self.finish()

    def on_finish(self):
        self.db.close()

    def srtp(self, user):
        schoolnum = self.get_argument('schoolnum',default=None)
        user.number = schoolnum if schoolnum else user.number
        self.api_post(API_URL+'srtp', {'number':user.number})

    def term(self, user):
        self.api_post(API_URL+'term', '')

    def sidebar(self, user):
        self.api_post(API_URL+'sidebar', {'cardnum':user.cardnum, 'term':TERM})

    def curriculum(self, user):
        curriculumTerm = self.get_argument('term',default=None)
        term = ""
        if curriculumTerm:
            term = curriculumTerm
        else:
            term = TERM
        date = self.get_argument('date',default=-1)
        self.api_post(API_URL+'curriculum', {'cardnum':user.cardnum, 'term':term,'date':date})

    def gpa(self, user):
        self.api_post(API_URL+'gpa', {'username':user.cardnum, 'password':user.password})

    def pe(self, user):
        if not user.pe_password:
            pwd = user.cardnum
        else:
            pwd = user.pe_password
        self.api_post(API_URL+'pe', {'cardnum':user.cardnum, 'pwd':pwd})
    def pedetail(self,user):
        self.api_post(API_URL+'pedetail', {'cardnum':user.cardnum, 'password':user.password})
    def simsimi(self, user):
        self.api_post(API_URL+'simsimi', {'msg':self.get_argument('msg', default='xxxx'), 'uid': self.uuid})

    def nic(self, user):
        self.api_post(API_URL+'nic', {'cardnum':user.cardnum, 'password':user.password})

    def card(self, user):
        self.api_post(API_URL+'card', {'cardnum':user.cardnum, 'password':user.password, 'timedelta':self.get_argument('timedelta', default='0')})

    def lecture(self, user):
        self.api_post(API_URL+'lecture', {'cardnum':user.cardnum, 'password':user.password})

    def library(self, user):
        self.api_post(API_URL+'library', {'cardnum':user.lib_username, 'password':user.lib_password})
    def library_hot(self,user):
        self.api_post(API_URL+'library_hot',{})

    def renew(self, user):
        self.api_post(API_URL+'renew', {'cardnum':user.lib_username, 'password':user.lib_password, 'barcode':self.get_argument('barcode')})

    def search(self, user):
        self.api_post(API_URL+'search', {'book':self.get_argument('book')})

    def pc(self, user):
        self.api_post(API_URL+'pc', '')

    def jwc(self, user):
        self.api_post(API_URL+'jwc', '')

    def schoolbus(self, user):
        self.api_post(API_URL+'schoolbus', '')

    def week(self, user):
        self.api_post(API_URL+'week', '')

    def phylab(self, user):
        self.api_post(API_URL+'phylab', {'number':user.cardnum, 'password':user.password, 'term':TERM})

    def lecturenotice(self, user):
        self.api_post(API_URL+'lecturenotice', '')

    def room(self,user):
        self.api_post(API_URL+'room',{'number':user.cardnum, 'password':user.password})
    def yuyue(self,user):
        key = ['method','itemId','dayInfo','time','cardNo','orderVO.useMode','orderVO.useTime','orderVO.itemId','orderVO.phone','useUserIds']
        data = {'cardnum':user.cardnum, 'password':user.password}
        for i in key:
            value = self.get_argument(i,default=None)
            if value:
                data[i] = value
        self.api_post(API_URL+'yuyue',data)
    def exam(self,user):
        self.api_post(API_URL+'exam',{'cardnum':user.cardnum, 'password':user.password})
    def tice(self,user):
        self.api_post(API_URL+'tice',{'cardnum':user.cardnum, 'password':user.password})

    def user(self, user):
        self.api_post(API_URL+'user', {'number':user.cardnum, 'password':user.password})

    def emptyroom(self, user):
        url = self.get_argument('url',None)
        method = self.get_argument('method',None)
        data = self.get_argument('data',None)
        self.api_post(API_URL+'query',{'url':url,'method':method,'data':data})
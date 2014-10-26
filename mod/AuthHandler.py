#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 12:55:44
# @Author  : yml_bright@163.com

import tornado.web
from sqlalchemy.sql import and_
from sqlalchemy.orm.exc import NoResultFound
from time import time
from hashlib import sha1
from models.user import User
from models.privilege import Privilege
from models.app import Application

class AuthHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('<form method="post"><input type="text" name="user"><input type="test" name="password"><input type="text" name="appid" value="123"><input type="submit" name="submit"></form>')
        self.write('Herald API')
        self.finish()

    def post(self):
        user = self.get_argument('user')
        pwd = self.get_argument('password')
        appid = self.get_argument('appid') 
        if not (user or pwd or appid):
            raise tornado.web.HTTPError(400)

        try:
            u = self.db.query(User).filter(
                and_(User.cardnum == user, User.password == pwd)).one()
            app = self.db.query(Application).filter(
                Application.uuid == appid).one()
            self.write(self.get_token(u,app))
        except NoResultFound:
            raise tornado.web.HTTPError(401)
        self.finish()

    def get_token(self, user, app):
        try:
            pri = self.db.query(Privilege).filter(
                and_(Privilege.cardnum == user.cardnum, Privilege.aid == app.aid)).one()
            return pri.uuid
        except NoResultFound:
            try:
                while 1:
                    token = sha1(user.cardnum+str(time())+'HearldAuth').hexdigest()
                    r = self.db.query(Privilege).filter(
                        Privilege.uuid == token).count()
                    if r == 0:
                        break
                item = Privilege(cardnum=user.cardnum,
                                aid=app.aid,
                                uuid=token)
                self.db.add(item)
                self.db.commit()
            except:
                raise tornado.web.HTTPError(401)
            return token
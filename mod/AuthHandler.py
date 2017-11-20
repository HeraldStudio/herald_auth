#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 12:55:44
# @Author  : yml_bright@163.com

from hashlib import sha1
from time import time

import tornado.web
from mod.models.app import Application
from mod.models.privilege import Privilege
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import and_

from check_password import check_password
from mod.models.user import User


class AuthHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        # self.write('<form method="post"><input type="text" name="user"><input type="test" name="password"><input type="text" name="appid" value="123"><input type="submit" name="submit"></form>')
        self.write('Herald Auth.')
        self.finish()

    def post(self):
        user = self.get_argument('user')
        pwd = self.get_argument('password')
        appid = self.get_argument('appid') 
        if not (user and pwd and appid):
            raise tornado.web.HTTPError(401)
            self.finish()

        if not self.user_check(user, pwd):
            raise tornado.web.HTTPError(401)
            self.finish()
        
        try:
            app = self.db.query(Application).filter(
                Application.uuid == appid).one()
            self.write(self.get_token(user, app))
            self.finish()
        except NoResultFound:
            raise tornado.web.HTTPError(400)
            self.finish()

    def user_check(self, user, pwd):
        try:
            u = self.db.query(User).filter(
                User.cardnum == user).one()
            if check_password(user, pwd):
                u.password = pwd
                self.db.add(u)
                self.db.commit()
                return True
            return False
        except NoResultFound:
            if check_password(user, pwd):
                u = User(cardnum=user, password=pwd, state=1)
                self.db.add(u)
                self.db.commit()
                return True
            return False

    def get_token(self, user, app):
        try:
            pri = self.db.query(Privilege).filter(
                and_(Privilege.cardnum == user, Privilege.aid == app.aid)).one()
            return pri.uuid
        except NoResultFound:
            try:
                while 1:
                    token = sha1(user+str(time())+'HearldAuth').hexdigest()
                    r = self.db.query(Privilege).filter(
                        Privilege.uuid == token).count()
                    if r == 0:
                        break
                item = Privilege(cardnum=user,
                                aid=app.aid,
                                uuid=token)
                self.db.add(item)
                self.db.commit()
            except:
                raise tornado.web.HTTPError(401)
            return token

    def on_finish(self):
        self.db.close()

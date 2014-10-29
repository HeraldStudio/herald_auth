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
from check_password import check_password

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
        if not (user and pwd and appid):
            raise tornado.web.HTTPError(400)

        if not self.user_check(user, pwd):
            raise tornado.web.HTTPError(401)

        try:
            app = self.db.query(Application).filter(
                Application.uuid == appid).one()
            self.write(self.get_token(u,app))
        except NoResultFound:
            raise tornado.web.HTTPError(400)

    def user_check(self, user, pwd):
        try:
            u = self.db.query(User).filter(
                User.cardnum == user).one()
            if u.password != pwd:
                if check_password(user, pwd):
                    u.password = pwd
                    self.db.add(u)
                    self.db.commit()
                    return True
                return False
            return True           
        except NoResultFound:
            if check_password(user, pwd):
                u = User(cardnum=user, password=pwd)
                self.db.add(u)
                self.db.commit()
                return True
            return False

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
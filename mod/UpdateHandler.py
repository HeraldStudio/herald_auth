#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 16:10:46
# @Author  : yml_bright@163.com

import tornado.web
from sqlalchemy.sql import and_
from sqlalchemy.orm.exc import NoResultFound
from models.user import User
from models.privilege import Privilege
from models.app import Application

class UpdateHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('<form method="post"><input type="text" name="appid"><input type="text" name="uuid"><input type="submit" name="submit"></form>')
        self.write('Herald Auth.')
        self.finish()

    def post(self):
        cardnum = self.get_argument('cardnum', default='')
        number = self.get_argument('number', default='')
        password = self.get_argument('password', default='')
        pe_password = self.get_argument('pe_password', default='')
        lib_username = self.get_argument('lib_username', default='')
        lib_password = self.get_argument('lib_password', default='')
        card_query_pwd = self.get_argument('card_query_pwd', default='')
        card_consume_pwd = self.get_argument('card_consume_pwd', default='')

        try:
            app = self.db.query(Application).filter(
                Application.uuid == appid).one()
            pri = self.db.query(Privilege).filter(
                and_(Privilege.uuid == uuid, Privilege.aid == app.aid)).one()
            self.write('OK')
        except NoResultFound:
            raise tornado.web.HTTPError(401)
        self.finish()
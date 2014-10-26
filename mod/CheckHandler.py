#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 15:40:22
# @Author  : yml_bright@163.com

import tornado.web
from sqlalchemy.sql import and_
from sqlalchemy.orm.exc import NoResultFound
from models.privilege import Privilege
from models.app import Application

class CheckHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('<form method="post"><input type="text" name="appid"><input type="text" name="uuid"><input type="submit" name="submit"></form>')
        self.write('Herald Auth.')
        self.finish()

    def post(self):
        appid = self.get_argument('appid')
        uuid = self.get_argument('uuid')
        if not (appid or uuid):
            raise tornado.web.HTTPError(400)

        try:
            app = self.db.query(Application).filter(
                Application.uuid == appid).one()
            pri = self.db.query(Privilege).filter(
                and_(Privilege.uuid == uuid, Privilege.aid == app.aid)).one()
            self.write('OK')
        except NoResultFound:
            raise tornado.web.HTTPError(401)
        self.finish()
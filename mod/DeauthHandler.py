#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 15:20:19
# @Author  : yml_bright@163.com

import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from models.privilege import Privilege
from models.app import Application

class DeauthHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('<form method="post"><input type="text" name="uuid"><input type="text" name="appid" value="123"><input type="submit" name="submit"></form>')
        self.write('Herald Auth.')
        self.finish()

    def post(self):
        uuid = self.get_argument('uuid')
        appid = self.get_argument('appid')
        if not uuid:
            raise tornado.web.HTTPError(400)

        try:
            pri = self.db.query(Privilege).filter(
                Privilege.uuid == uuid).one()
            app = self.db.query(Application).filter(
                Application.aid == pri.aid).one()
            if app.uuid == appid:
                self.db.delete(pri)
                self.db.commit()
                self.write('OK')
            else:
                raise tornado.web.HTTPError(401)
        except NoResultFound:
            raise tornado.web.HTTPError(400)
        self.finish()

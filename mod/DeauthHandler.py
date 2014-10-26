#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2014-10-26 15:20:19
# @Author  : yml_bright@163.com

import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from models.privilege import Privilege

class DeauthHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write('<form method="post"><input type="text" name="uuid"><input type="submit" name="submit"></form>')
        self.write('Herald Auth.')
        self.finish()

    def post(self):
        uuid = self.get_argument('uuid')
        if not uuid:
            raise tornado.web.HTTPError(400)

        try:
            pri = self.db.query(Privilege).filter(
                Privilege.uuid == uuid).one()
            self.db.delete(pri)
            self.db.commit()
            self.write('OK')
        except NoResultFound:
            raise tornado.web.HTTPError(400)
        self.finish()

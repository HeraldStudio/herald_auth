#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        #uuid和appid两项用以在数据库中比对确认修改用户信息的权限
        #其他项留空则不修改原数据
        self.write('''<form method="post">
                        <p>凭据信息</p>
                        <p>uuid            <input type="text" name="uuid"></p>
                        <p>appid           <input type="text" name="appid"></p>
                        <HR>
                        <p>更新用户信息（留空不变动）</p>
                        <p>cardnum(不可变动)</p>
                        <p>number          <input type="text" name="number"></p>
                        <p>password        <input type="password" name="password"></p>
                        <p>pe_password     <input type="password" name="pe_password"></p>
                        <p>lib_username    <input type="text" name="lib_username"></p>
                        <p>lib_password    <input type="password" name="lib_password"></p>
                        <p>card_query_pwd  <input type="password" name="card_query_pwd"></p>
                        <p>card_consume_pwd<input type="password" name="card_consume_pwd"></p>
                        <p><input type="submit" name="submit"></p>
                    </form>''')
        self.write('Herald Auth.')
        self.finish()

    def post(self):
        uuid = self.get_argument('uuid', default = '')
        appid = self.get_argument('appid', default = '')
        number = self.get_argument('number', default='')
        password = self.get_argument('password', default='')
        pe_password = self.get_argument('pe_password', default='')
        lib_username = self.get_argument('lib_username', default='')
        lib_password = self.get_argument('lib_password', default='')
        card_query_pwd = self.get_argument('card_query_pwd', default='')
        card_consume_pwd = self.get_argument('card_consume_pwd', default='')

        try:
            #通过uuid和appid检验权限
            app = self.db.query(Application).filter(
                Application.uuid == appid).one()
            pri = self.db.query(Privilege).filter(
                and_(Privilege.uuid == uuid, Privilege.aid == app.aid)).one()
            #通过uuid选择对应的用户
            user = self.db.query(User).filter(
                User.cardnum == pri.cardnum).one()
            cardnum = user.cardnum
            #非空则更改用户信息
            change_times = 0;
            if number:
                user.number = number
                change_times = change_times + 1
            if password:
                user.password = password
                change_times = change_times + 1
            if pe_password:
                user.pe_password = pe_password
                change_times = change_times + 1
            if lib_username:
                user.lib_username = lib_username
                change_times = change_times + 1
            if lib_password:
                user.lib_password = lib_password
                change_times = change_times + 1
            if card_query_pwd:
                user.card_query_pwd = card_query_pwd
                change_times = change_times + 1
            if card_consume_pwd:
                user.card_consume_pwd = card_consume_pwd
                change_times = change_times + 1

            self.db.add(user)
            self.db.commit()

            self.write('<p>修改成功，%d项更新。</p>'%(change_times))
            self.write('Herald Auth.')
            self.finish()
        except NoResultFound:
            raise tornado.web.HTTPError(401)
        self.finish()
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/26
# @Author : trl


import re
import time
import forgery_py
import unittest
import threading

from selenium import webdriver

from app import create_app, db
from app.config import TestingConfig
from app.models.user import Role, User


class SeleniumTest(unittest.TestCase):
    client = None
    app_ctx = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.client = webdriver.Firefox()
        except Exception as e:
            print e

        if cls.client:
            cls.app = create_app(TestingConfig)
            cls.app_ctx = cls.app.app_context()
            cls.app_ctx.push()

            db.drop_all()
            db.create_all()
            Role.insert_role()
            threading.Thread(target=cls.app.run).start()
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.client.get('http://localhost:5000/shutdown')
        cls.client.close()

        db.drop_all()
        db.session.remove()
        cls.app_ctx.pop()

    def setUp(self):
        if self.client is None:
            self.skipTest('略过测试')

    def tearDown(self):
        pass

    def test_user_register(self):
        from register_page import RegisterPage

        page = RegisterPage(self.client)
        self.client.get('http://localhost:5000/auth/register')
        self.assertTrue('注册' in page.title)

        username = forgery_py.internet.user_name(True)
        page.set_user_name(username)
        page.set_pwd(forgery_py.basic.text())
        page.set_re_pwd(forgery_py.basic.text())
        page.submit()

        self.assertTrue(re.search(username, self.client.page_source))

    def test_user_login(self):
        from login_page import LoginPage
        new_user = User(username=forgery_py.internet.user_name(True),
                        password='123456',
                        name=forgery_py.internet.user_name())
        db.session.add(new_user)
        db.session.commit()

        page = LoginPage(self.client)
        self.client.get('http://localhost:5000/auth/login')
        self.assertTrue('登录' in page.title)

        page.set_user_name(new_user.username)
        page.set_pwd('123456')
        page.submit()

        self.assertTrue(re.search(new_user.username, self.client.page_source))

if __name__ == '__main__':
    unittest.main()

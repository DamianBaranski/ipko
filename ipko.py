#! /usr/bin/env python3
# coding=utf8

import pycurl
import json
import requests
import re


class PKO:
    sid = ""
    flow_id = ""
    account = ""

    def _httpIPKO(self, url, data):
        headers = {'x-ias-ias_sid': self.sid,
                   'X-Requested-With': "XMLHttpRequest"}
        res = requests.post(url, json=data, headers=headers)
        return res.text

    def _getSID(self, login):
        url = "https://www.ipko.pl/secure/ikd3/api/login"
        data = {"_method": "POST",
                "version": 2, "seq": 1,
                "location": "",
                "request": {"state": "login",
                            "data": {"login": login}}}
        res = json.loads(self._httpIPKO(url, data))

        self.flow_id = res['response']['flow_id']
        self.sid = res['session']['sid']

        return self.sid, self.flow_id

    def _password(self, password):
        data = {"_method": "PUT",
                "sid": self.sid, "version": 2,
                "seq": 2, "location": "",
                "request": {"state": "password",
                            "flow_id": self.flow_id,
                            "first_prelogin": "true",
                            "data": {"password": password}}}
        url = "https://www.ipko.pl/secure/ikd3/api/login"
        self._httpIPKO(url, data)

    def _dispatch(self):
        data = {"_method": "PUT",
                "sid": self.sid,
                "version": 2,
                "seq": 3,
                "location": "",
                "request": {"state": "dispatch",
                            "flow_id": self.flow_id,
                            "first_prelogin": "true",
                            "data": {}}}
        url = "https://www.ipko.pl/secure/ikd3/api/login"
        self._httpIPKO(url, data)

    def login(self, login, password):
        self._getSID(login)
        self._password(password)
        self._dispatch()
        self._getAccountNumber()

    def _getAccountNumber(self):
        url = "https://www.ipko.pl/secure/ikd3/api/home/account"
        data = {"_method": "GET",
                "sid": self.sid,
                "seq": 10,
                "location": "#home",
                "request": {"object_id": "null"}}
        res = json.loads(self._httpIPKO(url, data))
        res = res['response']['filter']['account']['available'][0]
        self.account = res['data']['number']['value']
        return str(self.account)

    def getHistory(self):
        url = ("https://www.ipko.pl/secure/ikd3/api/"
               "accounts/operations/completed")
        data = {"_method": "POST",
                "sid": self.sid,
                "seq": 22,
                "location": "#accounts",
                "request": {"object_id": self.account,
                            "filter": {"page_size": 50}}}
        res = json.loads(self._httpIPKO(url, data))
        return res['response']['items']

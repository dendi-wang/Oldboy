#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import json
import os
from conf import settings


class dbHelper(object):
    def __init__(self, username):
        self.username = username

    def get_acc_data(self):
        account_file = '%s/%s.json' % (settings.DB_PATH, self.username)
        if os.path.exists(account_file):
            with open(account_file, 'r') as f:
                account_data = json.loads(f.read())
            account_data['home'] = '%s%s' % (settings.BASE_DIR, account_data['home'])
            return account_data
        else:
            return False

    def mod_acc(self, acc_dict):
        account_file = '%s/%s.json' % (settings.DB_PATH, self.username)
        with open(account_file, 'w') as f:
            f.write(json.dumps(acc_dict))
        return True

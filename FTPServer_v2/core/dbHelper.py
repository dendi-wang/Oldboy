#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import json
import os
from conf import settings


def dbHelper(username):
    account_file = '%s/%s.json' % (settings.DB_PATH, username)
    if os.path.exists(account_file):
        with open(account_file, 'r') as f:
            account_data = json.loads(f.read())
        account_data['home'] = '%s%s' % (settings.BASE_DIR, account_data['home'])
        return account_data
    else:
        return False

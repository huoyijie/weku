#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: huoyijie
@file: gen_secret_key.py
@time: 2018/08/29

@copyright: (c) 2018 by huoyijie, https://github.com/huoyijie/weku
@license: GPL v3, see LICENSE for more details.
"""

import string
import random

print(''.join(random.sample(string.ascii_letters + string.digits, 50)))

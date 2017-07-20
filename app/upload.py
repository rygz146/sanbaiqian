#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/13
# @Author : trl
from flask_uploads import UploadSet
from hashlib import md5


files = UploadSet('files')


def md5_filename(user, filename):

    return md5(user.uniqueID + filename).hexdigest().upper() + '.{}'.format(filename.split('.')[1])

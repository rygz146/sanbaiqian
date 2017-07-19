#!/usr/bin/python
# -*- coding: utf-8 -*-

import shutil


def write(local_file_path, content):
    try:
        with open(local_file_path, 'wb') as fo:
            shutil.copyfileobj(content.raw, fo)
    except IOError as err:
        print(local_file_path, err)

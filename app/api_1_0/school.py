#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
school
~~~~~~~~~~~~~~~~

关于学校会使用的一些api接口
"""

from flask import request

from app.log import Logger
from app.utils import json_response

from . import api
from ..models import db
from ..models.school import City


api_log = Logger('api_log', 'api.log', True)


@api.route('/province')
def get_province():
    provinces = db.session.query(City.province).group_by('province').order_by('id').all()
    data = [{'province': p.province} for p in provinces]

    return json_response(200, data)


@api.route('/district')
def get_district():
    province = request.args.get('province')
    districts = db.session.query(City.district).filter_by(province=province).group_by('district').order_by('id').all()
    data = [{'district': d.district} for d in districts]

    return json_response(200, data)


@api.route('/county')
def get_county():
    province = request.args.get('province')
    district = request.args.get('district')
    counties = db.session.query(City.id, City.county, City.zip_code).filter_by(province=province, district=district).order_by('id').all()
    data = [{'id': c.id, 'county': c.county, 'zip_code': c.zip_code} for c in counties]

    return json_response(200, data)

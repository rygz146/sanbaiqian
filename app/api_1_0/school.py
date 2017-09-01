#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
school
~~~~~~~~~~~~~~~~

关于学校会使用的一些api接口
"""

from flask import request, url_for

from ..log import Logger
from ..utils import json_response, json_page_response
from . import api
from ..models import db
from ..models.school import City


api_log = Logger('api_log', 'api.log', True)


@api.before_request
def api_before_request():
    print request.headers
    pass


@api.route('/')
def index():
    data = {
        'province': url_for('.get_province', _external=True),
        'district': url_for('.get_district', _external=True),
        'county': url_for('.get_county', _external=True),
        'schools': url_for('.get_schools', _external=True),
    }

    return json_response(200, data)


@api.route('/province')
def get_province():
    provinces = db.session.query(City.province).group_by('province').order_by('id').all()
    data = [{'province': p.province} for p in provinces]

    return json_response(200, data)


@api.route('/district')
def get_district():
    province = request.args.get('province')
    if province:
        districts = db.session.query(City.district).filter_by(province=province).group_by('district').order_by('id').all()
        data = [{'district': d.district} for d in districts]

        return json_response(200, data)
    else:
        return json_response(404, None, '参数错误')


@api.route('/county')
def get_county():
    province = request.args.get('province')
    district = request.args.get('district')
    if province and district:
        counties = db.session.query(City.id,
                                    City.county,
                                    City.zip_code).filter_by(province=province, district=district).order_by('id').all()
        data = [{'id': c.id, 'county': c.county, 'zip_code': c.zip_code} for c in counties]
        return json_response(200, data)
    else:
        return json_response(404, None, '参数错误')


@api.route('/schools')
def get_schools():
    page = request.args.get('page', 1, int)
    city_id = request.args.get('city_id', 1, int)
    pagination = City.query.filter_by(id=city_id).first().schools.paginate(page=page, per_page=5, error_out=False)
    schools = pagination.items
    data = [s.to_json() for s in schools]

    return json_page_response(200, pagination, data)

# coding:utf8

"""
Copyright 2016 Smallpay Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from flask import Blueprint
from flask_restful import Api
from pluto.backend.api import ApiResource
from pluto.backend.models import Depot, DepotBill


bp = Blueprint('restapi_depot', __name__)
api = Api(bp)


@api.resource('/depots')
class DepotListResource(ApiResource):

    def get(self):
        return Depot.query.filter(Depot.merchant_code == '1001').all()


@api.resource('/depots/<int:depot_id>')
class DepotResource(ApiResource):

    def get(self, depot_id):
        return Depot.query.filter(Depot.id == depot_id).first()


@api.resource('/depots/bills')
class DepotBillListResource(ApiResource):

    def get(self):
        return DepotBill.query.filter(Depot.merchant_code == '1001').first()


@api.resource('/depots/test')
class TestResource(ApiResource):

    def get(self):
        html = """<table width="420" cellspacing="0" cellpadding="0" border="0"><caption>北景区环保车票</caption><colgroup><col width="170" span="1" /><col width="250" span="1" /></colgroup><thead><tr><th class="blue" colspan="2">8.50元</th></tr><tr><th colspan="2">< img src="http://qr.liantu.com/api.php?text=1010011000001000000000000188224190050" alt="" /></th></tr><tr class="dashed"><th colspan="2">预约入园时间<p class="blue">2016-07-26 15:00:00</p ></th></tr></thead><tbody><tr class="dashed"><td class="right">证件姓名</td><td>1</td></tr><tr><td class="right">证件类型</td><td>护照</td></tr><tr><td class="right">证件号</td><td>1</td></tr><tr><td class="right">补打次数</td><td>31</td></tr><tr><td class="right">客服电话</td><td>010-10101010</td></tr><tr><td class="right">购票渠道</td><td>人工售票系统</td></tr></tbody></table>"""
        data_list = []
        data_list.append(html)
        data_list.append(html)
        return data_list
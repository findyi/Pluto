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
from flask_restful import Api, abort
from flask_restful.reqparse import Argument

from pluto.backend.api import ApiResource
from pluto.backend.models import Material, MaterialCategory


bp = Blueprint('restapi_material', __name__)
api = Api(bp)


@api.resource('/materials')
class MaterialListResource(ApiResource):

    _query_arguments = [
        Argument('merchant_code', required=True, type=str),
        Argument('category_id', type=int)
    ]

    def get(self):
        merchant_code = self.get_argument('merchant_code')
        category_id = self.get_argument('category_id')
        q = Material.query.filter(Material.merchant_code == merchant_code)
        if category_id:
            q = q.filter(Material.category_id == category_id)
        return q.all()

    def post(self):
        material = self.parse_body_to_model(Material)
        self.session.add(material)
        return material


@api.resource('/materials/categories')
class MaterialCategoryListResource(ApiResource):

    _query_arguments = [
        Argument('merchant_code', required=True, type=str),
        Argument('parent_category_id', required=False, type=int),
    ]

    def get(self):
        merchant_code = self.get_argument('merchant_code')
        parent_category_id = self.get_argument('parent_category_id')
        q = MaterialCategory.query.filter(MaterialCategory.merchant_code == merchant_code)
        if parent_category_id:
            q = q.filter(MaterialCategory.parent_id == parent_category_id)
        return q.all()

    def post(self):
        material_category = self.parse_body_to_model(MaterialCategory)
        db_material_category = MaterialCategory.query.\
            filter(MaterialCategory.parent_id == material_category.parent_id).\
            filter(MaterialCategory.name == material_category.name).first()
        if db_material_category:
            abort(400, message="同一个父分类ID下面,分类名称不能相同")

        self.session.add(material_category)
        self.session.commit()
        return material_category

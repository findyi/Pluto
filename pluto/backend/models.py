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
from pluto.backend import db
from sqlalchemy.orm.instrumentation import ClassManager
from sqlalchemy.ext.declarative import AbstractConcreteBase


class BaseModel(db.Model):

    __abstract__ = True

    def __str__(self):
        attr_names = self._get_attribute_names()
        attrs = ["%s=%s" % (attr_name, getattr(self, attr_name)) for attr_name in attr_names]
        return ",".join(attrs)

    def to_dict(self, excludes=(), include_none_value=True, **kwargs):
        dicts = dict()
        attr_names = self._get_attribute_names()
        for attr in attr_names:
            if not attr.startswith('_') and attr not in excludes:
                v = getattr(self, attr)
                if not include_none_value and v is None:
                    continue
                if isinstance(v, BaseModel):
                    v = v.to_dict()
                if attr in kwargs:
                    dicts[kwargs.get(attr)] = v
                else:
                    dicts[attr] = v
        return dicts

    def _get_attribute_names(self):
        """获取对象需要序列化的属性字段
        :return: list
        """
        sa_instance_state = getattr(self, ClassManager.STATE_ATTR, None)
        if sa_instance_state:
            attr_dct = sa_instance_state.attrs._data
            return attr_dct.keys()
        return self.__dict__

    def from_dict(self, dicts):
        keys = dicts.keys()
        for attr in self._get_attribute_names():
            if not attr.startswith('_') and attr in keys:
                setattr(self, attr, dicts.get(attr))
        return self

    def copy_from(self, other):
        assert type(other) == type(self)
        for attr in self._get_attribute_names():
            if not attr.startswith('_'):
                v = getattr(other, attr)
                if v is not None:
                    setattr(self, attr, v)


class Depot(BaseModel):

    __tablename__ = 'depot'

    id = db.Column(db.Integer, primary_key=True)
    merchant_code = db.Column(db.String(32))
    depot_type = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    is_enable = db.Column(db.Integer())
    create_time = db.Column(db.TIMESTAMP())


class DepotBill(BaseModel):

    __tablename__ = 'depot_bill'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32))
    bill_type = db.Column(db.Integer)
    name = db.Column(db.String(64))
    merchant_code = db.Column(db.String(32))
    operator = db.Column(db.String(32))
    status = db.Column(db.Integer())
    create_time = db.Column(db.TIMESTAMP())


class Material(BaseModel):

    __tablename__ = 'material'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32))
    merchant_code = db.Column(db.String(32))
    name = db.Column(db.String(64))
    category_id = db.Column(db.Integer())
    consume_unit_id = db.Column(db.Integer())
    purchase_unit_id = db.Column(db.Integer())
    check_unit_id = db.Column(db.Integer())
    pc_proportion = db.Column(db.Float())
    cc_proportion = db.Column(db.Float())
    is_enable = db.Column(db.Integer())
    create_time = db.Column(db.TIMESTAMP())


class MaterialCategory(BaseModel):

    __tablename__ = 'material_category'

    id = db.Column(db.Integer, primary_key=True)
    merchant_code = db.Column(db.String(32))
    parent_id = db.Column(db.Integer())
    name = db.Column(db.String(64))
    create_time = db.Column(db.TIMESTAMP())

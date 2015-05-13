import time
#from rethinkengine import Document
from datetime import datetime
from decimal import Decimal
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()
class Model(db.Document):
  meta = {'allow_inheritance': True}
  #def put(self, *args, **kwargs):
  #  pass

  @classmethod
  def get(cls, *args, **kwargs):
    try:
      return cls.objects.get(*args, **kwargs)
    except:
      return None

  def save(self, *args, **kwargs):
    self.updated = datetime.now
    super().save(*args, **kwargs)

  def dict_to_attr(self, obj):
    keys = obj.keys()
    for key in keys:
      setattr(self, key, obj[key])


#class Model(SdbModel):
#  @classmethod
#  def find_one(cls, *args, **kwargs):
#    for instance in cls.find(*args, **kwargs):
#      return instance
#
#  @classmethod
#  def get(cls, *args, **kwargs):
#    return cls.get_by_id(*args, **kwargs)
#
#  def is_new(self):
#    return not self.id
#
#  def put(self, *args, **kwargs):
#    for field in self.properties(hidden=True):
#      if not isinstance(field, prop._ReverseReferenceProperty):
#        value = getattr(self, field.name, None)
#        field.validate(value)
#    return super(Model, self).put(*args, **kwargs)

#class DecimalProperty(prop.Property):
#  data_type = Decimal
#  type_name = 'Decimal'
#
#  def __init__(self, verbose_name=None, name=None, default=None, required=False,
#               validator=None, choices=None, unique=False):
#    prop.Property.__init__(self, verbose_name, name, default, required,
#                           validator, choices, unique)
#
#  def validate(self, value):
#    if value is not None:
#      value = Decimal(value)
#    value = prop.Property.validate(self, value)
#    return value
#
#  def make_value_from_datastore(self, value):
#    if value:
#      return Decimal(value)
#
#  def empty(self, value):
#    return value is None

class money_property(object):
  def __init__(self, named):
    self._named = named
    pass

  def __get__(self, obj, objtype=None):
    cents = getattr(obj, self._named)
    return Decimal(cents) / 100

  def __set__(self, obj, decimal_value):
    cents = long(decimal_value * 100)
    setattr(obj, self._named, cents)

class epoch_property(object):
  def __init__(self, named):
    self._named = named
    pass

  def __get__(self, obj, objtype=None):
    epoch_timestamp = getattr(obj, self._named)
    return datetime.fromtimestamp(epoch_timestamp)

  def __set__(self, obj, datetime_inst):
    epoch_timestamp = time.mktime(datetime_inst.timetuple())
    setattr(obj, self._named, long(epoch_timestamp))

from .project import Project
from .medium import Medium
from .datapoint import DataPoint
from .webproperty import WebProperty
from .account import Account
from .user import User



from pprint import pprint

from datetime import datetime
from makers.models import db
from makers.models import Model
from makers.models import Medium

class DataPoint(Model):
  #name     = db.StringField(required=True)
  medium    = db.ReferenceField(Medium, required=True)
  data      = db.DictField()
  type      = db.StringField()
  date      = db.DateTimeField(default=datetime.today())
  created   = db.DateTimeField(default=datetime.now())
  updated   = db.DateTimeField(default=datetime.now())
  #groups       = db.DictField() #{group: [id,id,id]}
  #saved       = db.BooleanField(required=True, default=False) #pulled from google, might need to rename


  def sync(self):
    return False

  def change(self, date=None):
    if date is None:
      return 0
    dp = DataPoint.objects(medium=self.medium, date=datetime(date.year,date.month,date.day),data__source=self.data['source']).first()
    if self.type == 'trend' and dp is not None:
      if int(dp.data['visits']) == 0 and int(self.data['visits'])==0:
        return 0
      if int(dp.data['visits']) == 0:
       dp.data['visits'] = 1
      return round((int(self.data['visits']) - int(dp.data['visits'])) / int(dp.data['visits']),4)
    else:
      return 1 #doesn't exist.. all change is 100%

  def dict(self, diff=None):
    return {
      'id':    str(self.id),
      'medium': self.medium.dict(),
      'date':  self.date.strftime('%Y-%m-%d'),
      'data':  self.data,
      'change': self.change(diff),
      #'updated':  self.updated,
      #'customer_id': self.customer_id,
      #'active':      self.active,
      #'admin':       self.admin,
    }

  def __unicode__(self):
    return self.data['source']



from datetime import datetime
from makers.models import db
from makers.models import Model
from makers.models import WebProperty

class Account(Model):
  id           = db.StringField(primary_key=True)
  webproperties = db.ListField(field=db.ReferenceField(WebProperty))
  name         = db.StringField(required=True)
  #groups       = db.DictField() #{group: [id,id,id]}
  created     = db.DateTimeField(default=datetime.now)
  updated     = db.DateTimeField(default=datetime.now)
  #saved       = db.BooleanField(required=True, default=False) #pulled from google, might need to rename

  def dict(self):
    return {
      'id':    self.id,
      'webproperties': [p.dict() for p in self.webproperties],
      #'updated':  self.updated,
      'name':  self.name,
      #'customer_id': self.customer_id,
      #'active':      self.active,
      #'admin':       self.admin,
    }

  #def __unicode__(self):
  #  return self.display_name



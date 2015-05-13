from datetime import datetime
from makers.models import db
from makers.models import Model


class Project(Model):
  id          = db.StringField(primary_key=True)
  name        = db.StringField(required=True)
  groups      = db.DictField() #{group: [id,id,id]}
  created     = db.DateTimeField(default=datetime.now)
  updated     = db.DateTimeField(default=datetime.now)
  saved       = db.BooleanField(required=True, default=False) #pulled from google, might need to rename


  def dict(self):
    return {
      'id':    self.id,
      #'updated':  self.updated,
      'name':  self.name,
      'saved': self.saved,
      #'customer_id': self.customer_id,
      #'active':      self.active,
      #'admin':       self.admin,
    }

  def __unicode__(self):
    return self.name



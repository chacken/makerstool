from datetime import datetime
from makers.models import db
from makers.models import Model
from makers.models import Project

class Medium(Model):
  name     = db.StringField(required=True)
  project  = db.ReferenceField(Project, required=True)
  #data     = db.DictField()
  type     = db.StringField()
  #groups       = db.DictField() #{group: [id,id,id]}
  created     = db.DateTimeField(default=datetime.now())
  updated     = db.DateTimeField(default=datetime.now())
  #saved       = db.BooleanField(required=True, default=False) #pulled from google, might need to rename


  def sync(self):
    return False

  def dict(self):
    return {
      'id':    str(self.id),
      'name':    self.name,
      'type':    self.type,
      'project': self.project.dict(),
      #'data':  self.data,
      #'updated':  self.updated,
      #'customer_id': self.customer_id,
      #'active':      self.active,
      #'admin':       self.admin,
    }

  #def __unicode__(self):
  #  return self.display_name



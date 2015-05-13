from datetime import datetime
from makers.models import db
from makers.models import Model
from makers.models import Project

class WebProperty(Model):
  id           = db.StringField(primary_key=True)
  #account   = db.ReferenceField(required=True)
  projects  = db.ListField(field=db.ReferenceField(Project))
  name         = db.StringField(required=True)
  #groups       = db.DictField() #{group: [id,id,id]}
  created     = db.DateTimeField(default=datetime.now)
  updated     = db.DateTimeField(default=datetime.now)
  #saved       = db.BooleanField(required=True, default=False) #pulled from google, might need to rename


  def dict(self):
    return {
      'id':    self.id,
      'projects':    [p.dict() for p in self.projects],
      #'property_id':    self.property_id,
      #'updated':  self.updated,
      'name':  self.name,
      #'customer_id': self.customer_id,
      #'active':      self.active,
      #'admin':       self.admin,
    }

  #def __unicode__(self):
  #  return self.display_name



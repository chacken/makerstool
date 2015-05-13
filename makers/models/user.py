from datetime import datetime
from hashlib import sha1
from random import random

from makers.models import db
from makers.models import Model
from makers.models import Account



class User(Model):
  id            = db.StringField(primary_key=True)
  refresh_token = db.StringField()
  email         = db.EmailField(required=True)
  display_name  = db.StringField(required=True)
  given_name    = db.StringField(required=True)
  family_name   = db.StringField()
  flags         = db.DictField()
  accounts      = db.ListField(field=db.ReferenceField(Account))
  created       = db.DateTimeField(default=datetime.now())
  updated       = db.DateTimeField(default=datetime.now())
  last_login    = db.DateTimeField(default=datetime.now())
  #active        = prop.BooleanProperty(default=True)
  #address       = prop.ReferenceProperty(Address, required=False)
  #email         = prop.StringProperty(required=True)
  #password      = prop.StringProperty(required=True)

  @property
  def full_name(self):
    return ' '.join([self.first_name,self.last_name])

  @classmethod
  def authenticate(cls, email, password):
    """
    A Rough approximation of Django's built-in authentication mechanism. This is
    due to the origional prototype being build on Django, and already having a
    few users testing the system.
    """
    user = cls.find_one(email = email.lower())
    if not user or not user.password:
      return None
    algo, salt, hsh = user.password.split('$')

    if algo == 'sha1':
      digest = sha1(salt + password).hexdigest()
      if digest == hsh:
        return user
      else:
        return None
    else:
      raise ValueError('Unknown password algo, %s' % algo)

  def set_password(self, password, algo='sha1'):
    """
    Set the encrypted password of this user based on the given clear text
    password.
    """
    algo = 'sha1'
    salt = sha1(str(random())).hexdigest()[:5]
    hsh = sha1(salt+password).hexdigest()
    self.password = '%s$%s$%s' % (algo, salt, hsh)

  def put(self, *args, **kwargs):
    """
    Before persisting a user, perform a few checks and modifications to make
    sure that the entity is valid. For example, a user's email address should
    always be lower cased.
    """
    if self.email:
      self.email = self.email.lower()
    super(User, self).put(*args, **kwargs)

  def delete(self, *args, **kwargs):
    """
    When deleting a user, ensure that attached entities are also cleaned up. For
    example, networks and advertisers.
    """
    #for advertiser in self.advertiser_user_set:
    #  advertiser.delete()

    #for network in self.network_user_set:
    #  network.delete()

    super(User, self).delete(*args, **kwargs)

  def dict(self):
    return {
      'id':          self.id,
      # don't show this.. just for testing.
      #'refresh_token':  self.refresh_token,
      #'active':      self.active,
      'family_name':  self.family_name,
      'given_name':   self.given_name,
      'display_name': self.display_name,
      'email':       self.email,
    }

  def __unicode__(self):
    return self.email



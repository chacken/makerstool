import wtforms as wtf

from datetime import datetime

class EpochField(wtf.IntegerField):

  def process_formdata(self, valuelist):
    if valuelist:
      try:
        timestamp = int(valuelist[0])
        self.data = datetime.fromtimestamp(timestamp)
      except:
        raise ValueError('Not a valid date time')

class CentField(wtf.DecimalField):
  def process_formdata(self, valuelist):
    super(CentField, self).process_formdata(valuelist)
    if self.data:
      self.data = self.data * 100




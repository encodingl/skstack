

from django.db import models

# Create your models here.
class Rpt(models.Model):
    pnum = models.IntegerField()
    vm = models.IntegerField()
    user  = models.IntegerField()
    app = models.IntegerField()
    
   #def __unicode__(self):
    #    return self.pnum

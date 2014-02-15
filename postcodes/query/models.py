from django.db import models

# Create your models here.

class Postcode(models.Model):

    code = models.CharField(max_length=20, unique=True)
    latitude = models.CharField(max_length=20, blank=True)
    longitude = models.CharField(max_length=20, blank=True)

    def __unicode__(self):
        return u'%s' % (self.code)

class Distance(models.Model):

    distance = models.IntegerField(blank=True, null=True)
    a = models.ForeignKey(Postcode, related_name='distance_to')
    b = models.ForeignKey(Postcode, related_name='distance_from')

    def __unicode__(self):
        return u'%s %s %s' % (self.a, 'to', self.b)

        #Unique together(postcode_a, postcode_b)




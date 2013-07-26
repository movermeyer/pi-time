import datetime
import django_settings
import utils
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime

# Setting models

class Boolean(django_settings.db.Model):
	value = models.BooleanField()

	class Meta:
		abstract = True

class GPIOLayout(django_settings.db.Model):
	value = models.PositiveSmallIntegerField(max_length=2, choices=settings.GPIO_LAYOUT)

	class Meta:
		abstract = True

class UnitOfMeasurement(django_settings.db.Model):
	value = models.CharField(max_length=2, choices=settings.UNIT_OF_MEASUREMENT)

	class Meta:
		abstract = True

django_settings.register(Boolean)
django_settings.register(GPIOLayout)
django_settings.register(UnitOfMeasurement)

# Data models

class Track(models.Model):
	name = models.CharField(max_length=64, unique=True)
	distance = models.FloatField()
	timeout = models.PositiveSmallIntegerField()

	def save(self, *args, **kwargs):
		if (self.timeout is None):
			self.timeout = int(self.distance * 2)
		super(Track, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Session(models.Model):
	name = models.CharField(max_length=64, unique=True)
	track = models.ForeignKey(Track)
	start = models.DateTimeField()
	finish = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if (self.start is None):
			self.start = timezone.make_aware(datetime.datetime.now(),
				timezone.get_default_timezone())
		super(Session, self).save(*args, **kwargs)

class Rider(models.Model):
	name = models.CharField(max_length=64, unique=True)

	def __unicode__(self):
		return self.name

class Lap(models.Model):
	session = models.ForeignKey(Session)
	rider = models.ForeignKey(Rider)
	start = models.DateTimeField()
	finish =  models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		if (self.finish is None):
			return 'Elapsed Time: ' + utils.time_to_str(self.start, None)
		else:
			return 'Lap Time: ' + utils.time_to_str(self.start, self.finish)

	def save(self, *args, **kwargs):
		if (self.start is None):
			self.start = timezone.make_aware(datetime.datetime.now(),
				timezone.get_default_timezone())
		super(Lap, self).save(*args, **kwargs)

	def average_speed_per_hour(self):
		return utils.average_speed_per_hour(self.start, self.finish,
			self.session.track.distance)

	def average_speed_per_second(self):
		return utils.average_speed_per_second(self.start, self.finish,
			self.session.track.distance)

class Statistics:
	number_of_laps = int
	lap_time = float
	average_speed_per_hour = float
	average_speed_per_second = float

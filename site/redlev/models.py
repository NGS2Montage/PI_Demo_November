# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json

# Create your models here.

class ThresholdSamples(models.Model):
	R = models.FloatField()
	m = models.FloatField()
	mse = models.FloatField()
	nObs = models.IntegerField()
	std = models.FloatField()
	mean = models.FloatField()
	ratio = models.FloatField()
	activeRange = models.FloatField()
	max_val = models.FloatField()
	
	dist = models.TextField()
	
	def get_dist(self):
		return json.loads(self.dist)

	
class ContourVals(models.Model):
	nObs = models.IntegerField()
	conf = models.TextField()
	res = models.IntegerField()
	
	xi_vals = models.TextField()
	ratio_vals = models.TextField()
	
	def get_xi_vals(self):
		return json.loads(self.xi_vals)
		
	def get_ratio_vals(self):
		return json.loads(self.ratio_vals)
	
	
class Distribution(models.Model):
	nObs = models.IntegerField()
	xi = models.FloatField()
	res = models.IntegerField()
	
	ratio_vals = models.TextField()
	prob_vals = models.TextField()
	
	def get_ratio_vals(self):
		return json.loads(self.ratio_vals)
		
	def get_prob_vals(self):
		return json.loads(self.prob_vals)
		
	def get_error_vals(self):
		out = [x * self.nObs for x in json.loads(self.ratio_vals)]
		return out
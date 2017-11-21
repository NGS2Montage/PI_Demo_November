# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from .models import ContourVals, Distribution

import numpy as np
import json

# Create your views here.
def index(request):

    #Inputs
    nErrors = request.GET.get('n_errors',None)
    alpha = request.GET.get('alpha',None)
    mse = request.GET.get('mse',None)
    threshold = request.GET.get('threshold',None)
    
    nObs = 128
    res = 1000
    
    if (mse or threshold) and alpha and nErrors:
        mse = float(mse)
        threshold = float(threshold)
        alpha = float(alpha)
        nErrors = int(nErrors)
        
        xi_location = 1
        
    elif mse and threshold:
    	  mse = float(mse)
    	  threshold = float(threshold)
    	  R = (nObs * mse) ** 0.5
    	  xi_location = (R - threshold) / (threshold * ( nObs ** 0.5 - 1))
    	  nErrors = None
    	 
    else:
    	 return render(request, 'redlev/redlev.html', {
    	 	 'contours': '',
    		 'nObs': nObs,
    		 'xi_location': '',
    		 'errorDist': '',
    		 'mseThreshold': '',
    		 'complete': False,
    		 'nErrors': None,
    		})
    
    out = []
    for c in ContourVals.objects.filter(nObs=nObs, res=res):
        xy = zip(c.get_xi_vals(), c.get_ratio_vals())
        xy_dict = [dict(zip(['x','y'], d)) for d in xy]        
        out.append({
            'conf': c.conf,
            'data': xy_dict,
        })
        
    contours = json.dumps(out)
    
    errorDist = Distribution.objects.filter(nObs=nObs, res=res, xi__lt=xi_location).order_by('-xi').first()
    xy = zip(errorDist.get_error_vals(), errorDist.get_prob_vals())
    xy_dict = [dict(zip(['x','y'], d)) for d in xy]
    errorDistDict = json.dumps({'xi': errorDist.xi, 'data': xy_dict})

    xi = errorDist.xi
    tau = np.linspace(0.01, 100, 20)
    R = (xi * (nObs ** 0.5 - 1) * tau) + tau
    mseArray = np.log10(R ** 2 / nObs)
    
    xy = zip(tau, mseArray)
    xy_dict = [dict(zip(['x','y'], d)) for d in xy]
    mseDistDict = json.dumps({'xi': errorDist.xi, 'data': xy_dict})
    
	     
    
    return render(request, 'redlev/redlev.html', 
    		{'contours': contours,
    		 'nObs': nObs,
    		 'xi_location': xi_location,
    		 'errorDist': errorDistDict,
    		 'mseThreshold': mseDistDict,
    		 'complete': True,
    		 'nErrors': nErrors,
    		 'mse': mse,
    		 'alpha': alpha,
    		 'threshold': threshold,
    		})
    

def errorDistribution(request):
	
	return JsonResponse({})
	
	
def thresholdMseCurve(request):
	
	return JsonResponse({})
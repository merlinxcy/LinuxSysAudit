# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import monlib
# Create your views here.
def show(request):
	#return HttpResponse("hello world")
	context={}
	dbo=monlib.monlib()
	syslog=dbo.outputall(collection='syslog')
	context['context']=str(syslog)
	return render(request,"index.html",context)
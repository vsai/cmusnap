from django.shortcuts import render, redirect, get_object_or_404
from django.utils import simplejson as json
from django.http.response import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import socket, thread

IP_addresses = [];  # array since we're assuming RasPis

def home(request):
  configure()
  return render(request, "index.html", {})

def searchForRasPis(request):
  context = {}
  global IP_addresses
  print "searching for rasPis here..."



  #ASSUMING I TALK TO SERVER
  #server_result = ["1.2.3.4", "5.6.7.8"]

  #context['RasPis'] = server_result
  thread.start_new_thread(configure, ())

  print "--"
  print "IP:", IP_addresses
  context['RasPis'] = IP_addresses
  data = json.dumps(context, cls=DjangoJSONEncoder)

  return HttpResponse(data, mimetype="application/json", status="200")


def configure():
  global IP_addresses
  print "called configure"
  host = 'localhost'
  port = 50000 
  size = 1024 
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
  s.connect((host,port)) 
  s.send('Hello, World!') 
  data = s.recv(size) 
  s.close() 
  print 'Received:', data
  IP_addresses = data.split(',')
  print 'IPs:', IP_addresses
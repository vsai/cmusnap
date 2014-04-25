from django.shortcuts import render, redirect, get_object_or_404
from django.utils import simplejson as json
from django.http.response import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import socket, thread

config = {}; 

def home(request):
  global config
  context = {}
  config = recv_server()
  context['RasPis'] = config
  return render(request, "index.html", context)

def searchForRasPis(request):
  context = {}
  global config
  print "searching for rasPis here..."

  thread.start_new_thread(recv_server, ())

  context['RasPis'] = config

  print context
  data = json.dumps(context, cls=DjangoJSONEncoder)

  return HttpResponse(data, mimetype="application/json", status="200")

def config_handler(request):

  updated_selected = request.POST.getlist('dev_name')
  update_config(updated_selected)
  send_server()

  context = {}
  data = json.dumps(context, cls=DjangoJSONEncoder)
  return HttpResponse(data, mimetype="application/json", status="200")
  




def recv_server():
  # TODO: THIS NEEDS TO BE FIXED TO ACTUAL CODE

  # global IP_addresses
  # print "called recv_server"
  # host = 'localhost' #change this to the correct IP address of server
  # port = 50000 
  # size = 1024 
  # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
  # s.connect((host,port)) 
  # data = s.recv(size) 
  # s.close() 
  # IP_addresses = data.split(',')

  global config
  recv_data = "0:1,1:0,2:0,3:1,5:0"
  config = mapSRVRDataToDict(recv_data)
  print "-->"


def send_server():
  global config
  print "trying to send server!!", config



##### HELPERS #####

def mapSRVRDataToDict(input_str):
  res = {}
  data_array = input_str.split(',')
  for i in range(0,len(data_array)):
    item_info = data_array[i].split(':')
    item_name = item_info[0]
    item_config = item_info[1]
    res[item_name] = item_config

  return res

# changes the config global var
def update_config(updated_selected):
  global config

  print "hey there!"















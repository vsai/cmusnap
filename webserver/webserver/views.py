from django.shortcuts import render, redirect, get_object_or_404
from django.utils import simplejson as json
from django.http.response import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import socket, thread

config = {};
ipsToIds = {}
HOST = 'unix4.andrew.cmu.edu'   # The remote host
PORT = 4863                     # The same port as used by the server
SIZE = 1024                     # Receive size of data from server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connectToServer(s):
    """ Attempts to connect to server """
    while True:
        try:
            s.connect((HOST, PORT))
        except:
            print "Could not connect to server. Will try again in 5 seconds"
            time.sleep(5)
        else:
            print "Successfully connected to server!"
            return

thread.start_new_thread(connectToServer, (s,))

def home(request):
  global config
  context = {}
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
    global config,s, ipsToIds
    while True:
        data = s.recv(SIZE) 
        config, ipsToIds = mapSRVRDataToDict(data)


def send_server():
    global config
    toSend = mapDictToSRVRData(config)
    s.sendall(toSend) 


##### HELPERS #####

def mapSRVRDataToDict(input_str):
  """ Input has form ip:id for a new raspi at ip 'ip' with id 'id' """
  global config, ipsToIds
  newIpsToIds = dict()
  new_config = dict()
  inputData = input_str.split(',')
  for s in inputData:
    (ip, _, nickname) = s.partition(':')
    # Add all new Ips and default their configuration to on
    newIpsToIds[ip] = nickname
    if ip not in ipsToIds:
        new_config[ip] = 1
    else: 
        new_config[ip] = config[ip]

  return new_config, newIpsToIds

def mapDictToSRVRData(config):
  global ipsToIds
  res_str = ""

  for ip in config:
    keyStr = str(ipsToIds[ip])
    valStr = str(config[ip])
    keyValStr = keyStr + ":" + valStr

    res_str += keyValStr + ","

  # remove the last comma to fit spec
  res_str = res_str[:-1]

  return (res_str + '\n')

# changes the config global var
def update_config(updated_selected):
  global config

  for k in iter(config):
    if k in updated_selected:
      config[k] = 1
    else:
      config[k] = 0


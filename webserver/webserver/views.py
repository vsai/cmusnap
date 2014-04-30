from django.shortcuts import render, redirect, get_object_or_404
from django.utils import simplejson as json
from django.http.response import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import photo_handler

import socket, thread, string, time, string

config = {}
idsToIps = {}
HOST = 'unix4.andrew.cmu.edu'   # The remote host
PORT = 4864                     # The same port as used by the server
SIZE = 1024                     # Receive size of data from server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connectToServer():
    """ Attempts to connect to server """
    while True:
        try:
            s.connect((HOST, PORT))
        except:
            print "Could not connect to server. Will try again in 5 seconds"
            time.sleep(5)
        else:
            print "Successfully connected to server!"
            break

    recv_server()

thread.start_new_thread(connectToServer, ())

def home(request):
  global config
  context = {}
  context['RasPis'] = config
  return render(request, "index.html", context)

def searchForRasPis(request):

  ### TEMP PLACED HERE
  handleImages()
  ###

  context = {}
  global config
  print "searching for rasPis here..."
  context['RasPis'] = config

  print context
  data = json.dumps(context, cls=DjangoJSONEncoder)

  return HttpResponse(data, mimetype="application/json", status="200")

def config_handler(request):
  global config, idsToIps
  print "in config_handler"
  updated_selected = request.POST.getlist('dev_name')
  update_config(updated_selected)
  send_server()

  context = {}
  data = json.dumps(context, cls=DjangoJSONEncoder)
  return HttpResponse(data, mimetype="application/json", status="200")
  

def recv_server():
    global config, idsToIps
    while True:
        data = s.recv(SIZE) 
        print "here"
        if data.startswith('Done'):
          groupID = data[4:]
          print "Attempting to pull %s pics from AWS" % groupID
          thread.start_new_thread(pullFromAWS, (groupID,))
        else:
          config, idsToIps = mapSRVRDataToDict(data)


def send_server():
    global config
    toSend = mapDictToSRVRData(config)
    s.sendall(toSend) 


##### HELPERS #####


def handleImages():
  photo_handler.pullFromAWS("1")


def mapSRVRDataToDict(input_str):
  global config, idsToIps
  """ Input has form ip:id for a new raspi at ip 'ip' with id 'id' """
  newIdsToIps = dict()
  new_config = dict()
  inputData = input_str.split(',')
  for s in inputData:
    if not s: continue
    (nickname, _, ip) = s.partition(':')
    # Add all new Ips and default their configuration to on
    newIdsToIps[nickname] = ip
    if ip not in idsToIps:
        new_config[nickname] = 1
    else: 
        new_config[nickname] = config[nickname]
  print new_config, newIdsToIps
  return new_config, newIdsToIps

def mapDictToSRVRData(config):
  res_str = ""

  for nickname in config:
    keyStr = str(nickname)
    valStr = str(config[nickname])
    keyValStr = keyStr + ":" + valStr

    res_str += keyValStr + ","

  # remove the last comma to fit spec
  res_str = res_str[:-1]

  return (res_str + '\n')

# changes the config global var
def update_config(updated_selected):
  global config, idsToIps
  for k in config:
    if k in updated_selected:
      config[k] = 1
    else:
      config[k] = 0


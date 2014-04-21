from django.shortcuts import render, redirect, get_object_or_404
import socket

def home(request):
  configure
  return render(request, "index.html", {})
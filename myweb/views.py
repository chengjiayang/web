from django.shortcuts import render,HttpResponse,redirect,reverse


def hello(request):
    return HttpResponse("Hello world ! ")


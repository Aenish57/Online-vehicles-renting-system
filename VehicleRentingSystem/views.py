#Created by Yash
from django.http import HttpResponse
from django.shortcuts import render


def Owner(request):
    return HttpResponse('About Us')
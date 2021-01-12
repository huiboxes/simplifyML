from django.shortcuts import render
from django.http import JsonResponse

def categorie(request):

    return JsonResponse({'code': '200','status': 'OK'})

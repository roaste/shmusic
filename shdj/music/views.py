from django.shortcuts import render
from . import oop
import time
# Create your views here.
def music(request):
	'''Главная страница'''
	return render(request, 'main.html' ,context={'check':request},)
def get_music(request):
	'''Работа с формами'''
	check = oop.backend(request)

	data = check.validator()
	if data[0:3] == 'ok|':
		data = data.strip('ok|')
		return render(request, 'form_generic.html' ,context={'result':data},)
	elif data == 'time_error':
		return render(request, 'form_generic.html' ,context={'result':'Ошибка в указании времени'},)
	elif data == 'link_error':
		return render(request, 'form_generic.html' ,context={'result':'Ошибка в указании ссылки'},)
	# if request.method == 'GET':
	# 	if 'timeof' in request.GET and 'timeto' in request.GET and 'link' in request.GET:
	# 		print('ok')
	# 		return render(request, 'main.html' ,context={'check':request},)
	# 	else:
	# 		print('not ok')
	# 		return render(request, 'main.html' ,context={'check':request},)
